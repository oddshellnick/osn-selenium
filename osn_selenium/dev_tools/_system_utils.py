import shutil
from pathlib import Path
from osn_selenium.dev_tools.settings import LoggerSettings


__all__ = ["prepare_log_dir"]


def prepare_log_dir(logger_settings: LoggerSettings):
	"""
	Prepares the log directory based on the provided logger settings.

	If `log_dir_path` is specified:
	- Creates the directory if it doesn't exist.
	- If `renew_log` is True and the directory exists, it is cleared (recreated).

	Args:
		logger_settings (LoggerSettings): The settings object containing log directory configuration.

	Raises:
		ValueError: If `log_dir_path` is provided but is not a valid `Path` object
					or does not represent a directory.
	"""
	
	if isinstance(logger_settings.dir_path, Path) and (logger_settings.dir_path.is_dir() or not logger_settings.dir_path.exists()):
		if not logger_settings.dir_path.exists():
			logger_settings.dir_path.mkdir(parents=True)
		elif logger_settings.renew_log:
			shutil.rmtree(logger_settings.dir_path)
	
			logger_settings.dir_path.mkdir()
	elif logger_settings.dir_path is not None:
		raise ValueError(
				f"'log_dir_path' must be a pathlib.Path to directory or None, got {logger_settings.dir_path} (type: {type(logger_settings.dir_path).__name__})"
		)
