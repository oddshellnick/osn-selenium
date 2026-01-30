from pathlib import Path
from pydantic import Field
from osn_selenium._base_models import DictModel
from osn_selenium.dev_tools.filters import TargetFilter
from osn_selenium.dev_tools.domains import DomainsSettings
from typing import (
	Literal,
	Optional,
	Sequence,
	Union
)
from osn_selenium.javascript.fingerprint import FingerprintSettings
from osn_selenium.dev_tools._typehints import (
	CDP_LOG_LEVELS_TYPEHINT,
	DEVTOOLS_BACKGROUND_FUNCTION_TYPEHINT,
	FINGERPRINT_LOG_LEVELS_TYPEHINT
)


__all__ = [
	"CDPLoggerSettings",
	"DevToolsSettings",
	"FingerprintLoggerSettings",
	"LoggerSettings"
]


class FingerprintLoggerSettings(DictModel):
	"""
	Configuration settings for fingerprint logging.

	Attributes:
		buffer_size (int): The size of the log buffer. Defaults to 100.
		log_level_filter_mode (Literal["exclude", "include"]): Mode for filtering log levels.
			Defaults to "exclude".
		log_level_filter (Optional[Union[FingerprintLogLevelsType, Sequence[FingerprintLogLevelsType]]]):
			Specific log levels to filter based on the mode. Defaults to None.
		category_filter_mode (Literal["exclude", "include"]): Mode for filtering categories.
			Defaults to "exclude".
		category_filter (Optional[Union[str, Sequence[str]]]): Specific categories to filter.
			Defaults to None.
		send_wait (bool): Whether to wait for the log to be sent. Defaults to False.
	"""
	
	buffer_size: int = 100
	log_level_filter_mode: Literal["exclude", "include"] = "exclude"
	log_level_filter: Optional[
		Union[
			FINGERPRINT_LOG_LEVELS_TYPEHINT,
			Sequence[FINGERPRINT_LOG_LEVELS_TYPEHINT]
		]
	] = None
	category_filter_mode: Literal["exclude", "include"] = "exclude"
	category_filter: Optional[Union[str, Sequence[str]]] = None
	send_wait: bool = False


class CDPLoggerSettings(DictModel):
	"""
	Configuration settings for Chrome DevTools Protocol (CDP) logging.

	Attributes:
		buffer_size (int): The size of the log buffer. Defaults to 100.
		log_level_filter_mode (Literal["exclude", "include"]): The mode for filtering log levels.
			"exclude" means log levels in `log_level_filter` will be excluded.
			"include" means only log levels in `log_level_filter` will be included.
			Defaults to "exclude".
		log_level_filter (Optional[Union[CDPLogLevelsType, Sequence[CDPLogLevelsType]]]):
			A single log level or a sequence of log levels to filter by.
			Used in conjunction with `log_level_filter_mode`. Defaults to None.
		target_type_filter_mode (Literal["exclude", "include"]): The mode for filtering target types.
			"exclude" means target types in `target_type_filter` will be excluded.
			"include" means only target types in `target_type_filter` will be included.
			Defaults to "exclude".
		target_type_filter (Optional[Union[str, Sequence[str]]]):
			A single target type string or a sequence of target type strings to filter by.
			Used in conjunction with `target_type_filter_mode`. Defaults to None.
		send_wait (bool): Whether to wait for the log to be sent. Defaults to False.
	"""
	
	buffer_size: int = 100
	log_level_filter_mode: Literal["exclude", "include"] = "exclude"
	log_level_filter: Optional[Union[CDP_LOG_LEVELS_TYPEHINT, Sequence[CDP_LOG_LEVELS_TYPEHINT]]] = None
	target_type_filter_mode: Literal["exclude", "include"] = "exclude"
	target_type_filter: Optional[Union[str, Sequence[str]]] = None
	send_wait: bool = False


class LoggerSettings(DictModel):
	"""
	Settings for configuring the LoggerManager.

	Attributes:
		dir_path (Optional[Path]): The base directory where log files will be stored.
			If None, logging will only happen in memory and not be written to files.
			Defaults to None.
		renew_log (bool): Whether to clear/renew the log directory on startup. Defaults to True.
		cdp_settings (Optional[CDPLoggerSettings]): Settings specific to CDP logging. Defaults to None.
		fingerprint_settings (Optional[FingerprintLoggerSettings]): Settings specific to fingerprint logging.
			Defaults to None.
	"""
	
	dir_path: Optional[Path] = None
	renew_log: bool = True
	cdp_settings: Optional[CDPLoggerSettings] = None
	fingerprint_settings: Optional[FingerprintLoggerSettings] = None


class DevToolsSettings(DictModel):
	"""
	Settings for configuring the DevTools manager.

	Attributes:
		new_targets_filter (Optional[Sequence[TargetFilter]]): A sequence of `TargetFilter` objects
			to control which new browser targets (e.g., tabs, iframes) DevTools should discover and attach to.
			Defaults to None, meaning all targets are considered.
		new_targets_buffer_size (int): The buffer size for the Trio memory channel
			used to receive new target events. A larger buffer can prevent `trio.WouldBlock`
			errors under high event load. Defaults to 100.
		target_background_task (Optional[devtools_background_func_type]): An optional asynchronous function
			that will be run as a background task for each attached DevTools target. This can be used
			for custom per-target logic. Defaults to None.
		logger_settings (Optional[LoggerSettings]): Configuration settings for the internal logging system.
			If None, default logging settings will be used (no file logging by default).
			Defaults to None.
		fingerprint_settings (Optional[FingerprintSettings]): Configuration for fingerprint detection.
		domains_settings (Optional[DomainsSettings]): Configuration settings for various DevTools domains.
	"""
	
	new_targets_filter: Optional[Sequence[TargetFilter]] = None
	new_targets_buffer_size: int = 100
	target_background_task: Optional[DEVTOOLS_BACKGROUND_FUNCTION_TYPEHINT] = None
	logger_settings: Optional[LoggerSettings] = Field(default_factory=LoggerSettings)
	fingerprint_settings: Optional[FingerprintSettings] = None
	domains_settings: Optional[DomainsSettings] = None


LoggerSettings.model_rebuild()
DevToolsSettings.model_rebuild()
