import trio
from types import TracebackType
from typing import Optional, Type
from osn_selenium.dev_tools._decorators import log_on_error
from osn_selenium.dev_tools._wrappers import DevToolsPackage
from osn_selenium.dev_tools.manager.targets import TargetsMixin
from osn_selenium.dev_tools.logger.main import build_main_logger
from osn_selenium.dev_tools._exception_helpers import log_exception
from osn_selenium.exceptions.devtools import (
	BidiConnectionNotEstablishedError,
	CDPEndExceptions,
	CantEnterDevToolsContextError
)


__all__ = ["LifecycleMixin"]


class LifecycleMixin(TargetsMixin):
	"""
	Mixin managing the lifecycle of the DevTools context, including connection setup and teardown.
	"""
	
	def _get_websocket_url(self) -> None:
		"""
		Retrieves the WebSocket URL for DevTools from the WebDriver.

		This method attempts to get the WebSocket URL from the WebDriver capabilities or by directly querying the CDP details.
		The WebSocket URL is necessary to establish a connection to the browser's DevTools.

		Returns:
			None: The WebSocket URL for DevTools, or None if it cannot be retrieved.

		Raises:
			CDPEndExceptions: If a CDP-related connection error occurs.
			BaseException: If another unexpected error occurs during URL retrieval.
		"""
		
		try:
			driver = self._webdriver.driver
		
			if driver is None:
				self._websocket_url = None
		
			if driver.caps.get("se:cdp"):
				self._websocket_url = driver.caps.get("se:cdp")
		
			self._websocket_url = driver._get_cdp_details()[1]
		except CDPEndExceptions as error:
			raise error
		except BaseException as error:
			log_exception(error)
			raise error
	
	def _get_devtools_package(self) -> None:
		"""
		Retrieves the DevTools protocol package from the active BiDi connection.

		Returns:
			DevToolsPackage: The DevTools protocol package object, providing access to CDP domains and commands.

		Raises:
			BidiConnectionNotEstablishedError: If the BiDi connection is not active.
		"""
		
		try:
			if self._bidi_connection_object is not None:
				self._devtools_package = DevToolsPackage(package=self._bidi_connection_object.devtools)
			else:
				raise BidiConnectionNotEstablishedError()
		except CDPEndExceptions as error:
			raise error
		except BaseException as error:
			log_exception(error)
			raise error
	
	async def run(self) -> None:
		"""
		Initializes and runs the DevTools manager.

		This method sets up the BiDi connection, starts the Trio nursery, retrieves
		necessary CDP packages and URLs, initializes the main logger, and adds the
		initial target to be monitored.

		Raises:
			CantEnterDevToolsContextError: If the WebDriver is not initialized.
		"""
		
		if self._webdriver.driver is None:
			raise CantEnterDevToolsContextError(reason="Driver is not initialized")
		
		self._bidi_connection = self._webdriver.bidi_connection()
		self._bidi_connection_object = await self._bidi_connection.__aenter__()
		
		self._nursery = trio.open_nursery()
		self._nursery_object = await self._nursery.__aenter__()
		
		self._get_devtools_package()
		self._get_websocket_url()
		
		self._main_logger_cdp_send_channel, self._main_logger_fingerprint_send_channel, self._main_logger = build_main_logger(self._nursery_object, self._logger_settings)
		await self._main_logger.run()
		
		self.exit_event = trio.Event()
		
		self._fingerprint_injection_script = await self._webdriver.sync_to_trio(sync_function=self._fingerprint_settings.generate_js)()
		main_target = (await self._get_all_targets())[0]
		
		await self._add_target(target_event=main_target, is_main_target=True)
		
		self._is_active = True
	
	async def __aenter__(self):
		"""
		Enters the asynchronous context for DevTools event handling.

		This method establishes the BiDi connection, initializes the Trio nursery,
		sets up the main target, and starts listening for DevTools events.

		Raises:
			CantEnterDevToolsContextError: If the WebDriver is not initialized.
			BaseException: If any other unexpected error occurs during context entry.
		"""
		
		await self.run()
	
	async def stop(
			self,
			exc_type: Optional[Type[BaseException]],
			exc_val: Optional[BaseException],
			exc_tb: Optional[TracebackType],
	) -> None:
		"""
		Stops the DevTools manager and cleans up resources.

		This method signals all targets to stop, closes the main logger, cancels the nursery,
		and closes the BiDi connection.

		Args:
			exc_type (Optional[Type[BaseException]]): The exception type if stopping due to an error.
			exc_val (Optional[BaseException]): The exception value if stopping due to an error.
			exc_tb (Optional[TracebackType]): The traceback if stopping due to an error.
		"""
		
		@log_on_error
		async def _stop_main_logger():
			"""Stops the main logger and closes its channels."""
			
			if self._main_logger_cdp_send_channel is not None:
				await self._main_logger_cdp_send_channel.aclose()
				self._main_logger_cdp_send_channel = None
			
			if self._main_logger_fingerprint_send_channel is not None:
				await self._main_logger_fingerprint_send_channel.aclose()
				self._main_logger_fingerprint_send_channel = None
			
			if self._main_logger is not None:
				await self._main_logger.close()
				self._main_logger = None
		
		@log_on_error
		async def _stop_all_targets():
			"""Signals all active targets to stop and waits for their completion."""
			
			for target in self._handling_targets.copy().values():
				try:
					await target.stop()
					await target.stopped_event.wait()
				except (BaseException,):
					pass
			
			self._handling_targets = {}
		
		@log_on_error
		async def _close_nursery():
			"""Asynchronously exits the Trio nursery context manager."""
			
			if self._nursery_object is not None:
				self._nursery_object.cancel_scope.cancel()
				self._nursery_object = None
			
			if self._nursery is not None:
				await self._nursery.__aexit__(exc_type, exc_val, exc_tb)
				self._nursery = None
		
		@log_on_error
		async def _close_bidi_connection():
			"""Asynchronously exits the BiDi connection context manager."""
			
			if self._bidi_connection is not None:
				await self._bidi_connection.__aexit__(exc_type, exc_val, exc_tb)
				self._bidi_connection = None
				self._bidi_connection_object = None
		
		if self._is_active:
			self._is_closing = True
			self.exit_event.set()
		
			await _stop_all_targets()
			await _stop_main_logger()
			await _close_nursery()
			await _close_bidi_connection()
		
			self.exit_event = None
			self._devtools_package = None
			self._websocket_url = None
			self._num_cdp_logs = 0
			self._num_fingerprint_logs = 0
			self._cdp_targets_types_stats = {}
			self._cdp_log_level_stats = {}
			self._fingerprint_categories_stats = {}
			self._fingerprint_log_level_stats = {}
			self._is_active = False
			self._is_closing = False
	
	async def __aexit__(
			self,
			exc_type: Optional[Type[BaseException]],
			exc_val: Optional[BaseException],
			exc_tb: Optional[TracebackType],
	):
		"""
		Asynchronously exits the DevTools event handling context.

		This method is called when exiting an `async with` block with a DevTools instance.
		It ensures that all event listeners are cancelled, the Trio nursery is closed,
		and the BiDi connection is properly shut down. Cleanup attempts are made even if
		an exception occurred within the `async with` block.

		Args:
			exc_type (Optional[Type[BaseException]]): The exception type, if any, that caused the context to be exited.
			exc_val (Optional[BaseException]): The exception value, if any.
			exc_tb (Optional[TracebackType]): The exception traceback, if any.
		"""
		
		await self.stop(exc_type=exc_type, exc_val=exc_val, exc_tb=exc_tb)
