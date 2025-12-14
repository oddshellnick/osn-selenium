import trio
from osn_selenium.dev_tools.manager.base import BaseMixin
from osn_selenium.dev_tools.errors import cdp_end_exceptions
from osn_selenium.dev_tools.logger.target import TargetLogEntry
from osn_selenium.dev_tools.exception_utils import log_exception
from osn_selenium.dev_tools.logger.main import (
	LogLevelStats,
	MainLogEntry
)


class LoggingMixin(BaseMixin):
	"""
	Mixin for aggregating logs from all targets in the DevTools manager.
	"""
	
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
	
	async def _add_log(self, log_entry: TargetLogEntry):
		"""
		Updates internal logging statistics based on a new log entry.

		This method increments total log counts and updates per-channel and per-level statistics.
		It also triggers an update to the main logger.

		Args:
			log_entry (TargetLogEntry): The log entry to use for updating statistics.

		Raises:
			BaseException: Catches and logs any unexpected errors during the log aggregation process.
		"""
		
		try:
			self._num_logs += 1
		
			if log_entry.level not in self._log_level_stats:
				self._log_level_stats[log_entry.level] = LogLevelStats(num_logs=1, last_log_time=log_entry.datetime)
			else:
				self._log_level_stats[log_entry.level].num_logs += 1
				self._log_level_stats[log_entry.level].last_log_time = log_entry.datetime
		
			await self._main_log()
		except cdp_end_exceptions:
			pass
		except BaseException as error:
			log_exception(error)
			raise error
