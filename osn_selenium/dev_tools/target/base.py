import inspect
import warnings
from datetime import datetime
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    Optional,
    Sequence,
    TYPE_CHECKING,
    Tuple
)

import trio
from selenium.webdriver.common.bidi.cdp import CdpSession

from osn_selenium.dev_tools.logger.target import (
    TargetLogEntry,
    TargetLogger
)
from osn_selenium.dev_tools.logger.main import LoggerChannelStats
from osn_selenium.dev_tools.utils import (
    DevToolsPackage,
    TargetData
)
from osn_selenium.dev_tools.exception_utils import (
    extract_exception_trace,
    log_exception
)
from osn_selenium.dev_tools._functions import (
    validate_target_event_filter,
    validate_type_filter
)


if TYPE_CHECKING:
    from osn_selenium.dev_tools.domains import DomainsSettings
    from osn_selenium.dev_tools.settings import LoggerSettings
    from osn_selenium.dev_tools._types import (
        LogLevelsType,
        devtools_background_func_type
    )


class BaseMixin:
    """
    Base mixin for DevToolsTarget providing initialization, properties, and logging functionality.

    This class handles the core state of a DevTools target, including its data, logging channels,
    filter configurations, and synchronization primitives.

    Attributes:
        target_data (TargetData): The essential data identifying the target (id, type, url, etc.).
        websocket_url (Optional[str]): The WebSocket URL used to connect to this target.
        devtools_package (DevToolsPackage): The wrapper for the DevTools protocol module.
        exit_event (trio.Event): Event to signal global exit.
        started_event (trio.Event): Event set when the target handling has started.
        about_to_stop_event (trio.Event): Event set when the target is about to stop.
        stopped_event (trio.Event): Event set when the target handling has fully stopped.
        background_task_ended (Optional[trio.Event]): Event set when the background task completes.
    """

    def __init__(
            self,
            target_data: TargetData,
            logger_settings: "LoggerSettings",
            devtools_package: DevToolsPackage,
            websocket_url: Optional[str],
            new_targets_filter_list: Sequence[Dict[str, Any]],
            new_targets_buffer_size: int,
            domains: "DomainsSettings",
            nursery: trio.Nursery,
            exit_event: trio.Event,
            target_background_task: Optional["devtools_background_func_type"],
            add_target_func: Callable[[Any], Awaitable[bool]],
            remove_target_func: Callable[["BaseMixin"], Awaitable[Optional[bool]]],
            add_log_func: Callable[[TargetLogEntry], Awaitable[None]],
    ):
        """
        Initializes the BaseMixin.

        Args:
            target_data (TargetData): Information about the target.
            logger_settings ("LoggerSettings"): Configuration for logging.
            devtools_package (DevToolsPackage): Access to CDP commands and events.
            websocket_url (Optional[str]): The debugger URL.
            new_targets_filter_list (Sequence[Dict[str, Any]]): Filters for discovering new targets.
            new_targets_buffer_size (int): Buffer size for new target events.
            domains ("DomainsSettings"): Configuration for enabled domains and handlers.
            nursery (trio.Nursery): Trio nursery for background tasks.
            exit_event (trio.Event): Signal to stop all operations.
            target_background_task (Optional[devtools_background_func_type]): Optional background task to run.
            add_target_func (Callable[[Any], Awaitable[bool]]): Callback to add a new target.
            remove_target_func (Callable[["BaseMixin"], Awaitable[Optional[bool]]]): Callback to remove this target.
            add_log_func (Callable[[TargetLogEntry], Awaitable[None]]): Callback to record a log entry.
        """
        self.target_data = target_data
        self._logger_settings = logger_settings
        self.devtools_package = devtools_package
        self.websocket_url = websocket_url
        self._new_targets_filter_list = new_targets_filter_list
        self._new_targets_events_filters = validate_target_event_filter(new_targets_filter_list)
        self._new_targets_buffer_size = new_targets_buffer_size
        self._domains = domains
        self._nursery_object = nursery
        self.exit_event = exit_event

        self._target_type_log_accepted = validate_type_filter(
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
        self._log_stats.url = value
        self.target_data.url = value

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
        self._target_type_log_accepted = validate_type_filter(
                value,
                self._logger_settings.target_type_filter_mode,
                self._logger_settings.target_type_filter
        )
        self.target_data.type_ = value

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
        self._log_stats.title = value
        self.target_data.title = value

    @property
    def target_type_log_accepted(self) -> bool:
        """
        Checks if logging is accepted for this target type.

        Returns:
            bool: True if logging is allowed, False otherwise.
        """
        return self._target_type_log_accepted

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
        self._log_stats.target_id = value
        self.target_data.target_id = value

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

    async def log_step(
        self,
        message: str,
        extra_data: Optional[Dict[str, Any]] = None
    ):
        """
        Logs a 'step' or informational message at INFO level.

        Automatically includes the source function in the extra data.

        Args:
            message (str): The log message.
            extra_data (Optional[Dict[str, Any]]): Additional context data.
        """
        stack = inspect.stack()
        extra_data_ = {"source_function": " <- ".join(stack_.function for stack_ in stack[1:])}

        if extra_data is not None:
            extra_data_.update(extra_data)

        await self.log(level="INFO", message=message, extra_data=extra_data_)

    @property
    def log_stats(self) -> LoggerChannelStats:
        """
        Gets the logging statistics for this target channel.

        Returns:
            LoggerChannelStats: The statistics object.
        """
        return self._log_stats

    async def log_error(
        self,
        error: BaseException,
        extra_data: Optional[Dict[str, Any]] = None
    ):
        """
        Logs an error with exception traceback and context.

        Args:
            error (BaseException): The exception to log.
            extra_data (Optional[Dict[str, Any]]): Additional context data.
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

    async def log(
            self,
            level: "LogLevelsType",
            message: str,
            extra_data: Optional[Dict[str, Any]] = None
    ):
        """
        Records a log entry.

        If logging is accepted for this target type, the entry is sent to the target-specific
        logger channel.

        Args:
            level (LogLevelsType): The severity level (e.g., 'INFO', 'ERROR').
            message (str): The log message.
            extra_data (Optional[Dict[str, Any]]): Additional data to log.
        """
        log_entry = TargetLogEntry(
                target_data=self.target_data,
                message=message,
                level=level,
                datetime=datetime.now(),
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

    @property
    def cdp_session(self) -> CdpSession:
        """
        Gets the active CDP session for this target.

        Returns:
            CdpSession: The CDP session object.
        """
        return self._cdp_session

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
