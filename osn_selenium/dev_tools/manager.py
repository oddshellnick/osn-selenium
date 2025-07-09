import trio
import inspect
import warnings
from datetime import datetime
from types import TracebackType
from dataclasses import dataclass
from collections.abc import Sequence
from contextlib import (
	AbstractAsyncContextManager
)
from selenium.webdriver.remote.bidi_connection import BidiConnection
from typing import (
	Any,
	Awaitable,
	Callable,
	Optional,
	TYPE_CHECKING,
	Union
)
from osn_selenium.dev_tools.domains.abstract import (
	AbstractDomain,
	AbstractEvent
)
from selenium.webdriver.common.bidi.cdp import (
	BrowserError,
	CdpSession,
	open_cdp
)
from osn_selenium.dev_tools._types import (
	LogLevelsType,
	devtools_background_func_type
)
from osn_selenium.dev_tools.domains import (
	Domains,
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
	LoggerChannelStats,
	LoggerSettings,
	MainLogEntry,
	MainLogger,
	TargetLogger,
	TargetTypeStats,
	build_main_logger,
	build_target_logger
)
from osn_selenium.dev_tools.utils import (
	TargetData,
	TargetFilter,
	_background_task_decorator,
	_prepare_log_dir,
	_validate_type_filter,
	execute_cdp_command,
	extract_exception_trace,
	log_exception,
	log_on_error,
	wait_one,
	warn_if_active
)


if TYPE_CHECKING:
	from osn_selenium.webdrivers.BaseDriver.webdriver import BrowserWebDriver


@dataclass
class DevToolsSettings:
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
	logger_settings: Optional[LoggerSettings] = None


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
		_new_targets_filter (Optional[list[dict[str, Any]]]): Filter settings for discovering new targets.
		_new_targets_buffer_size (int): Buffer size for new target events.
		_domains (Domains): Configuration for DevTools domains and their event handlers.
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
		_events_receive_channels (dict[str, tuple[trio.MemoryReceiveChannel[Any], trio.Event]]): Channels and events for domain-specific events.
	"""
	
	def __init__(
			self,
			target_data: TargetData,
			logger_settings: LoggerSettings,
			devtools_package: Any,
			websocket_url: Optional[str],
			new_targets_filter: list[dict[str, Any]],
			new_targets_buffer_size: int,
			domains: Domains,
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
			devtools_package (Any): The DevTools protocol package.
			websocket_url (Optional[str]): WebSocket URL for CDP connection.
			new_targets_filter (Optional[list[dict[str, Any]]]): Filters for new targets.
			new_targets_buffer_size (int): Buffer size for new target events.
			domains (Domains): Configured DevTools domains.
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
		self._new_target_receive_channel: Optional[tuple[trio.MemoryReceiveChannel, trio.Event]] = None
		self._events_receive_channels: dict[str, tuple[trio.MemoryReceiveChannel, trio.Event]] = {}
	
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
	
	async def log_error(self, error: BaseException, extra_data: Optional[dict[str, Any]] = None):
		"""
		Logs an error message, including its traceback, to the relevant target's log file
		and also logs it globally via the standard logging module.

		This method formats the exception's traceback using `extract_exception_trace`
		and sends it as an "ERROR" level log entry. It also calls `log_exception`
		to ensure the error is processed by the default Python logging system.

		Args:
			error (BaseException): The exception object to be logged.
			extra_data (Optional[dict[str, Any]]): Optional additional data to include
				with the error log entry.
		"""
		
		await self.log(
				level="ERROR",
				message=extract_exception_trace(error),
				source_function=" <- ".join(stack.function for stack in inspect.stack()[1:]),
				extra_data=extra_data
		)
		log_exception(error)
	
	async def get_devtools_object(self, path: str) -> Any:
		"""
		Navigates and retrieves a specific object within the DevTools API structure.

		Using a dot-separated path, this method traverses the nested DevTools API objects to retrieve a target object.
		For example, a path like "fetch.enable" would access `self.devtools_module.fetch.enable`.
		Results are cached for faster access.

		Args:
			path (str): A dot-separated string representing the path to the desired DevTools API object.

		Returns:
			Any: The DevTools API object located at the specified path.

		Raises:
			cdp_end_exceptions: If a CDP-related connection error occurs.
			BaseException: If the object cannot be found or another error occurs during retrieval.
		"""
		
		try:
			package = self.devtools_package
		
			for part in path.split("."):
				package = getattr(package, part)
		
			return package
		except cdp_end_exceptions as error:
			raise error
		except BaseException as error:
			await self.log_error(error=error)
			raise error
	
	async def _run_event_handler(
			self,
			domain_handler_ready_event: trio.Event,
			event_config: AbstractEvent
	):
		"""
		Runs a single DevTools event handler for a specific target.

		This method sets up a listener for the specified CDP event and continuously
		receives and dispatches events to the configured `handle_function`.

		Args:
			domain_handler_ready_event (trio.Event): An event that will be set once the handler is started.
			event_config (AbstractEvent): The configuration for the specific CDP event handler.

		Raises:
			cdp_end_exceptions: If a CDP-related connection error occurs during listener setup or event processing.
			BaseException: If another unexpected error occurs during listener setup or event processing.
		"""
		
		await self.log_step(
				message=f"Event handler '{event_config['class_to_use_path']}' starting."
		)
		
		try:
			receiver_channel: trio.MemoryReceiveChannel = self.cdp_session.listen(
					await self.get_devtools_object(event_config["class_to_use_path"]),
					buffer_size=event_config["listen_buffer_size"]
			)
			channel_stopped_event = trio.Event()
		
			self._events_receive_channels[event_config["class_to_use_path"]] = (receiver_channel, channel_stopped_event)
		
			domain_handler_ready_event.set()
			handler = event_config["handle_function"]
		except cdp_end_exceptions as error:
			raise error
		except BaseException as error:
			await self.log_error(error=error)
			raise error
		
		await self.log_step(
				message=f"Event handler '{event_config['class_to_use_path']}' started."
		)
		
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
	
	async def _run_events_handlers(self, events_ready_event: trio.Event, domain_config: AbstractDomain):
		"""
		Runs all configured event handlers for a specific DevTools domain within a target.

		This method iterates through the event configurations for a given domain and
		starts a separate task for each event handler.

		Args:
			events_ready_event (trio.Event): An event that will be set once all domain handlers are started.
			domain_config (AbstractDomain): The configuration for the DevTools domain.

		Raises:
			cdp_end_exceptions: If a CDP-related connection error occurs during handler setup.
			BaseException: If another unexpected error occurs during the setup of any event handler.
		"""
		
		await self.log_step(
				message=f"Domain '{domain_config['name']}' events handlers setup started."
		)
		
		try:
			events_handlers_ready_events: list[trio.Event] = []
		
			for event_name, event_config in domain_config.get("handlers", {}).items():
				if event_config is not None:
					event_handler_ready_event = trio.Event()
					events_handlers_ready_events.append(event_handler_ready_event)
		
					self._nursery_object.start_soon(self._run_event_handler, event_handler_ready_event, event_config)
		
			for event_handler_ready_event in events_handlers_ready_events:
				await event_handler_ready_event.wait()
		
			events_ready_event.set()
		
			await self.log_step(
					message=f"Domain '{domain_config['name']}' events handlers setup complete."
			)
		except* cdp_end_exceptions as error:
			raise error
		except* BaseException as error:
			await self.log_error(error=error)
			raise error
	
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
			self._new_target_receive_channel: tuple[trio.MemoryReceiveChannel, trio.Event] = (
					self.cdp_session.listen(
							await self.get_devtools_object("target.TargetCreated"),
							await self.get_devtools_object("target.AttachedToTarget"),
							await self.get_devtools_object("target.TargetInfoChanged"),
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
			target_filter = (await self.get_devtools_object("target.TargetFilter"))(self._new_targets_filter) if self._new_targets_filter is not None else None
		
			await execute_cdp_command(
					self,
					"log",
					await self.get_devtools_object("target.set_discover_targets"),
					discover=True,
					filter_=target_filter,
			)
			await execute_cdp_command(
					self,
					"log",
					await self.get_devtools_object("target.set_auto_attach"),
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
		
			target_ready_events: list[trio.Event] = []
		
			new_targets_listener_ready_event = trio.Event()
			target_ready_events.append(new_targets_listener_ready_event)
		
			self._nursery_object.start_soon(self._run_new_targets_listener, new_targets_listener_ready_event)
		
			for domain_name, domain_config in self._domains.items():
				if domain_config.get("enable_func_path", None) is not None:
					enable_func_kwargs = domain_config.get("enable_func_kwargs", {})
					await execute_cdp_command(
							self,
							"raise",
							await self.get_devtools_object(domain_config["enable_func_path"]),
							**enable_func_kwargs
					)
		
				domain_handlers_ready_event = trio.Event()
				target_ready_events.append(domain_handlers_ready_event)
				self._nursery_object.start_soon(self._run_events_handlers, domain_handlers_ready_event, domain_config)
		
			for domain_handlers_ready_event in target_ready_events:
				await domain_handlers_ready_event.wait()
		
			await execute_cdp_command(
					self,
					"log",
					await self.get_devtools_object("runtime.run_if_waiting_for_debugger")
			)
		
			await self.log_step(message="Target setup complete.")
		except* cdp_end_exceptions as error:
			raise error
		except* BaseException as error:
			await self.log_error(error=error)
			raise error
	
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
				async with new_connection.open_session(self.target_id) as new_session:
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
			source_function: Optional[str] = None,
			extra_data: Optional[dict[str, Any]] = None
	):
		"""
		Logs a message to the internal logger manager, automatically determining the source function.

		This method acts as a convenient wrapper around the underlying `_logger.log` method.
		If `source_function` is not explicitly provided, it automatically determines the
		calling function's name from the call stack to enrich the log entry.

		Args:
			level (LogLevelsType): The severity level of the log (e.g., "INFO", "ERROR").
			message (str): The main log message.
			source_function (Optional[str]): The name of the function that generated the log.
				If None, the function will attempt to determine it from the call stack.
			extra_data (Optional[dict[str, Any]]): Optional additional data to associate
				with the log entry.
		"""
		
		log_entry = LogEntry(
				target_data=self.target_data,
				message=message,
				level=level,
				timestamp=datetime.now(),
				source_function=" <- ".join(stack.function for stack in inspect.stack()[1:])
				if source_function is None
				else source_function,
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
						f"WARNING: Log channel for session {self.target_id} is full. Log dropped:\n{log_entry.to_string()}"
				)
			except trio.BrokenResourceError:
				warnings.warn(
						f"WARNING: Log channel for session {self.target_id} is broken. Log dropped:\n{log_entry.to_string()}"
				)
	
	async def log_step(self, message: str):
		"""
		Logs an informational step message using the internal logger manager.

		This is a convenience method for logging "INFO" level messages,
		automatically determining the source function from the call stack.

		Args:
			message (str): The step message to log.
		"""
		
		await self.log(
				level="INFO",
				message=message,
				source_function=" <- ".join(stack.function for stack in inspect.stack()[1:])
		)


class DevTools:
	"""
	Base class for handling DevTools functionalities in Selenium WebDriver.

	Provides an interface to interact with Chrome DevTools Protocol (CDP)
	for advanced browser control and monitoring. This class supports event handling
	and allows for dynamic modifications of browser behavior, such as network request interception,
	by using an asynchronous context manager.

	Attributes:
		_webdriver ("BrowserWebDriver"): The parent WebDriver instance associated with this DevTools instance.
		_new_targets_filter (Optional[list[dict[str, Any]]]): Processed filters for new targets.
		_new_targets_buffer_size (int): Buffer size for new target events.
		_target_background_task (Optional[devtools_background_func_type]): Optional background task for targets.
		_logger_settings (LoggerSettings): Logging configuration for the entire DevTools manager.
		_bidi_connection (Optional[AbstractAsyncContextManager[BidiConnection, Any]]): Asynchronous context manager for the BiDi connection.
		_bidi_connection_object (Optional[BidiConnection]): The BiDi connection object when active.
		_nursery (Optional[AbstractAsyncContextManager[trio.Nursery, object]]): Asynchronous context manager for the Trio nursery.
		_nursery_object (Optional[trio.Nursery]): The Trio nursery object when active, managing concurrent tasks.
		_domains_settings (Domains): Settings for configuring DevTools domain handlers.
		_handling_targets (dict[str, DevToolsTarget]): Dictionary of target IDs currently being handled by event listeners.
		targets_lock (trio.Lock): A lock used for synchronizing access to shared resources, like the list of handled targets.
		exit_event (Optional[trio.Event]): Trio Event to signal exiting of DevTools event handling.
		_is_active (bool): Flag indicating if the DevTools event handler is currently active.
		_is_closing (bool): Flag indicating if the DevTools manager is in the process of closing.
		_num_logs (int): Total count of all log entries across all targets.
		_targets_types_stats (dict[str, TargetTypeStats]): Statistics for each target type.
		_log_level_stats (dict[str, LogLevelStats]): Overall statistics for each log level.
		_main_logger (Optional[MainLogger]): The main logger instance.
		_main_logger_send_channel (Optional[trio.MemorySendChannel[MainLogEntry]]): Send channel for the main logger.

	EXAMPLES
	________
	>>> from osn_selenium.webdrivers.Chrome.webdriver import ChromeWebDriver
	... from osn_selenium.dev_tools.domains import DomainsSettings
	...
	... async def main():
	...     driver = ChromeWebDriver("path/to/chromedriver")
	...     driver.dev_tools.set_domains_handlers(DomainsSettings(...))
	...
	...     driver_wrapper = driver.to_wrapper()
	...
	...	    # Configure domain handlers here.
	...	    async with driver.dev_tools:
	...	        # DevTools event handling is active within this block.
	...	        await driver_wrapper.search_url("https://example.com")
	...	        # DevTools event handling is deactivated after exiting the block.
	"""
	
	def __init__(
			self,
			parent_webdriver: "BrowserWebDriver",
			devtools_settings: Optional[DevToolsSettings] = None
	):
		"""
		Initializes the DevTools manager.

		Args:
			parent_webdriver ("BrowserWebDriver"): The WebDriver instance to which this DevTools manager is attached.
			devtools_settings (Optional[DevToolsSettings]): Configuration settings for DevTools.
				If None, default settings will be used.
		"""
		
		if devtools_settings is None:
			devtools_settings = DevToolsSettings()
		
		self._webdriver = parent_webdriver
		
		self._new_targets_filter = [filter_.to_dict() for filter_ in devtools_settings.new_targets_filter] if devtools_settings.new_targets_filter is not None else None
		
		self._new_targets_buffer_size = devtools_settings.new_targets_buffer_size
		self._target_background_task = devtools_settings.target_background_task
		self._logger_settings = devtools_settings.logger_settings
		self._bidi_connection: Optional[AbstractAsyncContextManager[BidiConnection, Any]] = None
		self._bidi_connection_object: Optional[BidiConnection] = None
		self._nursery: Optional[AbstractAsyncContextManager[trio.Nursery, Optional[bool]]] = None
		self._nursery_object: Optional[trio.Nursery] = None
		self._domains_settings: Domains = {}
		self._handling_targets: dict[str, DevToolsTarget] = {}
		self.targets_lock = trio.Lock()
		self._websocket_url: Optional[str] = None
		self.exit_event: Optional[trio.Event] = None
		self._is_active = False
		self._is_closing = False
		self._num_logs = 0
		self._targets_types_stats: dict[str, TargetTypeStats] = {}
		self._log_level_stats: dict[str, LogLevelStats] = {}
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
		Removes a target ID from the list of currently handled targets.

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
	def _devtools_package(self) -> Any:
		"""
		Retrieves the DevTools protocol package from the active BiDi connection.

		Returns:
			Any: The DevTools protocol package object, providing access to CDP domains and commands.

		Raises:
			BidiConnectionNotEstablishedError: If the BiDi connection is not active.
		"""
		
		try:
			if self._bidi_connection_object is not None:
				return self._bidi_connection_object.devtools
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
	
	async def _get_devtools_object(self, path: str) -> Any:
		"""
		Navigates and retrieves a specific object within the DevTools API structure.

		Using a dot-separated path, this method traverses the nested DevTools API objects to retrieve a target object.
		For example, a path like "fetch.enable" would access `self.devtools_module.fetch.enable`.
		Results are cached for faster access.

		Args:
			path (str): A dot-separated string representing the path to the desired DevTools API object.

		Returns:
			Any: The DevTools API object located at the specified path.

		Raises:
			cdp_end_exceptions: If a CDP-related connection error occurs.
			BaseException: If the object cannot be found or another error occurs during retrieval.
		"""
		
		try:
			package = self._devtools_package
		
			for part in path.split("."):
				package = getattr(package, part)
		
			return package
		except cdp_end_exceptions as error:
			raise error
		except BaseException as error:
			log_exception(error)
			raise error
	
	async def _get_all_targets(self) -> list[Any]:
		"""
		Retrieves a list of all currently active browser targets.

		Returns:
			list[Any]: A list of target objects, each containing information like target ID, type, and URL.

		Raises:
			BidiConnectionNotEstablishedError: If the BiDi connection is not active.
		"""
		
		try:
			if self._bidi_connection_object is not None:
				targets_filter = (await self._get_devtools_object("target.TargetFilter"))(
						[
							{"exclude": False, "type": "page"},
							{"exclude": False, "type": "tab"},
							{"exclude": True}
						]
				)
		
				return await self._bidi_connection_object.session.execute(self._devtools_package.target.get_targets(targets_filter))
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
			exc_type: Optional[type],
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
			exc_type (Optional[type[BaseException]]): The exception type, if any, that caused the context to be exited.
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
		
		self._domains_settings[domain] = settings
	
	def set_domains_handlers(self, settings: DomainsSettings):
		"""
		Sets handler settings for multiple domains from a DomainsSettings object.

		This method iterates through the provided settings and applies them to the corresponding domains.
		It should only be called when the DevTools context is not active.

		Args:
			settings (DomainsSettings): An object containing the configuration for one or more domains.
		"""
		
		for domain_name, domain_settings in settings.to_dict().items():
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
