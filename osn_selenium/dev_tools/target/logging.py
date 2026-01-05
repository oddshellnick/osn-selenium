import inspect
import warnings
from datetime import datetime
from typing import (
    Any,
    Dict,
    Optional,
    TYPE_CHECKING,
)

import trio

from osn_selenium.dev_tools.logger.target import (
    TargetLogEntry
)
from osn_selenium.dev_tools.logger.main import LoggerChannelStats
from osn_selenium.dev_tools.target.base import BaseMixin
from osn_selenium.dev_tools.exception_utils import (
    extract_exception_trace,
    log_exception
)


if TYPE_CHECKING:
    from osn_selenium.dev_tools._types import LogLevelsType


class LoggingMixin(BaseMixin):
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
