import trio
from osn_selenium.dev_tools.models import TargetData
from selenium.webdriver.common.bidi.cdp import CdpSession
from osn_selenium.dev_tools._wrappers import DevToolsPackage
from osn_selenium.dev_tools.logger.target import TargetLogger
from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	Optional,
	Sequence,
	TYPE_CHECKING,
	Tuple
)
from osn_selenium.dev_tools._validators import (
	validate_target_event_filter,
	validate_type_filter
)
from osn_selenium.dev_tools.logger.models import (
	CDPLoggerChannelStats,
	CDPTargetLogEntry,
	FingerprintLoggerChannelStats,
	FingerprintTargetLogEntry
)


__all__ = ["BaseMixin"]

if TYPE_CHECKING:
	from osn_selenium.dev_tools.target import DevToolsTarget
	from osn_selenium.dev_tools.domains import DomainsSettings
	from osn_selenium.dev_tools.settings import LoggerSettings
	from osn_selenium.dev_tools._typehints import DEVTOOLS_BACKGROUND_FUNCTION_TYPEHINT


class BaseMixin:
	"""
	Base mixin for DevToolsTarget providing initialization, properties, and logging functionality.

	This class handles the core state of a DevTools target, including its data, logging channels,
	filter configurations, and synchronization primitives.

	Attributes:
		target_data (TargetData): The essential data identifying the target (id, type, url, etc.).
		devtools_package (DevToolsPackage): The wrapper for the DevTools protocol module.
		websocket_url (Optional[str]): The WebSocket URL used to connect to this target.
		exit_event (trio.Event): Event to signal global exit.
		started_event (trio.Event): Event set when the target handling has started.
		about_to_stop_event (trio.Event): Event set when the target is about to stop.
		stopped_event (trio.Event): Event set when the target handling has fully stopped.
		background_task_ended (Optional[trio.Event]): Event set when the background task completes.
	"""
	
	def __init__(
			self,
			target_data: TargetData,
			is_main_target: bool,
			logger_settings: "LoggerSettings",
			domains_settings: Optional["DomainsSettings"],
			devtools_package: DevToolsPackage,
			websocket_url: Optional[str],
			new_targets_filter_list: Sequence[Dict[str, Any]],
			new_targets_buffer_size: int,
			nursery: trio.Nursery,
			exit_event: trio.Event,
			fingerprint_injection_script: Optional[str],
			target_background_task: Optional["DEVTOOLS_BACKGROUND_FUNCTION_TYPEHINT"],
			add_target_func: Callable[[Any], Coroutine[Any, Any, bool]],
			remove_target_func: Callable[["DevToolsTarget"], Coroutine[Any, Any, Optional[bool]]],
			add_cdp_log_func: Callable[[CDPTargetLogEntry], Coroutine[Any, Any, None]],
			add_fingerprint_log_func: Callable[[FingerprintTargetLogEntry], Coroutine[Any, Any, None]],
	):
		"""
		Initializes the BaseMixin.

		Args:
			target_data (TargetData): Information about the target.
			is_main_target (bool): Whether this is the primary target.
			logger_settings ("LoggerSettings"): Configuration for logging.
			domains_settings (Optional["DomainsSettings"]): Configuration for enabled domains and handlers.
			devtools_package (DevToolsPackage): Access to CDP commands and events.
			websocket_url (Optional[str]): The debugger URL.
			new_targets_filter_list (Sequence[Mapping[str, Any]]): Filters for discovering new targets.
			new_targets_buffer_size (int): Buffer size for new target events.
			nursery (trio.Nursery): Trio nursery for background tasks.
			exit_event (trio.Event): Signal to stop all operations.
			fingerprint_injection_script (Optional[str]): JS script to inject into the target.
			target_background_task (Optional[devtools_background_func_type]): Optional background task to run.
			add_target_func (Callable[[Any], Coroutine[Any, Any, bool]]): Callback to add a new target.
			remove_target_func (Callable[[DevToolsTarget], Coroutine[Any, Any, Optional[bool]]]): Callback to remove this target.
			add_cdp_log_func (Callable[[CDPTargetLogEntry], Coroutine[Any, Any, None]]): Callback to record a CDP log entry.
			add_fingerprint_log_func (Callable[[FingerprintTargetLogEntry], Coroutine[Any, Any, None]]): Callback to record a fingerprint log entry.
		"""
		
		self.target_data = target_data
		self._is_main_target = is_main_target
		self._logger_settings = logger_settings
		self._domains_settings = domains_settings
		self.devtools_package = devtools_package
		self.websocket_url = websocket_url
		self._new_targets_filter_list = new_targets_filter_list
		self._new_targets_buffer_size = new_targets_buffer_size
		self._nursery_object = nursery
		self.exit_event = exit_event
		self._target_background_task = target_background_task
		self._add_target_func = add_target_func
		self._remove_target_func = remove_target_func
		self._add_cdp_log_func = add_cdp_log_func
		self._add_fingerprint_log_func = add_fingerprint_log_func
		self._fingerprint_injection_script = fingerprint_injection_script
		
		self._new_targets_events_filters = validate_target_event_filter(filter_=new_targets_filter_list)
		
		self._cdp_target_type_log_accepted = validate_type_filter(
				type_=self.type_,
				filter_mode=self._logger_settings.cdp_settings.target_type_filter_mode,
				filter_instances=self._logger_settings.cdp_settings.target_type_filter
		)
		
		self._cdp_log_stats = CDPLoggerChannelStats(
				target_id=target_data.target_id,
				title=target_data.title,
				url=target_data.url,
		)
		
		self._fingerprint_log_stats = FingerprintLoggerChannelStats(
				target_id=target_data.target_id,
				title=target_data.title,
				url=target_data.url,
		)
		
		self.started_event = trio.Event()
		self.about_to_stop_event = trio.Event()
		self.background_task_ended: Optional[trio.Event] = None
		self.stopped_event = trio.Event()
		self._logger_cdp_send_channel: Optional[trio.MemorySendChannel[CDPTargetLogEntry]] = None
		self._logger_fingerprint_send_channel: Optional[trio.MemorySendChannel[FingerprintTargetLogEntry]] = None
		self._logger: Optional[TargetLogger] = None
		self._cdp_session: Optional[CdpSession] = None
		self._new_target_receive_channel: Optional[Tuple[trio.MemoryReceiveChannel, trio.Event]] = None
		self._detached_receive_channel: Optional[trio.MemoryReceiveChannel] = None
		self._events_receive_channels: Dict[str, Tuple[trio.MemoryReceiveChannel, trio.Event]] = {}
		self._cancel_scopes: Dict[str, trio.CancelScope] = {}
	
	@property
	def type_(self) -> Optional[str]:
		"""
		Gets the type of the target (e.g., 'page', 'iframe').

		Returns:
			Optional[str]: The target type.
		"""
		
		return self.target_data.type_
	
	@type_.setter
	def type_(self, value: Optional[str]) -> None:
		"""
		Sets the target type and re-evaluates log filtering.

		Args:
			value (Optional[str]): The new target type.
		"""
		
		self._cdp_target_type_log_accepted = validate_type_filter(
				type_=value,
				filter_mode=self._logger_settings.cdp_settings.target_type_filter_mode,
				filter_instances=self._logger_settings.cdp_settings.target_type_filter
		)
		self.target_data.type_ = value
	
	@property
	def attached(self) -> Optional[bool]:
		"""
		Checks if the target is currently attached.

		Returns:
			Optional[bool]: True if attached, False otherwise.
		"""
		
		return self.target_data.attached
	
	@attached.setter
	def attached(self, value: Optional[bool]) -> None:
		"""
		Sets the attached status.

		Args:
			value (Optional[bool]): The new attached status.
		"""
		
		self.target_data.attached = value
	
	@property
	def browser_context_id(self) -> Optional[str]:
		"""
		Gets the browser context ID.

		Returns:
			Optional[str]: The browser context ID.
		"""
		
		return self.target_data.browser_context_id
	
	@browser_context_id.setter
	def browser_context_id(self, value: Optional[str]) -> None:
		"""
		Sets the browser context ID.

		Args:
			value (Optional[str]): The new browser context ID.
		"""
		
		self.target_data.browser_context_id = value
	
	@property
	def can_access_opener(self) -> Optional[bool]:
		"""
		Checks if the target can access its opener.

		Returns:
			Optional[bool]: True if accessible, False otherwise.
		"""
		
		return self.target_data.can_access_opener
	
	@can_access_opener.setter
	def can_access_opener(self, value: Optional[bool]) -> None:
		"""
		Sets whether the target can access its opener.

		Args:
			value (Optional[bool]): Access status.
		"""
		
		self.target_data.can_access_opener = value
	
	@property
	def cancel_scopes(self) -> Dict[str, trio.CancelScope]:
		"""
		Provides access to the dictionary of cancellation scopes.

		Returns:
			Dict[str, trio.CancelScope]: The cancel scopes dictionary.
		"""
		
		return self._cancel_scopes
	
	@property
	def cdp_log_stats(self) -> CDPLoggerChannelStats:
		"""
		Gets the CDP logging statistics for this target channel.

		Returns:
			CDPLoggerChannelStats: The statistics object.
		"""
		
		return self._cdp_log_stats
	
	@property
	def cdp_session(self) -> CdpSession:
		"""
		Gets the active CDP session for this target.

		Returns:
			CdpSession: The CDP session object.
		"""
		
		return self._cdp_session
	
	@property
	def fingerprint_log_stats(self) -> FingerprintLoggerChannelStats:
		"""
		Gets the fingerprint logging statistics for this target channel.

		Returns:
			FingerprintLoggerChannelStats: The statistics object.
		"""
		
		return self._fingerprint_log_stats
	
	@property
	def opener_frame_id(self) -> Optional[str]:
		"""
		Gets the ID of the opener frame.

		Returns:
			Optional[str]: The opener frame ID.
		"""
		
		return self.target_data.opener_frame_id
	
	@opener_frame_id.setter
	def opener_frame_id(self, value: Optional[str]) -> None:
		"""
		Sets the ID of the opener frame.

		Args:
			value (Optional[str]): The new opener frame ID.
		"""
		
		self.target_data.opener_frame_id = value
	
	@property
	def opener_id(self) -> Optional[str]:
		"""
		Gets the ID of the opener target.

		Returns:
			Optional[str]: The opener ID.
		"""
		
		return self.target_data.opener_id
	
	@opener_id.setter
	def opener_id(self, value: Optional[str]) -> None:
		"""
		Sets the ID of the opener target.

		Args:
			value (Optional[str]): The new opener ID.
		"""
		
		self.target_data.opener_id = value
	
	@property
	def subtype(self) -> Optional[str]:
		"""
		Gets the subtype of the target.

		Returns:
			Optional[str]: The subtype.
		"""
		
		return self.target_data.subtype
	
	@subtype.setter
	def subtype(self, value: Optional[str]) -> None:
		"""
		Sets the subtype of the target.

		Args:
			value (Optional[str]): The new subtype.
		"""
		
		self.target_data.subtype = value
	
	@property
	def target_id(self) -> Optional[str]:
		"""
		Gets the unique target ID.

		Returns:
			Optional[str]: The target ID.
		"""
		
		return self.target_data.target_id
	
	@target_id.setter
	def target_id(self, value: Optional[str]) -> None:
		"""
		Sets the target ID and updates log stats.

		Args:
			value (Optional[str]): The new target ID.
		"""
		
		self._cdp_log_stats.target_id = value
		self.target_data.target_id = value
	
	@property
	def target_type_log_accepted(self) -> bool:
		"""
		Checks if logging is accepted for this target type.

		Returns:
			bool: True if logging is allowed, False otherwise.
		"""
		
		return self._cdp_target_type_log_accepted
	
	@property
	def title(self) -> Optional[str]:
		"""
		Gets the title of the target.

		Returns:
			Optional[str]: The title.
		"""
		
		return self.target_data.title
	
	@title.setter
	def title(self, value: Optional[str]) -> None:
		"""
		Sets the title of the target and updates log stats.

		Args:
			value (Optional[str]): The new title.
		"""
		
		self._cdp_log_stats.title = value
		self.target_data.title = value
	
	@property
	def url(self) -> Optional[str]:
		"""
		Gets the URL of the target.

		Returns:
			Optional[str]: The URL.
		"""
		
		return self.target_data.url
	
	@url.setter
	def url(self, value: Optional[str]) -> None:
		"""
		Sets the URL of the target and updates log stats.

		Args:
			value (Optional[str]): The new URL.
		"""
		
		self._cdp_log_stats.url = value
		self.target_data.url = value
