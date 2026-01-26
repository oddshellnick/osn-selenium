import trio
import inspect
import warnings
from datetime import datetime
from osn_selenium.dev_tools.target.base import BaseMixin
from osn_selenium.dev_tools.models import FingerprintData
from typing import (
	Any,
	Dict,
	Optional,
	TYPE_CHECKING
)
from osn_selenium.dev_tools._exception_helpers import (
	extract_exception_trace,
	log_exception
)
from osn_selenium.dev_tools.logger.models import (
	CDPTargetLogEntry,
	FingerprintTargetLogEntry
)


__all__ = ["LoggingMixin"]

if TYPE_CHECKING:
	from osn_selenium.dev_tools._typehints import CDP_LOG_LEVELS_TYPEHINT, FINGERPRINT_LOG_LEVELS_TYPEHINT


class LoggingMixin(BaseMixin):
	"""
	Mixin for handling logging operations within a DevTools target.
	"""
	
	async def log_cdp(
			self,
			level: "CDP_LOG_LEVELS_TYPEHINT",
			message: str,
			extra_data: Optional[Dict[str, Any]] = None
	):
		"""
		Records a CDP log entry.

		If logging is accepted for this target type, the entry is sent to the target-specific
		logger channel.

		Args:
			level (CDPLogLevelsType): The severity level (e.g., 'INFO', 'ERROR').
			message (str): The log message.
			extra_data (Optional[Dict[str, Any]]): Additional data to log.
		"""
		
		log_entry = CDPTargetLogEntry(
				target_data=self.target_data,
				message=message,
				level=level,
				datetime=datetime.now(),
				extra_data=extra_data
		)
		
		await self._add_cdp_log_func(log_entry)
		
		if self.target_type_log_accepted and self._logger is not None and self._logger_cdp_send_channel is not None:
			await self._cdp_log_stats.add_log(log_entry)
			await self._logger.run()
		
			try:
				if self._logger.filter_cdp_log(log_entry=log_entry):
					if self._logger_settings.cdp_settings.send_wait:
						await self._logger_cdp_send_channel.send(log_entry)
					else:
						self._logger_cdp_send_channel.send_nowait(log_entry)
			except trio.WouldBlock:
				warnings.warn(
						f"WARNING: Log channel for session {self.target_id} is full. Log dropped:\n{log_entry.model_dump_json(indent=4)}"
				)
			except trio.BrokenResourceError:
				warnings.warn(
						f"WARNING: Log channel for session {self.target_id} is broken. Log dropped:\n{log_entry.model_dump_json(indent=4)}"
				)
	
	async def log_cdp_error(self, error: BaseException, extra_data: Optional[Dict[str, Any]] = None):
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
		
		await self.log_cdp(
				level="ERROR",
				message=extract_exception_trace(error),
				extra_data=extra_data_
		)
		log_exception(exception=error, extra_data=extra_data_)
	
	async def log_cdp_step(self, message: str, extra_data: Optional[Dict[str, Any]] = None):
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
		
		await self.log_cdp(level="INFO", message=message, extra_data=extra_data_)
	
	async def log_fingerprint(self, level: "FINGERPRINT_LOG_LEVELS_TYPEHINT", data: FingerprintData):
		"""
		Records a fingerprint detection log entry.

		Args:
			level ("FingerprintLogLevelsType"): The log level (e.g., "Detect").
			data (FingerprintData): The detected fingerprint data.
		"""
		
		log_entry = FingerprintTargetLogEntry(
				target_data=self.target_data,
				level=level,
				api=data.api,
				used_method=data.used_method,
				datetime=datetime.now(),
				stacktrace=data.stacktrace,
		)
		
		await self._add_fingerprint_log_func(log_entry)
		
		if self.target_type_log_accepted and self._logger is not None and self._logger_fingerprint_send_channel is not None:
			await self._fingerprint_log_stats.add_log(log_entry)
			await self._logger.run()
		
			try:
				if self._logger.filter_fingerprint_log(log_entry=log_entry):
					if self._logger_settings.fingerprint_settings.send_wait:
						await self._logger_fingerprint_send_channel.send(log_entry)
					else:
						self._logger_fingerprint_send_channel.send_nowait(log_entry)
			except trio.WouldBlock:
				warnings.warn(
						f"WARNING: Log channel for session {self.target_id} is full. Log dropped:\n{log_entry.model_dump_json(indent=4)}"
				)
			except trio.BrokenResourceError:
				warnings.warn(
						f"WARNING: Log channel for session {self.target_id} is broken. Log dropped:\n{log_entry.model_dump_json(indent=4)}"
				)
