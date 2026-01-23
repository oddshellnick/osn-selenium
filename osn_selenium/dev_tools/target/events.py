import trio
from typing import List, TYPE_CHECKING
from osn_selenium.exceptions.devtools import CDPEndExceptions
from osn_selenium.dev_tools.target.logging import LoggingMixin


__all__ = ["EventHandlersMixin"]

if TYPE_CHECKING:
	from osn_selenium.dev_tools.domains.abstract import (AbstractDomainSettings, AbstractEventSettings)


class EventHandlersMixin(LoggingMixin):
	"""
	Mixin for handling generic DevTools domain events.
	"""
	
	async def _run_event_handler(
			self,
			domain_handler_ready_event: trio.Event,
			event_config: "AbstractEventSettings"
	):
		"""
		Runs a specific event handler listener loop.

		Listens for events of the type specified in `event_config` and invokes the configured `handle_function`.

		Args:
			domain_handler_ready_event (trio.Event): Event to signal that this specific handler is ready.
			event_config (AbstractEventSettings): Configuration for the specific event.

		Raises:
			CDPEndExceptions: If connection issues occur.
			BaseException: If initialization fails.
		"""
		
		await self.log_cdp_step(message=f"Event handler '{event_config.class_to_use_path}' starting.")
		
		try:
			receiver_channel: trio.MemoryReceiveChannel = self.cdp_session.listen(
					self.devtools_package.get(event_config.class_to_use_path),
					buffer_size=event_config.listen_buffer_size
			)
			channel_stopped_event = trio.Event()
		
			self._events_receive_channels[event_config.class_to_use_path] = (receiver_channel, channel_stopped_event)
		
			domain_handler_ready_event.set()
			handler = event_config.handle_function
		except CDPEndExceptions as error:
			raise error
		except BaseException as error:
			await self.log_cdp_error(error=error)
			raise error
		
		await self.log_cdp_step(message=f"Event handler '{event_config.class_to_use_path}' started.")
		
		keep_alive = True
		while keep_alive:
			try:
				event = await receiver_channel.receive()
				self._nursery_object.start_soon(handler, self, event_config, event)
			except* CDPEndExceptions:
				keep_alive = False
			except* BaseException as error:
				await self.log_cdp_error(error=error)
				keep_alive = False
		
		channel_stopped_event.set()
	
	async def _run_events_handlers(
			self,
			events_ready_event: trio.Event,
			domain_config: "AbstractDomainSettings"
	):
		"""
		Sets up and runs event handlers for a specific domain.

		Iterates through the domain configuration and starts a separate task for each configured event handler.

		Args:
			events_ready_event (trio.Event): Event to signal when all handlers for the domain are ready.
			domain_config (AbstractDomainSettings): Configuration for the domain events.

		Raises:
			CDPEndExceptions: If connection issues occur.
			BaseException: If other errors occur during setup.
		"""
		
		await self.log_cdp_step(
				message=f"Domain '{domain_config.name}' events handlers setup started."
		)
		
		try:
			events_handlers_ready_events: List[trio.Event] = []
		
			for event_name, event_config in domain_config.handlers.model_dump(exclude_none=True).items():
				if event_config is not None:
					event_handler_ready_event = trio.Event()
					events_handlers_ready_events.append(event_handler_ready_event)
		
					self._nursery_object.start_soon(
							self._run_event_handler,
							event_handler_ready_event,
							getattr(domain_config.handlers, event_name)
					)
		
			for event_handler_ready_event in events_handlers_ready_events:
				await event_handler_ready_event.wait()
		
			events_ready_event.set()
		
			await self.log_cdp_step(
					message=f"Domain '{domain_config.name}' events handlers setup complete."
			)
		except* CDPEndExceptions as error:
			raise error
		except* BaseException as error:
			await self.log_cdp_error(error=error)
			raise error
