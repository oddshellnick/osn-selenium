import trio
import pathlib
from typing import (
	Callable,
	Optional,
	Tuple
)
from osn_selenium.dev_tools.models import TargetData
from osn_selenium.dev_tools.settings import LoggerSettings
from osn_selenium.exceptions.devtools import TrioEndExceptions
from osn_selenium.dev_tools._validators import validate_log_filter
from osn_selenium.dev_tools._exception_helpers import log_exception
from osn_selenium.dev_tools.logger.models import (
	CDPTargetLogEntry,
	FingerprintTargetLogEntry
)


__all__ = ["TargetLogger", "build_target_logger"]


class TargetLogger:
	"""
	Manages logging for a specific browser target (e.g., a tab or iframe).

	Each `TargetLogger` instance is responsible for writing log entries
	related to its associated `TargetData` to a dedicated file.
	"""
	
	def __init__(
			self,
			logger_settings: LoggerSettings,
			nursery_object: trio.Nursery,
			target_data: TargetData,
			cdp_receive_channel: Optional[trio.MemoryReceiveChannel[CDPTargetLogEntry]],
			fingerprint_receive_channel: Optional[trio.MemoryReceiveChannel[FingerprintTargetLogEntry]],
	):
		"""
		Initializes the TargetLogger.

		Args:
			logger_settings (LoggerSettings): Configuration for logging.
			nursery_object (trio.Nursery): The Trio nursery to spawn background tasks.
			target_data (TargetData): The data of the browser target this logger will log for.
			cdp_receive_channel (Optional[trio.MemoryReceiveChannel[CDPTargetLogEntry]]):
				Channel to receive CDP logs.
			fingerprint_receive_channel (Optional[trio.MemoryReceiveChannel[FingerprintTargetLogEntry]]):
				Channel to receive fingerprint logs.

		Raises:
			ValueError: If settings require logging but `dir_path` is not set.
		"""
		
		self._target_data = target_data
		self._nursery_object = nursery_object
		self._cdp_receive_channel = cdp_receive_channel
		self._fingerprint_receive_channel = fingerprint_receive_channel
		self._cdp_file_path: Optional[pathlib.Path] = None
		self._cdp_log_level_filter: Optional[Callable[[str], bool]] = None
		self._cdp_target_type_filter: Optional[Callable[[str], bool]] = None
		self._fingerprint_file_path: Optional[pathlib.Path] = None
		self._fingerprint_log_level_filter: Optional[Callable[[str], bool]] = None
		self._fingerprint_target_type_filter: Optional[Callable[[str], bool]] = None
		
		if logger_settings.dir_path is None:
			if logger_settings.cdp_settings:
				raise ValueError("Can't log CDP without LoggerSettings.dir_path!")
			
			if logger_settings.fingerprint_settings:
				raise ValueError("Can't log Fingerprint without LoggerSettings.log_dir_path!")
		else:
			logdir_path = logger_settings.dir_path.joinpath(target_data.target_id)
			logdir_path.mkdir(exist_ok=True)
			
			if logger_settings.cdp_settings:
				self._cdp_file_path = logdir_path.joinpath(f"cdp_log.txt")
				
				self._cdp_log_level_filter = validate_log_filter(
						logger_settings.cdp_settings.log_level_filter_mode,
						logger_settings.cdp_settings.log_level_filter
				)
				
				self._cdp_target_type_filter = validate_log_filter(
						logger_settings.cdp_settings.target_type_filter_mode,
						logger_settings.cdp_settings.target_type_filter
				)
			
			if logger_settings.fingerprint_settings:
				self._fingerprint_file_path = logdir_path.joinpath(f"fingerprint_log.txt")
				
				self._fingerprint_log_level_filter = validate_log_filter(
						logger_settings.fingerprint_settings.log_level_filter_mode,
						logger_settings.fingerprint_settings.log_level_filter
				)
				
				self._fingerprint_category_filter = validate_log_filter(
						logger_settings.fingerprint_settings.category_filter_mode,
						logger_settings.fingerprint_settings.category_filter
				)
		
		self._cdp_file_writing_stopped: Optional[trio.Event] = None
		self._fingerprint_file_writing_stopped: Optional[trio.Event] = None
		self._is_active = False
	
	def filter_cdp_log(self, log_entry: CDPTargetLogEntry) -> bool:
		"""
		Applies configured filters to a CDP log entry.

		Args:
			log_entry (CDPTargetLogEntry): The log entry to check.

		Returns:
			bool: True if the log entry passes filters, False otherwise.
		"""
		
		return self._cdp_log_level_filter(log_entry.level) and self._cdp_target_type_filter(log_entry.target_data.type_)
	
	def filter_fingerprint_log(self, log_entry: FingerprintTargetLogEntry) -> bool:
		"""
		Applies configured filters to a fingerprint log entry.

		Args:
			log_entry (FingerprintTargetLogEntry): The log entry to check.

		Returns:
			bool: True if the log entry passes filters, False otherwise.
		"""
		
		return self._fingerprint_log_level_filter(log_entry.level) and self._fingerprint_category_filter(log_entry.api)
	
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
		Closes the target logger, including its receive channels and stops writing tasks.
		"""
		
		if self._cdp_receive_channel is not None:
			await self._cdp_receive_channel.aclose()
			self._cdp_receive_channel = None
		
		if self._cdp_file_writing_stopped is not None:
			await self._cdp_file_writing_stopped.wait()
			self._cdp_file_writing_stopped = None
		
		if self._fingerprint_receive_channel is not None:
			await self._fingerprint_receive_channel.aclose()
			self._fingerprint_receive_channel = None
		
		if self._fingerprint_file_writing_stopped is not None:
			await self._fingerprint_file_writing_stopped.wait()
			self._fingerprint_file_writing_stopped = None
		
		self._is_active = False
	
	async def _write_fingerprint_file(self):
		"""
		Asynchronously writes fingerprint log entries to the target-specific file.

		This method continuously receives `FingerprintTargetLogEntry` objects,
		filters them, and appends them to the log file.
		"""
		
		try:
			end_of_entry = "\n\n" + "=" * 100 + "\n\n"
		
			async with await trio.open_file(self._fingerprint_file_path, "a+", encoding="utf-8") as file:
				async for log_entry in self._fingerprint_receive_channel:
					await file.write(log_entry.model_dump_json(indent=4) + end_of_entry)
					await file.flush()
		except* TrioEndExceptions:
			pass
		except* BaseException as error:
			log_exception(error)
		finally:
			if self._fingerprint_file_writing_stopped is not None:
				self._fingerprint_file_writing_stopped.set()
	
	async def _write_cdp_file(self):
		"""
		Asynchronously writes CDP log entries to the target-specific file.

		This method continuously receives `CDPTargetLogEntry` objects from its channel
		and appends their string representation to the configured file,
		applying log level and target type filters.
		It runs as a background task.
		"""
		
		try:
			end_of_entry = "\n\n" + "=" * 100 + "\n\n"
		
			async with await trio.open_file(self._cdp_file_path, "a+", encoding="utf-8") as file:
				async for log_entry in self._cdp_receive_channel:
					await file.write(log_entry.model_dump_json(indent=4) + end_of_entry)
					await file.flush()
		except* TrioEndExceptions:
			pass
		except* BaseException as error:
			log_exception(error)
		finally:
			if self._cdp_file_writing_stopped is not None:
				self._cdp_file_writing_stopped.set()
	
	async def run(self):
		"""
		Starts the target logger, setting up its receive channel and file writing task.
		"""
		
		try:
			if not self._is_active:
				self._cdp_file_writing_stopped = trio.Event()
		
				if self._cdp_file_path is not None:
					self._nursery_object.start_soon(self._write_cdp_file)
		
				self._fingerprint_file_writing_stopped = trio.Event()
		
				if self._fingerprint_file_path is not None:
					self._nursery_object.start_soon(self._write_fingerprint_file)
		
				self._is_active = True
		except* TrioEndExceptions:
			await self.close()
		except* BaseException as error:
			log_exception(error)
			await self.close()


def build_target_logger(
		target_data: TargetData,
		nursery_object: trio.Nursery,
		logger_settings: LoggerSettings
) -> Tuple[
	Optional[trio.MemorySendChannel[CDPTargetLogEntry]],
	Optional[trio.MemorySendChannel[FingerprintTargetLogEntry]],
	TargetLogger
]:
	"""
	Builds and initializes a `TargetLogger` instance.

	Args:
		target_data (TargetData): Data associated with the target.
		nursery_object (trio.Nursery): Trio nursery for background tasks.
		logger_settings (LoggerSettings): Logger configuration.

	Returns:
		Tuple[Optional[trio.MemorySendChannel[CDPTargetLogEntry]], Optional[trio.MemorySendChannel[FingerprintTargetLogEntry]], TargetLogger]:
			Tuple containing send channels for logs and the initialized logger instance.
	"""
	
	if logger_settings.cdp_settings is not None:
		cdp_send, cdp_recv = trio.open_memory_channel(logger_settings.cdp_settings.buffer_size)
	else:
		cdp_send, cdp_recv = None, None
	
	if logger_settings.fingerprint_settings is not None:
		fp_send, fp_recv = trio.open_memory_channel(logger_settings.fingerprint_settings.buffer_size)
	else:
		fp_send, fp_recv = None, None
	
	target_logger = TargetLogger(
			logger_settings=logger_settings,
			nursery_object=nursery_object,
			target_data=target_data,
			cdp_receive_channel=cdp_recv,
			fingerprint_receive_channel=fp_recv,
	)
	
	return cdp_send, fp_send, target_logger
