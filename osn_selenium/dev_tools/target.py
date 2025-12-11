import trio
import inspect
import warnings
from datetime import datetime
from osn_selenium.dev_tools.errors import cdp_end_exceptions
from selenium.webdriver.common.bidi.cdp import (
	BrowserError,
	CdpSession,
	open_cdp
)
from osn_selenium.dev_tools._types import (
	LogLevelsType,
	devtools_background_func_type
)
from typing import (
	Any,
	Awaitable,
	Callable,
	Dict,
	List,
	Optional,
	TYPE_CHECKING,
	Tuple
)
from osn_selenium.dev_tools.logger import (
	LogEntry,
	LoggerChannelStats,
	LoggerSettings,
	TargetLogger,
	build_target_logger
)
from osn_selenium.dev_tools.utils import (
	DevToolsPackage,
	TargetData,
	_background_task_decorator,
	_validate_type_filter,
	execute_cdp_command,
	extract_exception_trace,
	log_exception,
	wait_one
)


if TYPE_CHECKING:
	from osn_selenium.dev_tools.domains import DomainsSettings
	from osn_selenium.dev_tools.domains.abstract import AbstractDomainSettings, AbstractEventSettings


class DevToolsTarget:
	"""
	Manages the DevTools Protocol session and event handling for a specific browser target.

	Each `DevToolsTarget` instance represents a single CDP target (e.g., a browser tab,
	an iframe, or a service worker) and handles its dedicated CDP session, event listeners,
	and associated logging.

	Attributes:
		target_data (TargetData): Data describing the browser target.
		_logger_settings (LoggerSettings): Logging configuration for this target.
		devtools_package (Any): The DevTools protocol package (e.g., `selenium.webdriver.common.bidi.cdp.devtools`).
		websocket_url (Optional[str]): The WebSocket URL for establishing the CDP connection.
		_new_targets_filter (Optional[List[Dict[str, Any]]]): Filter settings for discovering new targets.
		_new_targets_buffer_size (int): Buffer size for new target events.
		_domains (DomainsSettings): Configuration for DevTools domains and their event handlers.
		_nursery_object (trio.Nursery): The Trio nursery for spawning concurrent tasks.
		exit_event (trio.Event): An event signaling that the main DevTools context is exiting.
		_target_type_log_accepted (bool): Indicates if this target's type is accepted by the logger filter.
		_target_background_task (Optional[devtools_background_func_type]): An optional background task to run for this target.
		_add_target_func (Callable[[Any], Awaitable[bool]]): Callback function to add new targets to the manager.
		_remove_target_func (Callable[["DevToolsTarget"], Awaitable[bool]]): Callback function to remove targets from the manager.
		_add_log_func (Callable[[LogEntry], Awaitable[None]]): Callback function to add log entries to the main logger.
		started_event (trio.Event): An event set when the target's `run` method has started.
		about_to_stop_event (trio.Event): An event set when the target is signaled to stop.
		background_task_ended (Optional[trio.Event]): An event set when the target's background task completes.
		stopped_event (trio.Event): An event set when the target's `run` method has fully stopped.
		_log_stats (LoggerChannelStats): Statistics specific to this target's logging.
		_logger_send_channel (Optional[trio.MemorySendChannel[LogEntry]]): Send channel for this target's logger.
		_logger (Optional[TargetLogger]): The logger instance for this specific target.
		_cdp_session (Optional[CdpSession]): The active CDP session for this target.
		_new_target_receive_channel (Optional[tuple[trio.MemoryReceiveChannel[Any], trio.Event]]): Channel and event for new target events.
		_events_receive_channels (Dict[str, tuple[trio.MemoryReceiveChannel[Any], trio.Event]]): Channels and events for domain-specific events.
	"""
	
	def __init__(
			self,
			target_data: TargetData,
			logger_settings: LoggerSettings,
			devtools_package: DevToolsPackage,
			websocket_url: Optional[str],
			new_targets_filter: List[Dict[str, Any]],
			new_targets_buffer_size: int,
			domains: "DomainsSettings",
			nursery: trio.Nursery,
			exit_event: trio.Event,
			target_background_task: Optional[devtools_background_func_type],
			add_target_func: Callable[[Any], Awaitable[bool]],
			remove_target_func: Callable[["DevToolsTarget"], Awaitable[bool]],
			add_log_func: Callable[[LogEntry], Awaitable[None]],
	):
		"""
		Initializes a DevToolsTarget instance.

		Args:
			target_data (TargetData): Initial data for this target.
			logger_settings (LoggerSettings): Logging configuration.
			devtools_package (DevToolsPackage): The DevTools protocol package.
			websocket_url (Optional[str]): WebSocket URL for CDP connection.
			new_targets_filter (Optional[List[Dict[str, Any]]]): Filters for new targets.
			new_targets_buffer_size (int): Buffer size for new target events.
			domains (DomainsSettings): Configured DevTools domains.
			nursery (trio.Nursery): The Trio nursery for tasks.
			exit_event (trio.Event): Event to signal global exit.
			target_background_task (Optional[devtools_background_func_type]): Optional background task.
			add_target_func (Callable[[Any], Awaitable[Optional[bool]]]): Function to add new targets.
			remove_target_func (Callable[["DevToolsTarget"], Awaitable[Optional[bool]]]): Function to remove targets.
			add_log_func (Callable[[LogEntry], Awaitable[None]]): Function to add logs to main logger.
		"""
		
		self.target_data = target_data
		self._logger_settings = logger_settings
		self.devtools_package = devtools_package
		self.websocket_url = websocket_url
		self._new_targets_filter = new_targets_filter
		self._new_targets_buffer_size = new_targets_buffer_size
		self._domains = domains
		self._nursery_object = nursery
		self.exit_event = exit_event
		
		self._target_type_log_accepted = _validate_type_filter(
				self.type_,
				self._logger_settings.target_type_filter_mode,
				self._logger_settings.target_type_filter
		)
		
		self._target_background_task = target_background_task
		self._add_target_func = add_target_func
		self._remove_target_func = remove_target_func
		self._add_log_func = add_log_func
		self.started_event = trio.Event()
		self.about_to_stop_event = trio.Event()
		self.background_task_ended: Optional[trio.Event] = None
		self.stopped_event = trio.Event()
		
		self._log_stats = LoggerChannelStats(
				target_id=target_data.target_id,
				title=target_data.title,
				url=target_data.url,
				num_logs=0,
				last_log_time=datetime.now(),
				log_level_stats={}
		)
		
		self._logger_send_channel: Optional[trio.MemorySendChannel] = None
		self._logger: Optional[TargetLogger] = None
		self._cdp_session: Optional[CdpSession] = None
		self._new_target_receive_channel: Optional[Tuple[trio.MemoryReceiveChannel, trio.Event]] = None
		self._detached_receive_channel: Optional[trio.MemoryReceiveChannel] = None
		self._events_receive_channels: Dict[str, Tuple[trio.MemoryReceiveChannel, trio.Event]] = {}
	
	@property
	def attached(self) -> Optional[bool]:
		"""
		Gets whether the DevTools session is currently attached to this target.

		Returns:
			Optional[bool]: True if attached, False if not, or None if status is unknown.
		"""
		
		return self.target_data.attached
	
	@attached.setter
	def attached(self, value: Optional[bool]) -> None:
		"""
		Sets whether the DevTools session is currently attached to this target.

		Args:
			value (Optional[bool]): The new attached status (True, False, or None).
		"""
		
		self.target_data.attached = value
	
	@property
	def browser_context_id(self) -> Optional[str]:
		"""
		Gets the ID of the browser context this target belongs to.

		Browser contexts are isolated environments, often used for incognito mode
		or separate user profiles.

		Returns:
			Optional[str]: The ID of the browser context, or None if not associated
				with a specific context.
		"""
		
		return self.target_data.browser_context_id
	
	@browser_context_id.setter
	def browser_context_id(self, value: Optional[str]) -> None:
		"""
		Sets the ID of the browser context this target belongs to.

		Args:
			value (Optional[str]): The new browser context ID string, or None to clear it.
		"""
		
		self.target_data.browser_context_id = value
	
	@property
	def can_access_opener(self) -> Optional[bool]:
		"""
		Gets whether the target can access its opener.

		This property indicates if the target has permission to interact with
		the target that opened it.

		Returns:
			Optional[bool]: True if it can access the opener, False if not,
				or None if the status is unknown.
		"""
		
		return self.target_data.can_access_opener
	
	@can_access_opener.setter
	def can_access_opener(self, value: Optional[bool]) -> None:
		"""
		Sets whether the target can access its opener.

		Args:
			value (Optional[bool]): The new status for opener access (True, False, or None).
		"""
		
		self.target_data.can_access_opener = value
	
	@property
	def cdp_session(self) -> CdpSession:
		"""
		Gets the active Chrome DevTools Protocol (CDP) session for this target.

		This session object is the primary interface for sending CDP commands
		and receiving events specific to this target.

		Returns:
			CdpSession: The CDP session object associated with this target.
		"""
		
		return self._cdp_session
	
	@property
	def log_stats(self) -> LoggerChannelStats:
		"""
		Gets the logging statistics for this specific target channel.

		This provides aggregated data such as total log count, last log time,
		and per-level log counts for this target.

		Returns:
			LoggerChannelStats: An object containing the logging statistics for this target.
		"""
		
		return self._log_stats
	
	@property
	def opener_frame_id(self) -> Optional[str]:
		"""
		Gets the frame ID of the target that opened this one.

		Returns:
			Optional[str]: The frame ID of the opener, or None if not applicable or known.
		"""
		
		return self.target_data.opener_frame_id
	
	@opener_frame_id.setter
	def opener_frame_id(self, value: Optional[str]) -> None:
		"""
		Sets the frame ID of the target that opened this one.

		Args:
			value (Optional[str]): The new opener frame ID string, or None to clear it.
		"""
		
		self.target_data.opener_frame_id = value
	
	@property
	def opener_id(self) -> Optional[str]:
		"""
		Gets the ID of the target that opened this one.

		Returns:
			Optional[str]: The ID of the opener target, or None if not applicable or known.
		"""
		
		return self.target_data.opener_id
	
	@opener_id.setter
	def opener_id(self, value: Optional[str]) -> None:
		"""
		Sets the ID of the target that opened this one.

		Args:
			value (Optional[str]): The new opener target ID string, or None to clear it.
		"""
		
		self.target_data.opener_id = value
	
	async def stop(self):
		"""
		Signals the target to begin its shutdown process.

		This sets the `about_to_stop_event`, which is used to gracefully
		terminate ongoing tasks within the target's `run` method.
		"""
		
		self.about_to_stop_event.set()
	
	async def _close_instances(self):
		"""
		Closes all associated instances and channels for this target.

		This includes the new target receive channel, the logger send channel,
		the target logger itself, and all event receive channels. It also waits
		for the background task to end if one was started.
		"""

		if self._new_target_receive_channel is not None:
			await self._new_target_receive_channel[0].aclose()
			await self._new_target_receive_channel[1].wait()
		
			self._new_target_receive_channel = None

		if self._detached_receive_channel is not None:
			await self._detached_receive_channel.aclose()
			self._detached_receive_channel = None

		if self._logger_send_channel is not None:
			await self._logger_send_channel.aclose()
			self._logger_send_channel = None

		if self._logger is not None:
			await self._logger.close()
			self._logger = None

		for channel in self._events_receive_channels.values():
			await channel[0].aclose()
			await channel[1].wait()
		
		self._events_receive_channels = {}

		if self.background_task_ended is not None:
			await self.background_task_ended.wait()
			self.background_task_ended = None
	
	async def log_error(self, error: BaseException, extra_data: Optional[Dict[str, Any]] = None):
		"""
		Logs an error message, including its traceback, to the relevant target's log file
		and also logs it globally via the standard logging module.

		This method formats the exception's traceback using `extract_exception_trace`
		and sends it as an "ERROR" level log entry. It also calls `log_exception`
		to ensure the error is processed by the default Python logging system.

		Args:
			error (BaseException): The exception object to be logged.
			extra_data (Optional[Dict[str, Any]]): Optional additional data to include
				with the error log entry.
		"""
		
		stack = inspect.stack()
		
		extra_data_ = {
			"frame": str(stack[1].frame),
			"source_function": " <- ".join(stack_.function for stack_ in stack[1:]),
			"target_data": self.target_data.model_dump(),
		}
		
		if extra_data is not None:
			extra_data_.update(extra_data)
		
		await self.log(
				level="ERROR",
				message=extract_exception_trace(error),
				extra_data=extra_data_
		)
		log_exception(exception=error, extra_data=extra_data_)
	
	async def _run_event_handler(
			self,
			domain_handler_ready_event: trio.Event,
			event_config: "AbstractEventSettings"
	):
		"""
		Runs a single DevTools event handler for a specific target.

		This method sets up a listener for the specified CDP event and continuously
		receives and dispatches events to the configured `handle_function`.

		Args:
			domain_handler_ready_event (trio.Event): An event that will be set once the handler is started.
			event_config (AbstractEventSettings): The configuration for the specific CDP event handler.

		Raises:
			cdp_end_exceptions: If a CDP-related connection error occurs during listener setup or event processing.
			BaseException: If another unexpected error occurs during listener setup or event processing.
		"""
		
		await self.log_step(message=f"Event handler '{event_config.class_to_use_path}' starting.")
		
		try:
			receiver_channel: trio.MemoryReceiveChannel = self.cdp_session.listen(
					self.devtools_package.get(event_config.class_to_use_path),
					buffer_size=event_config.listen_buffer_size
			)
			channel_stopped_event = trio.Event()
		
			self._events_receive_channels[event_config.class_to_use_path] = (receiver_channel, channel_stopped_event)
		
			domain_handler_ready_event.set()
			handler = event_config.handle_function
		except cdp_end_exceptions as error:
			raise error
		except BaseException as error:
			await self.log_error(error=error)
			raise error
		
		await self.log_step(message=f"Event handler '{event_config.class_to_use_path}' started.")
		
		keep_alive = True
		while keep_alive:
			try:
				event = await receiver_channel.receive()
				self._nursery_object.start_soon(handler, self, event_config, event)
			except* cdp_end_exceptions:
				keep_alive = False
			except* BaseException as error:
				await self.log_error(error=error)
				keep_alive = False
		
		channel_stopped_event.set()
	
	async def _run_events_handlers(
			self,
			events_ready_event: trio.Event,
			domain_config: "AbstractDomainSettings"
	):
		"""
		Runs all configured event handlers for a specific DevTools domain within a target.

		This method iterates through the event configurations for a given domain and
		starts a separate task for each event handler.

		Args:
			events_ready_event (trio.Event): An event that will be set once all domain handlers are started.
			domain_config (AbstractDomainSettings): The configuration for the DevTools domain.

		Raises:
			cdp_end_exceptions: If a CDP-related connection error occurs during handler setup.
			BaseException: If another unexpected error occurs during the setup of any event handler.
		"""
		
		await self.log_step(
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
		
			await self.log_step(
					message=f"Domain '{domain_config.name}' events handlers setup complete."
			)
		except* cdp_end_exceptions as error:
			raise error
		except* BaseException as error:
			await self.log_error(error=error)
			raise error
	
	@property
	def type_(self) -> Optional[str]:
		"""
		Gets the type of the target (e.g., "page", "iframe", "service_worker").

		Returns:
			Optional[str]: The type of the target, or None if not set.
		"""
		
		return self.target_data.type_
	
	@type_.setter
	def type_(self, value: Optional[str]) -> None:
		"""
		Sets the type of the target and updates the logging acceptance flag.

		When the type is updated, this setter also re-evaluates whether
		this target's type should be accepted by the logging system's filters.

		Args:
			value (Optional[str]): The new type string for the target, or None to clear it.
		"""
		
		self._target_type_log_accepted = _validate_type_filter(
				value,
				self._logger_settings.target_type_filter_mode,
				self._logger_settings.target_type_filter
		)
		self.target_data.type_ = value
	
	@property
	def target_id(self) -> Optional[str]:
		"""
		Gets the unique identifier for the target.

		Returns:
			Optional[str]: The unique ID of the target, or None if not set.
		"""
		
		return self.target_data.target_id
	
	@target_id.setter
	def target_id(self, value: Optional[str]) -> None:
		"""
		Sets the unique identifier for the target and updates associated log statistics.

		When the target ID is updated, this setter ensures that the `target_data`
		object reflects the new ID and that the `_log_stats` object
		(which tracks per-channel statistics) is also updated.

		Args:
			value (Optional[str]): The new unique ID string to set, or None to clear it.
		"""
		
		self._log_stats.target_id = value
		self.target_data.target_id = value
	
	async def _run_detach_checking(self):
		self._detached_receive_channel: trio.MemoryReceiveChannel = self.cdp_session.listen(
				self.devtools_package.get("inspector.TargetCrashed"),
				self.devtools_package.get("inspector.Detached"),
				self.devtools_package.get("target.TargetCrashed"),
				self.devtools_package.get("target.TargetDestroyed"),
				self.devtools_package.get("target.DetachedFromTarget"),
				buffer_size=10
		)
		
		while True:
			event = await self._detached_receive_channel.receive()
			should_stop = False
		
			if isinstance(
					event,
					(
							self.devtools_package.get("inspector.Detached"),
							self.devtools_package.get("inspector.TargetCrashed"),
					)
			):
				should_stop = True
			elif isinstance(
					event,
					(
							self.devtools_package.get("target.TargetCrashed"),
							self.devtools_package.get("target.TargetDestroyed"),
							self.devtools_package.get("target.DetachedFromTarget"),
					)
			):
				if event.target_id == self.target_id:
					should_stop = True
		
			if should_stop:
				await self.stop()
				break
	
	async def _run_new_targets_listener(self, new_targets_listener_ready_event: trio.Event):
		"""
		Runs a listener for new browser targets (e.g., new tabs, iframes).

		This method continuously listens for `TargetCreated`, `AttachedToTarget`, and
		`TargetInfoChanged` events, and spawns a new task to handle each new target.

		Args:
			new_targets_listener_ready_event (trio.Event): An event that will be set once the listener is started.

		Raises:
			cdp_end_exceptions: If a CDP-related connection error occurs during listener setup or event processing.
			BaseException: If another unexpected error occurs during listener setup or event processing.
		"""
		
		await self.log_step(message="New Targets listener starting.")
		
		try:
			self._new_target_receive_channel: Tuple[trio.MemoryReceiveChannel, trio.Event] = (
					self.cdp_session.listen(
							self.devtools_package.get("target.TargetCreated"),
							self.devtools_package.get("target.AttachedToTarget"),
							self.devtools_package.get("target.TargetInfoChanged"),
							buffer_size=self._new_targets_buffer_size
					),
					trio.Event()
			)
			new_targets_listener_ready_event.set()
		except cdp_end_exceptions as error:
			raise error
		except BaseException as error:
			await self.log_error(error=error)
			raise error
		
		await self.log_step(message="New Targets listener started.")
		
		keep_alive = True
		while keep_alive:
			try:
				event = await self._new_target_receive_channel[0].receive()
		
				await execute_cdp_command(
						self=self,
						error_mode="log",
						function=self.devtools_package.get("target.attach_to_target"),
						target_id=event.target_info.target_id,
						flatten=True
				)
		
				self._nursery_object.start_soon(self._add_target_func, event)
			except* cdp_end_exceptions:
				keep_alive = False
			except* BaseException as error:
				await self.log_error(error=error)
				keep_alive = False
		
		self._new_target_receive_channel[1].set()
	
	async def _setup_new_targets_attaching(self):
		"""
		Configures the DevTools protocol to discover and auto-attach to new targets.

		This method uses `target.setDiscoverTargets` and `target.setAutoAttach`
		to ensure that new browser contexts (like new tabs or iframes) are
		automatically detected and attached to, allowing DevTools to manage them.

		Raises:
			cdp_end_exceptions: If a CDP-related connection error occurs during setup.
			BaseException: If another unexpected error occurs while setting up target discovery or auto-attachment.
		"""
		
		try:
			target_filter = self.devtools_package.get("target.TargetFilter")(self._new_targets_filter) if self._new_targets_filter is not None else None
		
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
		except cdp_end_exceptions as error:
			raise error
		except BaseException as error:
			await self.log_error(error=error)
			raise error
	
	async def _setup_target(self):
		"""
		Sets up a new browser target for DevTools interaction.

		This involves enabling target discovery and auto-attachment, and
		starting event handlers for configured DevTools domains within the target's session.

		Raises:
			cdp_end_exceptions: If a CDP-related connection error occurs during setup.
			BaseException: If any other unexpected error occurs during the target setup process.
		"""
		
		try:
			await self.log_step(message="Target setup started.")
		
			await self._setup_new_targets_attaching()
		
			target_ready_events: List[trio.Event] = []
		
			new_targets_listener_ready_event = trio.Event()
			target_ready_events.append(new_targets_listener_ready_event)
		
			self._nursery_object.start_soon(self._run_new_targets_listener, new_targets_listener_ready_event)
			self._nursery_object.start_soon(self._run_detach_checking,)
		
			for domain_name, domain_config in self._domains.model_dump(exclude_none=True).items():
				if domain_config.get("enable_func_path", None) is not None:
					enable_func_kwargs = domain_config.get("enable_func_kwargs", {})
		
					if (
							domain_config["include_target_types"]
							and self.type_ in domain_config["include_target_types"]
							or domain_config["exclude_target_types"]
							and self.type_ not in domain_config["exclude_target_types"]
					):
						await execute_cdp_command(
								self=self,
								error_mode="log",
								function=self.devtools_package.get(domain_config["enable_func_path"]),
								**enable_func_kwargs
						)
		
				domain_handlers_ready_event = trio.Event()
				target_ready_events.append(domain_handlers_ready_event)
				self._nursery_object.start_soon(
						self._run_events_handlers,
						domain_handlers_ready_event,
						getattr(self._domains, domain_name)
				)
		
			for domain_handlers_ready_event in target_ready_events:
				await domain_handlers_ready_event.wait()
		
			await execute_cdp_command(
					self=self,
					error_mode="log",
					function=self.devtools_package.get("runtime.run_if_waiting_for_debugger"),
			)
		
			await self.log_step(message="Target setup complete.")
		except* cdp_end_exceptions as error:
			raise error
		except* BaseException as error:
			await self.log_error(error=error)
			raise error
	
	async def run(self):
		"""
		Runs the DevTools session for this target, handling its lifecycle.

		This method establishes the CDP session, sets up event listeners,
		runs the optional background task, and waits for a stop signal.
		It handles various exceptions during its lifecycle, logging them
		and ensuring graceful shutdown.
		"""
		
		try:
			self._logger_send_channel, self._logger = build_target_logger(self.target_data, self._nursery_object, self._logger_settings)
		
			if self._target_type_log_accepted:
				await self._logger.run()
		
			await self.log_step(message=f"Target '{self.target_id}' added.")
		
			async with open_cdp(self.websocket_url) as new_connection:
				target_id_instance = self.devtools_package.get("target.TargetID").from_json(self.target_id)
		
				async with new_connection.open_session(target_id_instance) as new_session:
					self._cdp_session = new_session
		
					await self._setup_target()
		
					if self._target_background_task is not None:
						self._nursery_object.start_soon(_background_task_decorator(self._target_background_task), self)
		
					await wait_one(self.exit_event, self.about_to_stop_event)
		except* (BrowserError, RuntimeError):
			self.about_to_stop_event.set()
		except* cdp_end_exceptions:
			self.about_to_stop_event.set()
		except* BaseException as error:
			self.about_to_stop_event.set()
			await self.log_error(error=error)
		finally:
			await self._close_instances()
			await self._remove_target_func(self)
		
			self.stopped_event.set()
	
	@property
	def subtype(self) -> Optional[str]:
		"""
		Gets the subtype of the target, if applicable.

		Returns:
			Optional[str]: The subtype of the target, or None if not set.
		"""
		
		return self.target_data.subtype
	
	@subtype.setter
	def subtype(self, value: Optional[str]) -> None:
		"""
		Sets the subtype of the target.

		Args:
			value (Optional[str]): The new subtype string to set, or None to clear it.
		"""
		
		self.target_data.subtype = value
	
	@property
	def target_type_log_accepted(self) -> bool:
		"""
		Checks if this target's type is accepted by the logger's filter.

		This property reflects whether log entries originating from this target's
		type are configured to be processed by the logging system.

		Returns:
			bool: True if the target's type is accepted for logging, False otherwise.
		"""
		
		return self._target_type_log_accepted
	
	@property
	def title(self) -> Optional[str]:
		"""
		Gets the title of the target (e.g., the page title).

		Returns:
			Optional[str]: The current title of the target, or None if not available.
		"""
		
		return self.target_data.title
	
	@title.setter
	def title(self, value: Optional[str]) -> None:
		"""
		Sets the title of the target and updates associated log statistics.

		When the title is updated, this setter ensures that the `target_data`
		object reflects the new title and that the `_log_stats` object
		(which tracks per-channel statistics) is also updated.

		Args:
			value (Optional[str]): The new title string to set, or None to clear it.
		"""
		
		self._log_stats.title = value
		self.target_data.title = value
	
	@property
	def url(self) -> Optional[str]:
		"""
		Gets the URL of the target.

		Returns:
			Optional[str]: The current URL of the target, or None if not available.
		"""
		
		return self.target_data.url
	
	@url.setter
	def url(self, value: Optional[str]) -> None:
		"""
		Sets the URL of the target and updates associated log statistics.

		When the URL is updated, this setter ensures that the `target_data`
		object reflects the new URL and that the `_log_stats` object
		(which tracks per-channel statistics) is also updated.

		Args:
			value (Optional[str]): The new URL string to set, or None to clear it.
		"""
		
		self._log_stats.url = value
		self.target_data.url = value
	
	async def log(
			self,
			level: LogLevelsType,
			message: str,
			extra_data: Optional[Dict[str, Any]] = None
	):
		"""
		Logs a message to the internal logger manager, automatically determining the source function.

		This method acts as a convenient wrapper around the underlying `_logger.log` method.
		If `source_function` is not explicitly provided, it automatically determines the
		calling function's name from the call stack to enrich the log entry.

		Args:
			level (LogLevelsType): The severity level of the log (e.g., "INFO", "ERROR").
			message (str): The main log message.
			extra_data (Optional[Dict[str, Any]]): Optional additional data to associate
				with the log entry.
		"""
		
		log_entry = LogEntry(
				target_data=self.target_data,
				message=message,
				level=level,
				timestamp=datetime.now(),
				extra_data=extra_data
		)
		await self._add_log_func(log_entry)
		
		if self._target_type_log_accepted and self._logger is not None and self._logger_send_channel is not None:
			await self._log_stats.add_log(log_entry)
			await self._logger.run()
		
			try:
				self._logger_send_channel.send_nowait(log_entry)
			except trio.WouldBlock:
				warnings.warn(
						f"WARNING: Log channel for session {self.target_id} is full. Log dropped:\n{log_entry.model_dump_json(indent=4)}"
				)
			except trio.BrokenResourceError:
				warnings.warn(
						f"WARNING: Log channel for session {self.target_id} is broken. Log dropped:\n{log_entry.model_dump_json(indent=4)}"
				)
	
	async def log_step(self, message: str, extra_data: Optional[Dict[str, Any]] = None):
		"""
		Logs an informational step message using the internal logger manager.

		This is a convenience method for logging "INFO" level messages,
		automatically determining the source function from the call stack.

		Args:
			message (str): The step message to log.
		"""
		
		stack = inspect.stack()
		
		extra_data_ = {"source_function": " <- ".join(stack_.function for stack_ in stack[1:]),}
		
		if extra_data is not None:
			extra_data_.update(extra_data)
		
		await self.log(level="INFO", message=message, extra_data=extra_data_)
