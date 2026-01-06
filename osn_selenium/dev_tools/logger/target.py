import trio
from datetime import datetime
from osn_selenium.types import DictModel
from osn_selenium.dev_tools.utils import TargetData
from typing import (
	Any,
	Dict,
	Optional,
	Tuple
)
from osn_selenium.dev_tools._types import LogLevelsType
from osn_selenium.dev_tools.settings import LoggerSettings
from osn_selenium.dev_tools.errors import trio_end_exceptions
from osn_selenium.dev_tools.exception_utils import log_exception
from osn_selenium.dev_tools.logger.functions import validate_log_filter


class TargetLogEntry(DictModel):
	"""
	Represents a single log entry with detailed information.

	Attributes:
		target_data (TargetData): Data about the target (browser tab/session) from which the log originated.
		message (str): The main log message.
		level (LogLevelsType): The severity level of the log (e.g., "INFO", "ERROR").
		datetime (datetime): The exact time when the log entry was created.
		extra_data (Optional[Dict[str, Any]]): Optional additional data associated with the log.
	"""
	
	target_data: TargetData
	message: str
	level: LogLevelsType
	datetime: datetime
	extra_data: Optional[Dict[str, Any]] = None


class TargetLogger:
	"""
	Manages logging for a specific browser target (e.g., a tab or iframe).

	Each `TargetLogger` instance is responsible for writing log entries
	related to its associated `TargetData` to a dedicated file.

	Attributes:
		_target_data (TargetData): The data of the browser target this logger is associated with.
		_nursery_object (trio.Nursery): The Trio nursery for managing concurrent tasks.
		_receive_channel (trio.MemoryReceiveChannel[TargetLogEntry]): The receive channel for log entries specific to this target.
		_log_level_filter (Callable[[Any], bool]): Filter function for log levels.
		_target_type_filter (Callable[[Any], bool]): Filter function for target types.
		_file_writing_stopped (Optional[trio.Event]): An event set when file writing task stops.
		_file_path (Optional[Path]): The path to the target-specific log file.
		_is_active (bool): Flag indicating if the target logger is active.
	"""
	
	def __init__(
			self,
			target_data: TargetData,
			nursery_object: trio.Nursery,
			receive_channel: trio.MemoryReceiveChannel[TargetLogEntry],
			logger_settings: LoggerSettings,
	):
		"""
		Initializes the TargetLogger.

		Args:
			target_data (TargetData): The data of the browser target this logger will log for.
			nursery_object (trio.Nursery): The Trio nursery to spawn background tasks.
			receive_channel (trio.MemoryReceiveChannel[TargetLogEntry]): Channel to receive logs.
			logger_settings (LoggerSettings): Configuration for logging.
		"""
		
		self._target_data = target_data
		self._nursery_object = nursery_object
		self._receive_channel = receive_channel
		
		self._log_level_filter = validate_log_filter(
				logger_settings.log_level_filter_mode,
				logger_settings.log_level_filter
		)
		
		self._target_type_filter = validate_log_filter(
				logger_settings.target_type_filter_mode,
				logger_settings.target_type_filter
		)
		
		self._file_writing_stopped: Optional[trio.Event] = None
		
		if logger_settings.log_dir_path is None:
			self._file_path = None
		else:
			self._file_path = logger_settings.log_dir_path.joinpath(f"{target_data.target_id}.txt")
			
			if self._file_path.exists():
				with open(self._file_path, "w", encoding="utf-8") as file:
					file.write("")
		
		self._is_active = False
	
	@property
	def is_active(self) -> bool:
		"""
		Checks if the target logger is currently active.

		Returns:
			bool: True if the logger is active and running, False otherwise.
		"""
		
		return self._is_active
	
	async def close(self):
		"""
		Closes the target logger, including its receive channel.
		"""
		
		if self._receive_channel is not None:
			await self._receive_channel.aclose()
			self._receive_channel = None
		
		if self._file_writing_stopped is not None:
			await self._file_writing_stopped.wait()
			self._file_writing_stopped = None
		
		self._is_active = False
	
	async def _write_file(self):
		"""
		Asynchronously writes log entries to the target-specific file.

		This method continuously receives `LogEntry` objects from its channel
		and appends their string representation to the configured file,
		applying log level and target type filters.
		It runs as a background task.

		Raises:
			BaseException: If an unexpected error occurs during file writing.
		"""
		
		try:
			end_of_entry = "\n\n" + "=" * 100 + "\n\n"
		
			async with await trio.open_file(self._file_path, "a+", encoding="utf-8") as file:
				async for log_entry in self._receive_channel:
					if self._log_level_filter(log_entry.level) and self._target_type_filter(log_entry.target_data.type_):
						await file.write(log_entry.model_dump_json(indent=4) + end_of_entry)
						await file.flush()
		except* trio_end_exceptions:
			pass
		except* BaseException as error:
			log_exception(error)
		finally:
			if self._file_writing_stopped is not None:
				self._file_writing_stopped.set()
	
	async def run(self):
		"""Starts the target logger, setting up its receive channel and file writing task."""
		
		try:
			if not self._is_active:
				self._file_writing_stopped = trio.Event()
		
				if self._file_path is not None:
					self._nursery_object.start_soon(self._write_file,)
		
				self._is_active = True
		except* trio_end_exceptions:
			await self.close()
		except* BaseException as error:
			log_exception(error)
			await self.close()


def build_target_logger(
		target_data: TargetData,
		nursery_object: trio.Nursery,
		logger_settings: LoggerSettings
) -> Tuple[trio.MemorySendChannel[TargetLogEntry], TargetLogger]:
	"""
	Builds and initializes a `TargetLogger` instance along with its send channel.

	Args:
		target_data (TargetData): The data for the target this logger will serve.
		nursery_object (trio.Nursery): The Trio nursery to associate with the logger for background tasks.
		logger_settings (LoggerSettings): The logger configuration settings.

	Returns:
		Tuple[trio.MemorySendChannel[TargetLogEntry], TargetLogger]: A tuple containing
			the send channel for `LogEntry` objects and the initialized `TargetLogger` instance.
	"""
	
	send_channel, receive_channel = trio.open_memory_channel(1000)
	target_logger = TargetLogger(target_data, nursery_object, receive_channel, logger_settings)
	
	return send_channel, target_logger
