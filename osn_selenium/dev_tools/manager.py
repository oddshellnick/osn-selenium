from __future__ import annotations

import trio
from pydantic import Field
from types import TracebackType
from collections.abc import Sequence
from osn_selenium.types import DictModel
from contextlib import (
	AbstractAsyncContextManager
)
from osn_selenium.dev_tools.target import DevToolsTarget
from selenium.webdriver.remote.bidi_connection import BidiConnection
from osn_selenium.dev_tools._types import (
	devtools_background_func_type
)
from typing import (
	Any,
	Dict,
	List,
	Optional,
	TYPE_CHECKING,
	Type,
	Union
)
from osn_selenium.dev_tools.domains import (
	DomainsSettings,
	domains_classes_type,
	domains_type
)
from osn_selenium.dev_tools.errors import (
	BidiConnectionNotEstablishedError,
	CantEnterDevToolsContextError,
	cdp_end_exceptions
)
from osn_selenium.dev_tools.logger import (
	LogEntry,
	LogLevelStats,
	LoggerSettings,
	MainLogEntry,
	MainLogger,
	TargetTypeStats,
	build_main_logger
)
from osn_selenium.dev_tools.utils import (
	DevToolsPackage,
	TargetData,
	TargetFilter,
	_prepare_log_dir,
	log_exception,
	log_on_error,
	warn_if_active
)


if TYPE_CHECKING:
	from osn_selenium.webdrivers.trio_threads.base import WebDriver


class DevToolsSettings(DictModel):
	"""
	Settings for configuring the DevTools manager.

	Attributes:
		new_targets_filter (Optional[Sequence[TargetFilter]]): A sequence of `TargetFilter` objects
			to control which new browser targets (e.g., tabs, iframes) DevTools should discover and attach to.
			Defaults to None, meaning all targets are considered.
		new_targets_buffer_size (int): The buffer size for the Trio memory channel
			used to receive new target events. A larger buffer can prevent `trio.WouldBlock`
			errors under high event load. Defaults to 100.
		target_background_task (Optional[devtools_background_func_type]): An optional asynchronous function
			that will be run as a background task for each attached DevTools target. This can be used
			for custom per-target logic. Defaults to None.
		logger_settings (Optional[LoggerSettings]): Configuration settings for the internal logging system.
			If None, default logging settings will be used (no file logging by default).
			Defaults to None.
	"""
	
	new_targets_filter: Optional[Sequence[TargetFilter]] = None
	new_targets_buffer_size: int = 100
	target_background_task: devtools_background_func_type = None
	logger_settings: Optional[LoggerSettings] = Field(default_factory=LoggerSettings)
	domains_settings: Optional[DomainsSettings] = Field(default_factory=DomainsSettings)


class DevTools:
	"""
	Base class for handling DevTools functionalities in Selenium WebDriver.

	Provides an interface to interact with Chrome DevTools Protocol (CDP)
	for advanced browser control and monitoring. This class supports event handling
	and allows for dynamic modifications of browser behavior, such as network request interception,
	by using an asynchronous context manager.

	Attributes:
		_webdriver ("BrowserWebDriver"): The parent WebDriver instance associated with this DevTools instance.
		_new_targets_filter (Optional[List[Dict[str, Any]]]): Processed filters for new targets.
		_new_targets_buffer_size (int): Buffer size for new target events.
		_target_background_task (Optional[devtools_background_func_type]): Optional background task for targets.
		_logger_settings (LoggerSettings): Logging configuration for the entire DevTools manager.
		_bidi_connection (Optional[AbstractAsyncContextManager[BidiConnection, Any]]): Asynchronous context manager for the BiDi connection.
		_bidi_connection_object (Optional[BidiConnection]): The BiDi connection object when active.
		_nursery (Optional[AbstractAsyncContextManager[trio.Nursery, object]]): Asynchronous context manager for the Trio nursery.
		_nursery_object (Optional[trio.Nursery]): The Trio nursery object when active, managing concurrent tasks.
		_domains_settings (DomainsSettings): Settings for configuring DevTools domain handlers.
		_handling_targets (Dict[str, DevToolsTarget]): Dictionary of target IDs currently being handled by event listeners.
		targets_lock (trio.Lock): A lock used for synchronizing access to shared resources, like the List of handled targets.
		exit_event (Optional[trio.Event]): Trio Event to signal exiting of DevTools event handling.
		_is_active (bool): Flag indicating if the DevTools event handler is currently active.
		_is_closing (bool): Flag indicating if the DevTools manager is in the process of closing.
		_num_logs (int): Total count of all log entries across all targets.
		_targets_types_stats (Dict[str, TargetTypeStats]): Statistics for each target type.
		_log_level_stats (Dict[str, LogLevelStats]): Overall statistics for each log level.
		_main_logger (Optional[MainLogger]): The main logger instance.
		_main_logger_send_channel (Optional[trio.MemorySendChannel[MainLogEntry]]): Send channel for the main logger.

	EXAMPLES
	________
	>>> from osn_selenium.webdrivers.trio_threads.chrome import ChromeWebDriver
	... from osn_selenium.dev_tools.domains import DomainsSettings
	...
	... async def main():
	...	 driver = ChromeWebDriver("path/to/chromedriver")
	...	 driver.dev_tools.set_domains_handlers(DomainsSettings(...))
	...
	...		# Configure domain handlers here.
	...		async with driver.dev_tools:
	...			# DevTools event handling is active within this block.
	...			await driver.get("https://example.com")
	...			# DevTools event handling is deactivated after exiting the block.
	"""
	
	def __init__(
			self,
			parent_webdriver: "WebDriver",
			devtools_settings: Optional[DevToolsSettings] = None
	):
		"""
		Initializes the DevTools manager.

		Args:
			parent_webdriver ("WebDriver"): The WebDriver instance to which this DevTools manager is attached.
			devtools_settings (Optional[DevToolsSettings]): Configuration settings for DevTools.
				If None, default settings will be used.
		"""
		
		if devtools_settings is None:
			devtools_settings = DevToolsSettings()
		
		self._webdriver = parent_webdriver
		
		self._new_targets_filter = [
			filter_.model_dump(exclude_none=True, by_alias=True)
			for filter_ in devtools_settings.new_targets_filter
		] if devtools_settings.new_targets_filter is not None else None
		
		self._new_targets_buffer_size = devtools_settings.new_targets_buffer_size
		self._target_background_task = devtools_settings.target_background_task
		self._logger_settings = devtools_settings.logger_settings
		self._domains_settings = devtools_settings.domains_settings
		self._bidi_connection: Optional[AbstractAsyncContextManager[BidiConnection, Any]] = None
		self._bidi_connection_object: Optional[BidiConnection] = None
		self._nursery: Optional[AbstractAsyncContextManager[trio.Nursery, Optional[bool]]] = None
		self._nursery_object: Optional[trio.Nursery] = None
		self._handling_targets: Dict[str, DevToolsTarget] = {}
		self.targets_lock = trio.Lock()
		self._websocket_url: Optional[str] = None
		self.exit_event: Optional[trio.Event] = None
		self._is_active = False
		self._is_closing = False
		self._num_logs = 0
		self._targets_types_stats: Dict[str, TargetTypeStats] = {}
		self._log_level_stats: Dict[str, LogLevelStats] = {}
		self._main_logger: Optional[MainLogger] = None
		self._main_logger_send_channel: Optional[trio.MemorySendChannel[MainLogEntry]] = None
		
		_prepare_log_dir(devtools_settings.logger_settings)
	
	async def _main_log(self):
		"""
		Sends updated overall logging statistics to the main logger.

		This method constructs a `MainLogEntry` with current statistics and
		sends it to the `_main_logger_send_channel`. If the channel buffer is full,
		the log is dropped silently.
		"""
		
		try:
			if self._main_logger_send_channel is not None and self._main_logger is not None:
				log_entry = MainLogEntry(
						num_channels=len(self._handling_targets),
						targets_types_stats=self._targets_types_stats,
						num_logs=self._num_logs,
						log_level_stats=self._log_level_stats,
						channels_stats=list(
								map(
										lambda target: target.log_stats,
										filter(
												lambda target: target.target_type_log_accepted,
												self._handling_targets.values()
										)
								)
						),
				)
				self._main_logger_send_channel.send_nowait(log_entry)
		except (trio.WouldBlock, trio.BrokenResourceError):
			pass
		except cdp_end_exceptions as error:
			raise error
		except BaseException as error:
			log_exception(error)
			raise error
	
	async def _add_log(self, log_entry: LogEntry):
		"""
		Updates internal logging statistics based on a new log entry.

		This method increments total log counts and updates per-channel and per-level statistics.
		It also triggers an update to the main logger.

		Args:
			log_entry (LogEntry): The log entry to use for updating statistics.

		Raises:
			BaseException: Catches and logs any unexpected errors during the log aggregation process.
		"""
		
		try:
			self._num_logs += 1
		
			if log_entry.level not in self._log_level_stats:
				self._log_level_stats[log_entry.level] = LogLevelStats(num_logs=1, last_log_time=log_entry.timestamp)
			else:
				self._log_level_stats[log_entry.level].num_logs += 1
				self._log_level_stats[log_entry.level].last_log_time = log_entry.timestamp
		
			await self._main_log()
		except cdp_end_exceptions:
			pass
		except BaseException as error:
			log_exception(error)
			raise error
	
	async def _remove_target(self, target: DevToolsTarget) -> Optional[bool]:
		"""
		Removes a target ID from the List of currently handled targets.

		This method also triggers the removal of the target's specific logger channel
		and updates overall logging statistics.

		Args:
			target (DevToolsTarget): The target instance to remove.

		Returns:
			Optional[bool]: True if the target ID was successfully removed, False if it was not found.
							Returns None if an exception occurs.
		"""
		
		try:
			async with self.targets_lock:
				if target.target_id in self._handling_targets:
					self._targets_types_stats[target.type_].num_targets -= 1
		
					target = self._handling_targets.pop(target.target_id)
					await target.log_step(message=f"Target '{target.target_id}' removed.")
					await target.stop()
		
					await self._main_log()
		
					return True
				else:
					return False
		except cdp_end_exceptions:
			pass
		except BaseException as error:
			log_exception(error)
	
	@property
	def _devtools_package(self) -> DevToolsPackage:
		"""
		Retrieves the DevTools protocol package from the active BiDi connection.

		Returns:
			DevToolsPackage: The DevTools protocol package object, providing access to CDP domains and commands.

		Raises:
			BidiConnectionNotEstablishedError: If the BiDi connection is not active.
		"""
		
		try:
			if self._bidi_connection_object is not None:
				return DevToolsPackage(package=self._bidi_connection_object.devtools)
			else:
				raise BidiConnectionNotEstablishedError()
		except cdp_end_exceptions as error:
			raise error
		except BaseException as error:
			log_exception(error)
			raise error
	
	async def _add_target(self, target_event: Any) -> Optional[bool]:
		"""
		Adds a new browser target to the manager based on a target event.

		This method processes events like `TargetCreated` or `AttachedToTarget`
		to initialize and manage new `DevToolsTarget` instances. It ensures
		that targets are not added if the manager is closing or if they already exist.

		Args:
			target_event (Any): The event object containing target information.
								 Expected to have a `target_info` attribute or be the target info itself.

		Returns:
			Optional[bool]: True if a new target was successfully added and started,
							False if the target already existed or was filtered,
							or None if an error occurred.

		Raises:
			BaseException: Catches and logs any unexpected errors during target addition.
		"""
		
		try:
			if hasattr(target_event, "target_info"):
				target_info = target_event.target_info
			else:
				target_info = target_event
		
			async with self.targets_lock:
				target_id = target_info.target_id
		
				if self._is_closing:
					return False
		
				if target_id not in self._handling_targets:
					self._handling_targets[target_id] = DevToolsTarget(
							target_data=TargetData(
									target_id=target_id,
									type_=target_info.type_,
									title=target_info.title,
									url=target_info.url,
									attached=target_info.attached,
									can_access_opener=target_info.can_access_opener,
									opener_id=target_info.opener_id,
									opener_frame_id=target_info.opener_frame_id,
									browser_context_id=target_info.browser_context_id,
									subtype=target_info.subtype,
							),
							logger_settings=self._logger_settings,
							devtools_package=self._devtools_package,
							websocket_url=self._websocket_url,
							new_targets_filter=self._new_targets_filter,
							new_targets_buffer_size=self._new_targets_buffer_size,
							domains=self._domains_settings,
							nursery=self._nursery_object,
							exit_event=self.exit_event,
							target_background_task=self._target_background_task,
							add_target_func=self._add_target,
							remove_target_func=self._remove_target,
							add_log_func=self._add_log,
					)
		
					if target_info.type_ not in self._targets_types_stats:
						self._targets_types_stats[target_info.type_] = TargetTypeStats(num_targets=1)
					else:
						self._targets_types_stats[target_info.type_].num_targets += 1
		
					await self._main_log()
		
					self._nursery_object.start_soon(self._handling_targets[target_id].run,)
		
					return True
				else:
					self._handling_targets[target_id].type_ = target_info.type_
					self._handling_targets[target_id].title = target_info.title
					self._handling_targets[target_id].url = target_info.url
					self._handling_targets[target_id].attached = target_info.attached
					self._handling_targets[target_id].can_access_opener = target_info.can_access_opener
					self._handling_targets[target_id].opener_id = target_info.opener_id
					self._handling_targets[target_id].opener_frame_id = target_info.opener_frame_id
					self._handling_targets[target_id].browser_context_id = target_info.browser_context_id
					self._handling_targets[target_id].subtype = target_info.subtype
		
					return False
		except* cdp_end_exceptions:
			pass
		except* BaseException as error:
			log_exception(error)
			raise error
	
	async def _get_all_targets(self) -> List[Any]:
		"""
		Retrieves a List of all currently active browser targets.

		Returns:
			List[Any]: A List of target objects, each containing information like target ID, type, and URL.

		Raises:
			BidiConnectionNotEstablishedError: If the BiDi connection is not active.
		"""
		
		try:
			if self._bidi_connection_object is not None:
				targets_filter = self._devtools_package.get("target.TargetFilter")(
						[
							{"exclude": False, "type": "page"},
							{"exclude": False, "type": "tab"},
							{"exclude": True}
						]
				)
		
				return await self._bidi_connection_object.session.execute(self._devtools_package.get("target.get_targets")(targets_filter))
			else:
				raise BidiConnectionNotEstablishedError()
		except cdp_end_exceptions as error:
			raise error
		except BaseException as error:
			log_exception(error)
			raise error
	
	def _get_websocket_url(self) -> Optional[str]:
		"""
		Retrieves the WebSocket URL for DevTools from the WebDriver.

		This method attempts to get the WebSocket URL from the WebDriver capabilities or by directly querying the CDP details.
		The WebSocket URL is necessary to establish a connection to the browser's DevTools.

		Returns:
			Optional[str]: The WebSocket URL for DevTools, or None if it cannot be retrieved.

		Raises:
			cdp_end_exceptions: If a CDP-related connection error occurs.
			BaseException: If another unexpected error occurs during URL retrieval.
		"""
		
		try:
			driver = self._webdriver.driver
		
			if driver is None:
				self._websocket_url = None
		
			if driver.caps.get("se:cdp"):
				self._websocket_url = driver.caps.get("se:cdp")
		
			self._websocket_url = driver._get_cdp_details()[1]
		except cdp_end_exceptions as error:
			raise error
		except BaseException as error:
			log_exception(error)
			raise error
	
	async def __aenter__(self):
		"""
		Enters the asynchronous context for DevTools event handling.

		This method establishes the BiDi connection, initializes the Trio nursery,
		sets up the main target, and starts listening for DevTools events.

		Raises:
			CantEnterDevToolsContextError: If the WebDriver is not initialized.
			BaseException: If any other unexpected error occurs during context entry.
		"""
		
		if self._webdriver.driver is None:
			raise CantEnterDevToolsContextError("Driver is not initialized")
		
		self._bidi_connection: AbstractAsyncContextManager[BidiConnection, Any] = self._webdriver.driver.bidi_connection()
		self._bidi_connection_object = await self._bidi_connection.__aenter__()
		
		self._nursery = trio.open_nursery()
		self._nursery_object = await self._nursery.__aenter__()
		
		self._get_websocket_url()
		
		self._main_logger_send_channel, self._main_logger = build_main_logger(self._nursery_object, self._logger_settings)
		await self._main_logger.run()
		
		self.exit_event = trio.Event()
		
		main_target = (await self._get_all_targets())[0]
		await self._add_target(main_target)
		
		self._is_active = True
	
	async def __aexit__(
			self,
			exc_type: Optional[Type[BaseException]],
			exc_val: Optional[BaseException],
			exc_tb: Optional[TracebackType]
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
		
		@log_on_error
		async def _stop_main_logger():
			"""Stops the main logger and closes its channels."""
			
			if self._main_logger_send_channel is not None:
				await self._main_logger_send_channel.aclose()
				self._main_logger_send_channel = None
			
			if self._main_logger is not None:
				await self._main_logger.close()
				self._main_logger = None
		
		@log_on_error
		async def _stop_all_targets():
			"""Signals all active targets to stop and waits for their completion."""
			
			for target in self._handling_targets.copy().values():
				await target.stop()
				await target.stopped_event.wait()
			
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
		
			await _stop_main_logger()
			await _stop_all_targets()
			await _close_nursery()
			await _close_bidi_connection()
		
			self.exit_event = None
			self._websocket_url = None
			self._num_logs = 0
			self._targets_types_stats = {}
			self._log_level_stats = {}
			self._is_active = False
			self._is_closing = False
	
	@property
	def is_active(self) -> bool:
		"""
		Checks if DevTools is currently active.

		Returns:
			bool: True if DevTools event handler context manager is active, False otherwise.
		"""
		
		return self._is_active
	
	@warn_if_active
	def _remove_handler_settings(self, domain: domains_type):
		"""
		Removes the settings for a specific domain.

		This is an internal method intended to be used only when the DevTools context is not active.
		It uses the `@warn_if_active` decorator to log a warning if called incorrectly.

		Args:
			domain (domains_type): The name of the domain to remove settings for.
		"""
		
		if self._domains_settings is not None:
			self._domains_settings.pop(domain, None)
	
	def remove_domains_handlers(self, domains: Union[domains_type, Sequence[domains_type]]):
		"""
		Removes handler settings for one or more DevTools domains.

		This method can be called with a single domain name or a sequence of domain names.
		It should only be called when the DevTools context is not active.

		Args:
			domains (Union[domains_type, Sequence[domains_type]]): A single domain name as a string,
				or a sequence of domain names to be removed.

		Raises:
			TypeError: If the `domains` argument is not a string or a sequence of strings.
		"""
		
		if isinstance(domains, Sequence) and all(isinstance(domain, str) for domain in domains):
			for domain in domains:
				self._remove_handler_settings(domain)
		elif isinstance(domains, str):
			self._remove_handler_settings(domains)
		else:
			raise TypeError(f"domains must be a str or a sequence of str, got {type(domains)}.")
	
	@warn_if_active
	def _set_handler_settings(self, domain: domains_type, settings: domains_classes_type):
		"""
		Sets the handler settings for a specific domain.

		This is an internal method intended to be used only when the DevTools context is not active.
		It uses the `@warn_if_active` decorator to log a warning if called incorrectly.

		Args:
			domain (domains_type): The name of the domain to configure.
			settings (domains_classes_type): The configuration settings for the domain.
		"""
		
		setattr(self._domains_settings, domain, settings)
	
	def set_domains_handlers(self, settings: DomainsSettings):
		"""
		Sets handler settings for multiple domains from a DomainsSettings object.

		This method iterates through the provided settings and applies them to the corresponding domains.
		It should only be called when the DevTools context is not active.

		Args:
			settings (DomainsSettings): An object containing the configuration for one or more domains.
		"""
		
		for domain_name, domain_settings in settings.model_dump(exclude_none=True).items():
			self._set_handler_settings(domain_name, domain_settings)
	
	@property
	def websocket_url(self) -> Optional[str]:
		"""
		Gets the WebSocket URL for the DevTools session.

		This URL is used to establish a direct Chrome DevTools Protocol (CDP) connection
		to the browser, enabling low-level control and event listening.

		Returns:
			Optional[str]: The WebSocket URL, or None if it has not been retrieved yet.
		"""
		
		return self._websocket_url


DevToolsSettings.model_rebuild()
