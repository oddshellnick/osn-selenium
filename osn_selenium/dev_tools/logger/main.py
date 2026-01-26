import trio
from typing import (
	Optional,
	TYPE_CHECKING,
	Tuple
)
from osn_selenium.exceptions.devtools import TrioEndExceptions
from osn_selenium.dev_tools._exception_helpers import log_exception
from osn_selenium.exceptions.configuration import ConfigurationError
from osn_selenium.dev_tools.logger.models import (
	CDPMainLogEntry,
	FingerprintMainLogEntry
)


__all__ = ["MainLogger", "build_main_logger"]

if TYPE_CHECKING:
	from osn_selenium.dev_tools.settings import LoggerSettings


class MainLogger:
	"""
	Manages the main log file, summarizing overall logging activity.

	This logger is responsible for writing aggregated statistics about all active
	logging channels and target types to a designated file.
	"""
	
	def __init__(
			self,
			logger_settings: "LoggerSettings",
			nursery_object: trio.Nursery,
			cdp_receive_channel: Optional[trio.MemoryReceiveChannel[CDPMainLogEntry]],
			fingerprint_receive_channel: Optional[trio.MemoryReceiveChannel[FingerprintMainLogEntry]]
	):
		"""
		Initializes the MainLogger.

		Args:
			logger_settings ("LoggerSettings"): The settings for logging, including log directory.
			nursery_object (trio.Nursery): The Trio nursery to spawn background tasks.
			cdp_receive_channel (Optional[trio.MemoryReceiveChannel[CDPMainLogEntry]]):
				The channel from which CDP main log entries are received.
			fingerprint_receive_channel (Optional[trio.MemoryReceiveChannel[FingerprintMainLogEntry]]):
				The channel from which fingerprint main log entries are received.

		Raises:
			ValueError: If settings require logging but `dir_path` is not set.
		"""
		
		self._nursery_object = nursery_object
		self._cdp_receive_channel = cdp_receive_channel
		self._fingerprint_receive_channel = fingerprint_receive_channel
		self._cdp_file_path = None
		self._cdp_log_level_filter = None
		self._cdp_target_type_filter = None
		self._fingerprint_file_path = None
		self._fingerprint_log_level_filter = None
		self._fingerprint_target_type_filter = None
		
		if logger_settings.dir_path is None:
			if logger_settings.cdp_settings:
				raise ConfigurationError("Can't log CDP without LoggerSettings.dir_path!")
			
			if logger_settings.fingerprint_settings:
				raise ConfigurationError("Can't log Fingerprint without LoggerSettings.dir_path!")
		else:
			logdir_path = logger_settings.dir_path.joinpath("__MAIN__")
			logdir_path.mkdir(exist_ok=True)
			
			if logger_settings.cdp_settings:
				self._cdp_file_path = logdir_path.joinpath(f"cdp_log.txt")
			
			if logger_settings.fingerprint_settings:
				self._fingerprint_file_path = logdir_path.joinpath(f"fingerprint_log.txt")
		
		self._cdp_file_writing_stopped: Optional[trio.Event] = None
		self._fingerprint_file_writing_stopped: Optional[trio.Event] = None
		self._is_active = False
	
	async def close(self):
		"""
		Closes the main logger, including its receive channels and stops writing tasks.
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
		Asynchronously writes fingerprint main log entries to the file.

		This method continuously receives `FingerprintMainLogEntry` objects and
		updates the log file.
		"""
		
		try:
			async with await trio.open_file(self._fingerprint_file_path, "w+", encoding="utf-8") as file:
				async for log_entry in self._fingerprint_receive_channel:
					await file.seek(0)
					await file.write(log_entry.model_dump_json(indent=4))
					await file.truncate()
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
		Asynchronously writes CDP main log entries to the file.

		This method continuously receives `CDPMainLogEntry` objects from its channel
		and overwrites the configured file with their string representation.
		It runs as a background task.
		"""
		
		try:
			async with await trio.open_file(self._cdp_file_path, "w+", encoding="utf-8") as file:
				async for log_entry in self._cdp_receive_channel:
					await file.seek(0)
					await file.write(log_entry.model_dump_json(indent=4))
					await file.truncate()
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
		Starts the main logger, setting up its receive channel and file writing task.

		Raises:
			BaseException: If an error occurs during setup or if the logger fails to activate.
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


def build_main_logger(nursery_object: trio.Nursery, logger_settings: "LoggerSettings") -> Tuple[
	Optional[trio.MemorySendChannel[CDPMainLogEntry]],
	Optional[trio.MemorySendChannel[FingerprintMainLogEntry]],
	MainLogger
]:
	"""
	Builds and initializes a `MainLogger` instance along with its send channels.

	Args:
		nursery_object (trio.Nursery): The Trio nursery to associate with the logger for background tasks.
		logger_settings ("LoggerSettings"): The logger configuration settings.

	Returns:
		Tuple[Optional[trio.MemorySendChannel[CDPMainLogEntry]], Optional[trio.MemorySendChannel[FingerprintMainLogEntry]], MainLogger]:
			A tuple containing the send channels for logs and the initialized `MainLogger` instance.
	"""
	
	if logger_settings.cdp_settings is not None:
		cdp_send, cdp_recv = trio.open_memory_channel(logger_settings.cdp_settings.buffer_size)
	else:
		cdp_send, cdp_recv = None, None
	
	if logger_settings.fingerprint_settings is not None:
		fp_send, fp_recv = trio.open_memory_channel(logger_settings.fingerprint_settings.buffer_size)
	else:
		fp_send, fp_recv = None, None
	
	target_logger = MainLogger(
			logger_settings=logger_settings,
			nursery_object=nursery_object,
			cdp_receive_channel=cdp_recv,
			fingerprint_receive_channel=fp_recv,
	)
	
	return cdp_send, fp_send, target_logger
