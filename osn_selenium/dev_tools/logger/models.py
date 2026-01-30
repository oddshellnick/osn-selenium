from pydantic import Field
from datetime import datetime
from osn_selenium._base_models import DictModel
from osn_selenium.dev_tools.models import TargetData
from typing import (
	Any,
	Dict,
	Optional,
	Sequence
)
from osn_selenium.dev_tools._typehints import (
	CDP_LOG_LEVELS_TYPEHINT,
	FINGERPRINT_LOG_LEVELS_TYPEHINT
)


__all__ = [
	"CDPLogLevelStats",
	"CDPLoggerChannelStats",
	"CDPMainLogEntry",
	"CDPTargetLogEntry",
	"CDPTargetTypeStats",
	"FingerprintAPIStats",
	"FingerprintLogLevelStats",
	"FingerprintLoggerChannelStats",
	"FingerprintMainLogEntry",
	"FingerprintTargetLogEntry"
]


class FingerprintLogLevelStats(DictModel):
	"""
	Statistics for a specific fingerprint log level.

	Attributes:
		num_logs (int): Number of logs recorded.
		last_log_time (datetime): Timestamp of the last log.
	"""
	
	num_logs: int
	last_log_time: datetime


class FingerprintTargetLogEntry(DictModel):
	"""
	A single log entry for fingerprint detection events.

	Attributes:
		target_data (TargetData): Information about the target.
		level (FingerprintLogLevelsType): The log level (e.g., "Detect").
		api (str): The API involved in the fingerprinting.
		used_method (str): The method called.
		datetime (datetime): When the event occurred.
		stacktrace (Optional[str]): Stack trace of the event.
	"""
	
	target_data: TargetData
	level: FINGERPRINT_LOG_LEVELS_TYPEHINT
	api: str
	used_method: str
	datetime: datetime
	stacktrace: Optional[str]


class FingerprintLoggerChannelStats(DictModel):
	"""
	Statistics for a fingerprint logging channel.

	Attributes:
		target_id (str): ID of the target.
		title (str): Title of the target.
		url (str): URL of the target.
		num_logs (int): Total logs for this channel.
		last_log_time (datetime): Time of the last log.
		log_level_stats (Dict[str, FingerprintLogLevelStats]): Stats per log level.
	"""
	
	target_id: str
	title: str
	url: str
	num_logs: int = 0
	last_log_time: datetime = Field(default_factory=datetime.now)
	log_level_stats: Dict[str, FingerprintLogLevelStats] = Field(default_factory=dict)
	
	async def add_log(self, log_entry: FingerprintTargetLogEntry):
		"""
		Updates the channel statistics based on a new log entry.

		Args:
			log_entry (FingerprintTargetLogEntry): The new log entry to incorporate into the statistics.
		"""
		
		self.num_logs += 1
		self.last_log_time = log_entry.datetime
		
		if log_entry.level not in self.log_level_stats:
			self.log_level_stats[log_entry.level] = FingerprintLogLevelStats(num_logs=1, last_log_time=log_entry.datetime)
		else:
			self.log_level_stats[log_entry.level].num_logs += 1
			self.log_level_stats[log_entry.level].last_log_time = log_entry.datetime


class FingerprintAPIStats(DictModel):
	"""
	Statistics for a specific Fingerprint API.

	Attributes:
		num_logs (int): Number of targets accessing this API.
		methods_stats (Dict[str, int]): Count of calls per method.
	"""
	
	num_logs: int
	methods_stats: Dict[str, int]


class FingerprintMainLogEntry(DictModel):
	"""
	Summary log entry for all fingerprinting activity.

	Attributes:
		num_channels (int): Total active channels.
		apis_stats (Dict[str, FingerprintAPIStats]): Stats per API.
		num_logs (int): Total logs recorded.
		log_level_stats (Dict[str, FingerprintLogLevelStats]): Stats per log level.
		channels_stats (Sequence[FingerprintLoggerChannelStats]): Stats for each channel.
	"""
	
	num_channels: int
	apis_stats: Dict[str, FingerprintAPIStats]
	num_logs: int
	log_level_stats: Dict[str, FingerprintLogLevelStats]
	channels_stats: Sequence[FingerprintLoggerChannelStats]


class CDPLogLevelStats(DictModel):
	"""
	Dataclass to store statistics for a specific log level.

	Attributes:
		num_logs (int): The total number of logs recorded for this level.
		last_log_time (datetime): The timestamp of the most recent log entry for this level.
	"""
	
	num_logs: int
	last_log_time: datetime


class CDPTargetLogEntry(DictModel):
	"""
	Represents a single log entry with detailed information.

	Attributes:
		target_data (TargetData): Data about the target (browser tab/session) from which the log originated.
		message (str): The main log message.
		level (CDPLogLevelsType): The severity level of the log (e.g., "INFO", "ERROR").
		datetime (datetime): The exact time when the log entry was created.
		extra_data (Optional[Dict[str, Any]]): Optional additional data associated with the log.
	"""
	
	target_data: TargetData
	message: str
	level: CDP_LOG_LEVELS_TYPEHINT
	datetime: datetime
	extra_data: Optional[Dict[str, Any]] = None


class CDPLoggerChannelStats(DictModel):
	"""
	Dataclass to store statistics for a specific logging channel (per target).

	Attributes:
		target_id (str): The unique ID of the target associated with this channel.
		title (str): The title of the target (e.g., page title).
		url (str): The URL of the target.
		num_logs (int): The total number of log entries for this channel.
		last_log_time (datetime): The timestamp of the most recent log entry for this channel.
		log_level_stats (Dict[str, CDPLogLevelStats]): A dictionary mapping log levels to their specific statistics.
	"""
	
	target_id: str
	title: str
	url: str
	num_logs: int = 0
	last_log_time: datetime = Field(default_factory=datetime.now)
	log_level_stats: Dict[str, CDPLogLevelStats] = Field(default_factory=dict)
	
	async def add_log(self, log_entry: CDPTargetLogEntry):
		"""
		Updates the channel statistics based on a new log entry.

		Args:
			log_entry (CDPTargetLogEntry): The new log entry to incorporate into the statistics.
		"""
		
		self.num_logs += 1
		self.last_log_time = log_entry.datetime
		
		if log_entry.level not in self.log_level_stats:
			self.log_level_stats[log_entry.level] = CDPLogLevelStats(num_logs=1, last_log_time=log_entry.datetime)
		else:
			self.log_level_stats[log_entry.level].num_logs += 1
			self.log_level_stats[log_entry.level].last_log_time = log_entry.datetime


class CDPTargetTypeStats(DictModel):
	"""
	Dataclass to store statistics for a specific target type.

	Attributes:
		num_targets (int): The count of targets of this type.
	"""
	
	num_targets: int


class CDPMainLogEntry(DictModel):
	"""
	Represents a summary log entry for the entire logging system.

	Attributes:
		num_channels (int): The total number of active logging channels (targets).
		targets_types_stats (Dict[str, CDPTargetTypeStats]): Statistics grouped by target type.
		num_logs (int): The total number of log entries across all channels.
		log_level_stats (Dict[str, CDPLogLevelStats]): Overall statistics for each log level.
		channels_stats (Sequence[CDPLoggerChannelStats]): A List of statistics for each active logging channel.
	"""
	
	num_channels: int
	targets_types_stats: Dict[str, CDPTargetTypeStats]
	num_logs: int
	log_level_stats: Dict[str, CDPLogLevelStats]
	channels_stats: Sequence[CDPLoggerChannelStats]
