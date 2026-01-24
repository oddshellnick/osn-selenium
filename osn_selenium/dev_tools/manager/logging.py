import trio
from osn_selenium.dev_tools.manager.base import BaseMixin
from osn_selenium.exceptions.devtools import CDPEndExceptions
from osn_selenium.dev_tools._exception_helpers import log_exception
from osn_selenium.dev_tools.logger.models import (
	CDPLogLevelStats,
	CDPMainLogEntry,
	CDPTargetLogEntry,
	FingerprintAPIStats,
	FingerprintLogLevelStats,
	FingerprintMainLogEntry,
	FingerprintTargetLogEntry
)


__all__ = ["LoggingMixin"]


class LoggingMixin(BaseMixin):
	"""
	Mixin for aggregating logs from all targets in the DevTools manager.
	"""
	
	async def _add_main_cdp_log(self):
		"""
		Sends updated overall logging statistics to the main logger.

		This method constructs a `MainLogEntry` with current statistics and
		sends it to the `_main_logger_send_channel`. If the channel buffer is full,
		the log is dropped silently.

		Raises:
			CDPEndExceptions: If a CDP connection error occurs.
			BaseException: If any other error occurs during logging.
		"""
		
		try:
			if self._main_logger_cdp_send_channel is not None and self._main_logger is not None:
				log_entry = CDPMainLogEntry(
						num_channels=len(self._handling_targets),
						targets_types_stats=self._cdp_targets_types_stats,
						num_logs=self._num_cdp_logs,
						log_level_stats=self._cdp_log_level_stats,
						channels_stats=[
							target.cdp_log_stats
							for target in self._handling_targets.values()
							if target.target_type_log_accepted
						],
				)
		
				self._main_logger_cdp_send_channel.send_nowait(log_entry)
		except (trio.WouldBlock, trio.BrokenResourceError):
			pass
		except CDPEndExceptions as error:
			raise error
		except BaseException as error:
			log_exception(error)
			raise error
	
	async def _add_cdp_log(self, log_entry: CDPTargetLogEntry):
		"""
		Updates internal logging statistics based on a new log entry.

		This method increments total log counts and updates per-channel and per-level statistics.
		It also triggers an update to the main logger.

		Args:
			log_entry (CDPTargetLogEntry): The log entry to use for updating statistics.

		Raises:
			BaseException: Catches and logs any unexpected errors during the log aggregation process.
		"""
		
		try:
			self._num_cdp_logs += 1
		
			if log_entry.level not in self._cdp_log_level_stats:
				self._cdp_log_level_stats[log_entry.level] = CDPLogLevelStats(num_logs=1, last_log_time=log_entry.datetime)
			else:
				self._cdp_log_level_stats[log_entry.level].num_logs += 1
				self._cdp_log_level_stats[log_entry.level].last_log_time = log_entry.datetime
		
			await self._add_main_cdp_log()
		except CDPEndExceptions:
			pass
		except BaseException as error:
			log_exception(error)
			raise error
	
	async def _add_main_fingerprint_log(self):
		"""
		Sends updated overall fingerprint logging statistics to the main logger.

		Raises:
			CDPEndExceptions: If a CDP connection error occurs.
			BaseException: If any other error occurs during logging.
		"""
		
		try:
			if self._main_logger_fingerprint_send_channel is not None and self._main_logger is not None:
				log_entry = FingerprintMainLogEntry(
						num_channels=len(self._handling_targets),
						apis_stats=self._fingerprint_categories_stats,
						num_logs=self._num_fingerprint_logs,
						log_level_stats=self._fingerprint_log_level_stats,
						channels_stats=[
							target.fingerprint_log_stats
							for target in self._handling_targets.values()
							if target.target_type_log_accepted
						],
				)
		
				self._main_logger_fingerprint_send_channel.send_nowait(log_entry)
		except (trio.WouldBlock, trio.BrokenResourceError):
			pass
		except CDPEndExceptions as error:
			raise error
		except BaseException as error:
			log_exception(error)
			raise error
	
	async def _add_fingerprint_log(self, log_entry: FingerprintTargetLogEntry):
		"""
		Updates internal fingerprint logging statistics based on a new log entry.

		Args:
			log_entry (FingerprintTargetLogEntry): The log entry to use for updating statistics.

		Raises:
			BaseException: Catches and logs any unexpected errors during the log aggregation process.
		"""
		
		try:
			self._num_fingerprint_logs += 1
		
			if log_entry.level not in self._fingerprint_log_level_stats:
				self._fingerprint_log_level_stats[log_entry.level] = FingerprintLogLevelStats(num_logs=1, last_log_time=log_entry.datetime)
			else:
				self._fingerprint_log_level_stats[log_entry.level].num_logs += 1
				self._fingerprint_log_level_stats[log_entry.level].last_log_time = log_entry.datetime
		
			if log_entry.api not in self._fingerprint_categories_stats:
				self._fingerprint_categories_stats[log_entry.api] = FingerprintAPIStats(num_logs=1, methods_stats={log_entry.used_method: 1})
			else:
				self._fingerprint_categories_stats[log_entry.api].num_logs += 1
				self._fingerprint_categories_stats[log_entry.api].methods_stats[log_entry.used_method] = self._fingerprint_categories_stats[log_entry.api].methods_stats.get(log_entry.used_method, 0) + 1
		
			await self._add_main_fingerprint_log()
		except CDPEndExceptions:
			pass
		except BaseException as error:
			log_exception(error)
			raise error
