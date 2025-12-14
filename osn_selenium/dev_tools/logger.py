from __future__ import annotations

import trio
from pathlib import Path
from datetime import datetime
from osn_selenium.types import DictModel
from osn_selenium.dev_tools._types import LogLevelsType
from osn_selenium.dev_tools.errors import trio_end_exceptions
from typing import (
	Any,
	Dict,
	Literal,
	Optional,
	Sequence,
	Tuple,
	Union
)
from osn_selenium.dev_tools.utils import (
	TargetData,
	_validate_log_filter,
	log_exception
)


class LoggerSettings(DictModel):
	"""
	Settings for configuring the LoggerManager.

	Attributes:
		log_dir_path (Optional[Path]): The base directory where log files will be stored.
			If None, logging will only happen in memory and not be written to files.
			Defaults to None.
		renew_log (bool): If True and `log_dir_path` is provided, the log directory
			will be cleared (recreated) on initialization. Defaults to True.
		log_level_filter_mode (Literal["exclude", "include"]): The mode for filtering log levels.
			"exclude" means log levels in `log_level_filter` will be excluded.
			"include" means only log levels in `log_level_filter` will be included.
			Defaults to "exclude".
		log_level_filter (Optional[Union[LogLevelsType, Sequence[LogLevelsType]]]):
			A single log level or a sequence of log levels to filter by.
			Used in conjunction with `log_level_filter_mode`. Defaults to None.
		target_type_filter_mode (Literal["exclude", "include"]): The mode for filtering target types.
			"exclude" means target types in `target_type_filter` will be excluded.
			"include" means only target types in `target_type_filter` will be included.
			Defaults to "exclude".
		target_type_filter (Optional[Union[str, Sequence[str]]]):
			A single target type string or a sequence of target type strings to filter by.
			Used in conjunction with `target_type_filter_mode`. Defaults to None.
	"""
	
	log_dir_path: Optional[Path] = None
	renew_log: bool = True
	log_level_filter_mode: Literal["exclude", "include"] = "exclude"
	log_level_filter: Optional[Union[LogLevelsType, Sequence[LogLevelsType]]] = None
	target_type_filter_mode: Literal["exclude", "include"] = "exclude"
	target_type_filter: Optional[Union[str, Sequence[str]]] = None


class LogEntry(DictModel):
	"""
	Represents a single log entry with detailed information.

	Attributes:
		target_data (TargetData): Data about the target (browser tab/session) from which the log originated.
		message (str): The main log message.
		level (LogLevelsType): The severity level of the log (e.g., "INFO", "ERROR").
		timestamp (datetime): The exact time when the log entry was created.
		extra_data (Optional[Dict[str, Any]]): Optional additional data associated with the log.
	"""
	
	target_data: TargetData
	message: str
	level: LogLevelsType
	timestamp: datetime
	extra_data: Optional[Dict[str, Any]] = None


class TargetLogger:
	"""
	Manages logging for a specific browser target (e.g., a tab or iframe).

	Each `TargetLogger` instance is responsible for writing log entries
	related to its associated `TargetData` to a dedicated file.

	Attributes:
		_target_data (TargetData): The data of the browser target this logger is associated with.
		_nursery_object (trio.Nursery): The Trio nursery for managing concurrent tasks.
		_receive_channel (trio.MemoryReceiveChannel[LogEntry]): The receive channel for log entries specific to this target.
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
			receive_channel: trio.MemoryReceiveChannel[LogEntry],
			logger_settings: LoggerSettings,
	):
		"""
		Initializes the TargetLogger.

		Args:
			target_data (TargetData): The data of the browser target this logger will log for.
			nursery_object (trio.Nursery): The Trio nursery to spawn background tasks.
		"""
		
		self._target_data = target_data
		self._nursery_object = nursery_object
		self._receive_channel = receive_channel
		
		self._log_level_filter = _validate_log_filter(
				logger_settings.log_level_filter_mode,
				logger_settings.log_level_filter
		)
		
		self._target_type_filter = _validate_log_filter(
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
) -> Tuple[trio.MemorySendChannel[LogEntry], TargetLogger]:
	"""
	Builds and initializes a `TargetLogger` instance along with its send channel.

	Args:
		target_data (TargetData): The data for the target this logger will serve.
		nursery_object (trio.Nursery): The Trio nursery to associate with the logger for background tasks.
		logger_settings (LoggerSettings): The logger configuration settings.

	Returns:
		Tuple[trio.MemorySendChannel[LogEntry], TargetLogger]: A tuple containing
			the send channel for `LogEntry` objects and the initialized `TargetLogger` instance.
	"""
	
	send_channel, receive_channel = trio.open_memory_channel(1000)
	target_logger = TargetLogger(target_data, nursery_object, receive_channel, logger_settings)
	
	return send_channel, target_logger


class LogLevelStats(DictModel):
	"""
	Dataclass to store statistics for a specific log level.

	Attributes:
		num_logs (int): The total number of logs recorded for this level.
		last_log_time (datetime): The timestamp of the most recent log entry for this level.
	"""
	
	num_logs: int
	last_log_time: datetime


class LoggerChannelStats(DictModel):
	"""
	Dataclass to store statistics for a specific logging channel (per target).

	Attributes:
		target_id (str): The unique ID of the target associated with this channel.
		title (str): The title of the target (e.g., page title).
		url (str): The URL of the target.
		num_logs (int): The total number of log entries for this channel.
		last_log_time (datetime): The timestamp of the most recent log entry for this channel.
		log_level_stats (Dict[str, LogLevelStats]): A dictionary mapping log levels to their specific statistics.
	"""
	
	target_id: str
	title: str
	url: str
	num_logs: int
	last_log_time: datetime
	log_level_stats: Dict[str, LogLevelStats]
	
	async def add_log(self, log_entry: LogEntry):
		"""
		Updates the channel statistics based on a new log entry.

		Args:
			log_entry (LogEntry): The new log entry to incorporate into the statistics.
		"""
		
		self.num_logs += 1
		self.last_log_time = log_entry.timestamp
		
		if log_entry.level not in self.log_level_stats:
			self.log_level_stats[log_entry.level] = LogLevelStats(num_logs=1, last_log_time=log_entry.timestamp)
		else:
			self.log_level_stats[log_entry.level].num_logs += 1
			self.log_level_stats[log_entry.level].last_log_time = log_entry.timestamp


class TargetTypeStats(DictModel):
	"""
	Dataclass to store statistics for a specific target type.

	Attributes:
		num_targets (int): The count of targets of this type.
	"""
	
	num_targets: int


class MainLogEntry(DictModel):
	"""
	Represents a summary log entry for the entire logging system.

	Attributes:
		num_channels (int): The total number of active logging channels (targets).
		targets_types_stats (Dict[str, TargetTypeStats]): Statistics grouped by target type.
		num_logs (int): The total number of log entries across all channels.
		log_level_stats (Dict[str, LogLevelStats]): Overall statistics for each log level.
		channels_stats (Sequence[LoggerChannelStats]): A List of statistics for each active logging channel.
	"""
	
	num_channels: int
	targets_types_stats: Dict[str, TargetTypeStats]
	num_logs: int
	log_level_stats: Dict[str, LogLevelStats]
	channels_stats: Sequence[LoggerChannelStats]


class MainLogger:
	"""
	Manages the main log file, summarizing overall logging activity.

	This logger is responsible for writing aggregated statistics about all active
	logging channels and target types to a designated file.

	Attributes:
		_nursery_object (trio.Nursery): The Trio nursery for managing concurrent tasks.
		_receive_channel (trio.MemoryReceiveChannel[MainLogEntry]): The receive channel for main log entries.
		_file_writing_stopped (Optional[trio.Event]): An event set when the file writing task stops.
		_is_active (bool): Flag indicating if the main logger is active.
		_file_path (Optional[Path]): The path to the main log file.
	"""
	
	def __init__(
			self,
			logger_settings: LoggerSettings,
			nursery_object: trio.Nursery,
			receive_channel: trio.MemoryReceiveChannel[MainLogEntry]
	):
		"""
		Initializes the MainLogger.

		Args:
			logger_settings (LoggerSettings): The settings for logging, including log directory.
			nursery_object (trio.Nursery): The Trio nursery to spawn background tasks.
			receive_channel (trio.MemoryReceiveChannel[MainLogEntry]): The channel from which main log entries are received.
		"""
		
		self._nursery_object = nursery_object
		self._receive_channel = receive_channel
		self._file_writing_stopped: Optional[trio.Event] = None
		self._is_active = False
		
		if logger_settings.log_dir_path is None:
			self._file_path = None
		else:
			self._file_path = logger_settings.log_dir_path.joinpath("__MAIN__.txt")
	
	async def close(self):
		"""
		Closes the main logger, including its receive channel.
		"""
		
		if self._receive_channel is not None:
			await self._receive_channel.aclose()
			self._receive_channel = None
		
		if self._file_writing_stopped is not None:
			await self._file_writing_stopped.wait()
		
		self._is_active = False
	
	async def _write_file(self):
		"""
		Asynchronously writes main log entries to the file.

		This method continuously receives `MainLogEntry` objects from its channel
		and overwrites the configured file with their string representation.
		It runs as a background task.

		Raises:
			BaseException: If an unexpected error occurs during file writing.
		"""
		
		try:
			async with await trio.open_file(self._file_path, "w+", encoding="utf-8") as file:
				async for log_entry in self._receive_channel:
					await file.seek(0)
					await file.write(log_entry.model_dump_json(indent=4))
					await file.truncate()
					await file.flush()
		except* trio_end_exceptions:
			pass
		except* BaseException as error:
			log_exception(error)
		finally:
			if self._file_writing_stopped is not None:
				self._file_writing_stopped.set()
	
	async def run(self):
		"""
		Starts the main logger, setting up its receive channel and file writing task.

		Raises:
			BaseException: If an error occurs during setup or if the logger fails to activate.
		"""
		
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


def build_main_logger(nursery_object: trio.Nursery, logger_settings: LoggerSettings) -> Tuple[trio.MemorySendChannel[MainLogEntry], MainLogger]:
	"""
	Builds and initializes a `MainLogger` instance along with its send channel.

	Args:
		nursery_object (trio.Nursery): The Trio nursery to associate with the logger for background tasks.
		logger_settings (LoggerSettings): The logger configuration settings.

	Returns:
		Tuple[trio.MemorySendChannel[MainLogEntry], MainLogger]: A tuple containing
			the send channel for `MainLogEntry` objects and the initialized `MainLogger` instance.
	"""
	
	send_channel, receive_channel = trio.open_memory_channel(1000)
	target_logger = MainLogger(logger_settings, nursery_object, receive_channel)
	
	return send_channel, target_logger


LoggerSettings.model_rebuild()
LogEntry.model_rebuild()
LogLevelStats.model_rebuild()
LoggerChannelStats.model_rebuild()
TargetTypeStats.model_rebuild()
MainLogEntry.model_rebuild()
