import json
import shutil
import logging
import warnings
import traceback
import functools
from pathlib import Path
from typing import (
	Any,
	Callable,
	Dict, Iterable,
	List, Literal,
	Optional,
	TYPE_CHECKING,
	Union
)

import trio
from pydantic import Field

from osn_selenium.types import DictModel
from osn_selenium.dev_tools.errors import cdp_end_exceptions
from osn_selenium.dev_tools._types import (
	devtools_background_func_type
)


if TYPE_CHECKING:
	from osn_selenium.dev_tools.logger import LoggerSettings
	from osn_selenium.dev_tools.manager import DevTools, DevToolsTarget


def warn_if_active(func: Callable) -> Callable:
	"""
	Decorator to warn if DevTools operations are attempted while DevTools is active.

	This decorator is used to wrap methods in the DevTools class that should not be called
	while the DevTools event handler context manager is active. It checks the `is_active` flag
	of the DevTools instance. If DevTools is active, it issues a warning; otherwise, it proceeds
	to execute the original method.

	Args:
		func (Callable): The function to be wrapped. This should be a method of the DevTools class.

	Returns:
		Callable: The wrapped function. When called, it will check if DevTools is active and either
				  execute the original function or issue a warning.
	"""
	
	@functools.wraps(func)
	def wrapper(self: "DevTools", *args: Any, **kwargs: Any) -> Any:
		if self.is_active:
			warnings.warn("DevTools is active. Exit dev_tools context before changing settings.")
		
		return func(self, *args, **kwargs)
	
	return wrapper


async def wait_one(*events: trio.Event):
	"""
	Waits for the first of multiple Trio events to be set.

	This function creates a nursery and starts a task for each provided event.
	As soon as any event is set, it receives a signal, cancels the nursery,
	and returns.

	Args:
		*events (trio.Event): One or more Trio Event objects to wait for.
	"""
	
	async def waiter(event: trio.Event, send_chan_: trio.MemorySendChannel):
		"""Internal helper to wait for an event and send a signal."""
		
		await event.wait()
		await send_chan_.send(0)
	
	send_chan, receive_chan = trio.open_memory_channel(0)
	
	async with trio.open_nursery() as nursery:
		for event_ in events:
			nursery.start_soon(waiter, event_, send_chan.clone())
	
		await receive_chan.receive()
		nursery.cancel_scope.cancel()


def log_on_error(func: Callable) -> Callable:
	"""
	Decorator that logs any `BaseException` raised by the decorated async function.

	If an exception occurs, it is logged using `log_exception`, and an `ExceptionThrown`
	object wrapping the exception is returned instead of re-raising it.

	Args:
		func (Callable): The asynchronous function to be wrapped.

	Returns:
		Callable: The wrapped asynchronous function.
	"""
	
	@functools.wraps(func)
	async def wrapper(*args: Any, **kwargs: Any) -> Any:
		try:
			return await func(*args, **kwargs)
		except BaseException as exception:
			log_exception(exception)
			return ExceptionThrown(exception)
	
	return wrapper


def extract_exception_trace(exception: BaseException) -> str:
	"""
	Extracts a comprehensive traceback string for an exception, including handling for `ExceptionGroup`s.

	This function recursively flattens `ExceptionGroup`s to ensure all nested exceptions
	have their tracebacks included in the final output string.

	Args:
		exception (BaseException): The exception object to extract the trace from.

	Returns:
		str: A multi-line string containing the formatted traceback(s) for the given exception
			 and any nested exceptions within an `ExceptionGroup`.

	EXAMPLES
	________
	>>> try:
	...	 raise ValueError("Simple error occurred")
	... except ValueError as e:
	...	 trace = extract_exception_trace(e)
	...	 # The first line typically indicates the start of a traceback
	...	 print(trace.splitlines()[0].strip())
	...
	>>> try:
	...	 raise ExceptionGroup(
	...		 "Multiple issues",
	...		 [
	...			 TypeError("Invalid type provided"),
	...			 ValueError("Value out of range")
	...		 ]
	...	 )
	... except ExceptionGroup as eg:
	...	 trace = extract_exception_trace(eg)
	...	 # Check if tracebacks for both nested exceptions are present
	...	 print("TypeError" in trace and "ValueError" in trace)
	...
	"""
	
	def flatten_exceptions(exception_: BaseException) -> List[BaseException]:
		"""Recursively flattens an ExceptionGroup into a List of individual exceptions."""
		
		if isinstance(exception_, ExceptionGroup):
			inner_exceptions = exception_.exceptions
		else:
			return [exception_]
		
		result = []
		for exception__ in inner_exceptions:
			result.extend(flatten_exceptions(exception__))
		
		return result
	
	def format_exception(exception_: BaseException) -> str:
		"""Formats a single exception's traceback into a string."""
		
		return "".join(
				traceback.format_exception(exception_.__class__, exception_, exception_.__traceback__)
		)
	
	return "\n".join(format_exception(exc) for exc in flatten_exceptions(exception))


def log_exception(exception: BaseException, extra_data: Optional[Dict[str, Any]] = None):
	"""
	Logs the full traceback of an exception at the ERROR level.

	This function uses `extract_exception_trace` to get a comprehensive traceback string
	and then logs it using the standard logging module.

	Args:
		exception (BaseException): The exception object to log.
	"""

	if extra_data is None:
		exception_data = extract_exception_trace(exception)
	else:
		trace = extract_exception_trace(exception)
		max_len = max(len(line) for line in trace.splitlines())

		exception_data = "{bound}\n{exception}\nWith extra data:\n{extra_data}\n{bound}".format(
				bound="=" * max_len,
				exception=trace,
				extra_data=json.dumps(extra_data, indent=4, ensure_ascii=False)
		)
	
	logging.log(logging.ERROR, exception_data)


class ExceptionThrown:
	"""
	A wrapper class to indicate that an exception was thrown during an operation.

	This is used in `execute_cdp_command` when `error_mode` is "log" or "pass"
	to return an object indicating an error occurred without re-raising it immediately.

	Attributes:
		exception (BaseException): The exception that was caught.
		traceback (str): The formatted traceback string of the exception.
	"""
	
	def __init__(self, exception: BaseException):
		"""
		Initializes the ExceptionThrown wrapper.

		Args:
			exception (BaseException): The exception to wrap.
		"""
		
		self.exception = exception
		self.traceback = extract_exception_trace(exception)


async def execute_cdp_command(
		self: "DevToolsTarget",
		error_mode: Literal["raise", "log", "pass"],
		function: Callable[..., Any],
		*args: Any,
		**kwargs: Any
) -> Union[Any, ExceptionThrown]:
	"""
	Executes a Chrome DevTools Protocol (CDP) command with specified error handling.

	This function attempts to execute a CDP command via the `cdp_session`.
	It provides different behaviors based on the `error_mode` if an exception occurs:
	- "raise": Re-raises the exception immediately.
	- "log": Logs the exception using the target's logger and returns an `ExceptionThrown` object.
	- "pass": Returns an `ExceptionThrown` object without logging the exception.

	Args:
		self ("DevToolsTarget"): The `DevToolsTarget` instance through which the command is executed.
		error_mode (Literal["raise", "log", "pass"]): Defines how exceptions are handled.
			"raise": Re-raises the exception.
			"log": Logs the exception and returns `ExceptionThrown`.
			"pass": Returns `ExceptionThrown` without logging.
		function (Callable[..., Any]): The CDP command function to execute (e.g., `devtools.page.navigate`).
		*args (Any): Positional arguments to pass to the CDP command function.
		**kwargs (Any): Keyword arguments to pass to the CDP command function.

	Returns:
		Union[Any, ExceptionThrown]: The result of the CDP command if successful,
			or an `ExceptionThrown` object if an error occurred and `error_mode` is "log" or "pass".

	Raises:
		cdp_end_exceptions: If a CDP-related connection error occurs, these are always re-raised.
		BaseException: If `error_mode` is "raise" and any other exception occurs.
		ValueError: If an unknown `error_mode` is provided.
	"""
	
	try:
		return await self.cdp_session.execute(function(*args, **kwargs))
	except cdp_end_exceptions as error:
		raise error
	except BaseException as error:
		if error_mode == "raise":
			raise error
		elif error_mode == "log":
			await self.log_error(
					error=error,
					extra_data={
						"cdp_command": function.__name__,
						"args": args,
						"kwargs": kwargs
					}
			)

			return ExceptionThrown(exception=error)
		elif error_mode == "pass":
			return ExceptionThrown(exception=error)
		else:
			raise ValueError(f"Wrong error_mode: {error_mode}. Expected: 'raise', 'log', 'pass'.")


def _validate_log_filter(
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
		log_filter (Optional[Union[str, Sequence[str]]]):
			A single log filter item or a sequence of such items.
			If None:
				- In "include" mode, the generated filter will always return False (nothing is included).
				- In "exclude" mode, the generated filter will always return True (nothing is excluded).

	Returns:
		Callable[[str], bool]: A callable function that takes a single argument (e.g., a log level or target type)
			and returns True if it passes the filter, False otherwise.

	Raises:
		ValueError: If `filter_mode` is invalid.

	EXAMPLES
	________
	>>> # Example 1: Include only "INFO" logs
	... info_only_filter = _validate_log_filter("include", "INFO")
	... print(info_only_filter("INFO"))	# True
	... print(info_only_filter("ERROR"))   # False

	>>> # Example 2: Exclude "DEBUG" and "WARNING" logs
	... no_debug_warning_filter = _validate_log_filter("exclude", ["DEBUG", "WARNING"])
	... print(no_debug_warning_filter("INFO"))	# True
	... print(no_debug_warning_filter("DEBUG"))   # False

	>>> # Example 3: No filter (exclude mode, so everything passes)
	... all_logs_filter = _validate_log_filter("exclude", None)
	... print(all_logs_filter("INFO"))	 # True
	... print(all_logs_filter("ERROR"))	# True

	>>> # Example 4: No filter (include mode, so nothing passes)
	... no_logs_filter = _validate_log_filter("include", None)
	... print(no_logs_filter("INFO"))	  # False
	... print(no_logs_filter("ERROR"))	 # False
	"""
	
	if log_filter is None:
		if filter_mode == "include":
			return lambda x: False
		elif filter_mode == "exclude":
			return lambda x: True
	
	if isinstance(log_filter, Iterable):
		if filter_mode == "include":
			return lambda x: x in log_filter
		elif filter_mode == "exclude":
			return lambda x: x not in log_filter
	
	if filter_mode == "include":
		return lambda x: x == log_filter
	elif filter_mode == "exclude":
		return lambda x: x != log_filter
	
	raise ValueError(f"Invalid log filter_mode ({filter_mode}).")


def _validate_type_filter(
		type_: str,
		filter_mode: Literal["include", "exclude"],
		filter_instances: Any
):
	"""
	Validates a target type against a given filter mode and filter instances.

	This is a wrapper around `_validate_log_filter` specifically for target types.

	Args:
		type_ (str): The target type string to check (e.g., "page", "iframe").
		filter_mode (Literal["include", "exclude"]): The mode of the filter ("include" or "exclude").
		filter_instances (Any): The filter value(s) (e.g., a string or a sequence of strings).

	Returns:
		bool: True if the `type_` passes the filter, False otherwise.
	"""
	
	return _validate_log_filter(filter_mode, filter_instances)(type_)


def _prepare_log_dir(logger_settings: "LoggerSettings"):
	"""
	Prepares the log directory based on the provided logger settings.

	If `log_dir_path` is specified:
	- Creates the directory if it doesn't exist.
	- If `renew_log` is True and the directory exists, it is cleared (recreated).

	Args:
		logger_settings ("LoggerSettings"): The settings object containing log directory configuration.

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
				f"'log_dir_path' must be a pathlib.Path to directory or None, got {logger_settings.log_dir_path} (type: {type(logger_settings.log_dir_path)})"
		)


def _background_task_decorator(func: devtools_background_func_type) -> devtools_background_func_type:
	"""
	Decorator for DevToolsTarget background tasks to manage their lifecycle.

	This decorator wraps a target's background task function. It ensures that
	`target.background_task_ended` event is set when the function completes,
	allowing the `DevToolsTarget` to track the task's termination.

	Args:
		func (devtools_background_func_type): The asynchronous background task function
											  to be wrapped. It should accept a `DevToolsTarget` instance.

	Returns:
		devtools_background_func_type: The wrapped function.
	"""
	
	@functools.wraps(func)
	async def wrapper(target: "DevToolsTarget") -> Any:
		target.background_task_ended = trio.Event()
		
		await func(target)
		
		target.background_task_ended.set()
	
	return wrapper


class TargetFilter(DictModel):
	"""
	Dataclass to define a filter for discovering new browser targets.

	Used in `DevToolsSettings` to specify which types of targets (e.g., "page", "iframe")
	should be automatically attached to or excluded.

	Attributes:
		type_ (Optional[str]): The type of target to filter by (e.g., "page", "iframe").
			If None, this filter applies regardless of type.
		exclude (Optional[bool]): If True, targets matching `type_` will be excluded.
			If False or None, targets matching `type_` will be included.
	"""
	
	type_: Optional[str] = Field(default=None, alias="type")
	exclude: Optional[bool] = None


class TargetData(DictModel):
	"""
	Dataclass to hold essential information about a browser target (e.g., a tab, iframe, or worker).

	Attributes:
		target_id (Optional[str]): The unique identifier for the target.
		type_ (Optional[str]): The type of the target (e.g., "page", "iframe", "worker").
		title (Optional[str]): The title of the target (e.g., the page title).
		url (Optional[str]): The URL of the target.
		attached (Optional[bool]): Indicates if the DevTools session is currently attached to this target.
	"""
	
	target_id: Optional[str] = None
	type_: Optional[str] = None
	title: Optional[str] = None
	url: Optional[str] = None
	attached: Optional[bool] = None
	can_access_opener: Optional[bool] = None
	opener_id: Optional[str] = None
	opener_frame_id: Optional[str] = None
	browser_context_id: Optional[str] = None
	subtype: Optional[str] = None


TargetFilter.model_rebuild()
TargetData.model_rebuild()
