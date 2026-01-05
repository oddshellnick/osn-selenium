import shutil
from pathlib import Path
from typing import (
    Callable,
    Iterable,
    Literal,
    Optional,
    Union
)

from osn_selenium.dev_tools.settings import LoggerSettings


def validate_log_filter(
    filter_mode: Literal["include", "exclude"],
    log_filter: Optional[Union[str, Iterable[str]]]
) -> Callable[[str], bool]:
    """
    Creates a callable filter function based on the specified filter mode and values.

    This function generates a lambda that can be used to check if a given log level
    or target type should be processed, based on whether the filter is set to
    "include" (only process items in the filter) or "exclude" (process all items
    except those in the filter).

    Args:
        filter_mode (Literal["include", "exclude"]): The mode of the filter.
            "include" means only items present in `log_filter` will pass.
            "exclude" means all items except those present in `log_filter` will pass.
        log_filter (Optional[Union[str, Iterable[str]]]):
            A single log filter item or an iterable of such items.
            If None:
                - In "include" mode, the generated filter will always return False (nothing is included).
                - In "exclude" mode, the generated filter will always return True (nothing is excluded).

    Returns:
        Callable[[str], bool]: A callable function that takes a single argument (e.g., a log level or target type)
            and returns True if it passes the filter, False otherwise.

    Raises:
        ValueError: If `filter_mode` or 'log_filter' is invalid.

    EXAMPLES
    ________
    >>> # Example 1: Include only "INFO" logs
    ... info_only_filter = validate_log_filter("include", "INFO")
    ... print(info_only_filter("INFO"))    # True
    ... print(info_only_filter("ERROR"))   # False
    >>> # Example 2: Exclude "DEBUG" and "WARNING" logs
    ... no_debug_warning_filter = validate_log_filter("exclude", ["DEBUG", "WARNING"])
    ... print(no_debug_warning_filter("INFO"))    # True
    ... print(no_debug_warning_filter("DEBUG"))   # False
    >>> # Example 3: No filter (exclude mode, so everything passes)
    ... all_logs_filter = validate_log_filter("exclude", None)
    ... print(all_logs_filter("INFO"))     # True
    ... print(all_logs_filter("ERROR"))    # True
    """

    if log_filter is None:
        if filter_mode == "include":
            return lambda x: False

        if filter_mode == "exclude":
            return lambda x: True

    if isinstance(log_filter, Iterable) and not isinstance(log_filter, str):
        if filter_mode == "include":
            return lambda x: x in log_filter

        if filter_mode == "exclude":
            return lambda x: x not in log_filter

    if isinstance(log_filter, str):
        if filter_mode == "include":
            return lambda x: x == log_filter

        if filter_mode == "exclude":
            return lambda x: x != log_filter

    raise ValueError(f"Invalid 'filter_mode' ({filter_mode}) or 'log_filter' type ({type(filter_mode).__name__}).")


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

    if isinstance(logger_settings.log_dir_path, Path) and (
            logger_settings.log_dir_path.is_dir()
            or not logger_settings.log_dir_path.exists()
    ):
        if not logger_settings.log_dir_path.exists():
            logger_settings.log_dir_path.mkdir(parents=True)
        elif logger_settings.renew_log:
            shutil.rmtree(logger_settings.log_dir_path)

            logger_settings.log_dir_path.mkdir()

    elif logger_settings.log_dir_path is not None:
        raise ValueError(
            f"'log_dir_path' must be a pathlib.Path to directory or None, got {logger_settings.log_dir_path} (type: {type(logger_settings.log_dir_path).__name__})"
        )
