import trio
from typing import Tuple
from osn_selenium.exceptions.devtools import CDPEndExceptions
from osn_selenium.dev_tools.target.logging import LoggingMixin
from osn_selenium.dev_tools._functions import execute_cdp_command
from osn_selenium.dev_tools._validators import (
	validate_target_event
)


__all__ = ["DiscoveryMixin"]


class DiscoveryMixin(LoggingMixin):
	"""
	Mixin for discovering and attaching to new DevTools targets.
	"""
	
	async def _run_new_targets_listener(self, new_targets_listener_ready_event: trio.Event):
		"""
		Listens for `TargetCreated` and `TargetInfoChanged` events to manage new targets.

		Attaches to valid new targets and adds them to the management system.

		Args:
			new_targets_listener_ready_event (trio.Event): Event to signal that the listener is successfully started.

		Raises:
			CDPEndExceptions: If connection issues occur during initialization.
			BaseException: If other errors occur during initialization.
		"""
		
		await self.log_cdp_step(message="New Targets listener starting.")
		
		try:
			self._new_target_receive_channel: Tuple[trio.MemoryReceiveChannel, trio.Event] = (
					self.cdp_session.listen(
							self.devtools_package.get("target.TargetCreated"),
							# self.devtools_package.get("target.AttachedToTarget"),
							self.devtools_package.get("target.TargetInfoChanged"),
							buffer_size=self._new_targets_buffer_size
					),
					trio.Event()
			)
			new_targets_listener_ready_event.set()
		except CDPEndExceptions as error:
			raise error
		except BaseException as error:
			await self.log_cdp_error(error=error)
			raise error
		
		await self.log_cdp_step(message="New Targets listener started.")
		
		keep_alive = True
		while keep_alive:
			try:
				event = await self._new_target_receive_channel[0].receive()
		
				if validate_target_event(event=event, filter_=self._new_targets_events_filters):
					await execute_cdp_command(
							self=self,
							error_mode="log",
							function=self.devtools_package.get("target.attach_to_target"),
							target_id=event.target_info.target_id,
							flatten=True
					)
		
					self._nursery_object.start_soon(self._add_target_func, event)
			except* CDPEndExceptions:
				keep_alive = False
			except* BaseException as error:
				await self.log_cdp_error(error=error)
				keep_alive = False
		
		self._new_target_receive_channel[1].set()
	
	async def _setup_new_targets_attaching(self):
		"""
		Configures the target to discover and auto-attach to new targets.

		Executes CDP commands to set discovery mode and auto-attach behavior
		based on the configured filters.

		Raises:
			CDPEndExceptions: If the connection closes during setup.
			BaseException: If other errors occur.
		"""
		
		try:
			target_filter = self.devtools_package.get("target.TargetFilter")(self._new_targets_filter_list) if self._new_targets_filter_list is not None else None
		
			await execute_cdp_command(
					self=self,
					error_mode="log",
					function=self.devtools_package.get("target.set_discover_targets"),
					discover=True,
					filter_=target_filter,
			)
			await execute_cdp_command(
					self=self,
					error_mode="log",
					function=self.devtools_package.get("target.set_auto_attach"),
					auto_attach=True,
					wait_for_debugger_on_start=True,
					flatten=True,
					filter_=target_filter,
			)
		except CDPEndExceptions as error:
			raise error
		except BaseException as error:
			await self.log_cdp_error(error=error)
			raise error
