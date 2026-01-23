import trio
from osn_selenium.dev_tools.errors import cdp_end_exceptions
from osn_selenium.dev_tools.exception_utils import ExceptionThrown
from typing import (
	Any,
	Callable,
	Dict,
	Generator,
	Iterable,
	List,
	Literal,
	Optional,
	Sequence,
	TYPE_CHECKING,
	Union
)


__all__ = [
	"cdp_command_error",
	"execute_cdp_command",
	"validate_target_event",
	"validate_target_event_filter",
	"validate_target_type",
	"validate_type_filter",
	"wait_one",
	"yield_package_item_way"
]

if TYPE_CHECKING:
	from osn_selenium.dev_tools.target.logging import LoggingMixin as LoggingTargetMixin
	from osn_selenium.dev_tools.utils import TargetsFilters


def yield_package_item_way(name: Union[str, Iterable[str]]) -> Generator[str, Any, None]:
	"""
	Yields parts of a package path from a string or iterable of strings.

	Args:
		name (Union[str, Iterable[str]]): The name or path components to yield.

	Returns:
		Generator[str, Any, None]: A generator yielding each part of the path.

	Raises:
		TypeError: If `name` is not a string or an iterable of strings.
	"""
	
	if (
			not isinstance(name, str) and (
					not isinstance(name, (list, set, tuple)) or not all(isinstance(item, str) for item in name)
			)
	):
		raise TypeError(
				f"Wrong name type ({type(name).__name__})! Must be str or Iterable[str]!"
		)
	
	way = name if isinstance(name, (list, set, tuple)) else [name]
	
	for item in way:
		for part in item.split("."):
			yield part


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


def validate_type_filter(
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
	
	from osn_selenium.dev_tools.logger.functions import validate_log_filter
	
	return validate_log_filter(filter_mode, filter_instances)(type_)


def validate_target_event_filter(filter_: Optional[Sequence[Dict[str, Any]]]) -> "TargetsFilters":
	"""
	Validates and processes a raw dictionary-based event filter into a `TargetsFilters` object.

	Args:
		filter_ (Optional[List[Dict[str, Any]]]): A list of dictionary filters defining inclusion/exclusion rules.

	Returns:
		"TargetsFilters": A processed object containing excluded and included types.

	Raises:
		ValueError: If duplicate types appear in both included and excluded lists.
	"""
	
	if filter_ is None:
		filter_ = []
	
	all_excluded_types = [
		type_filter["type"]
		for type_filter in filter_
		if type_filter.get("exclude", True)
		and type_filter.get("type", None) is not None
	]
	all_included_types = [
		type_filter["type"]
		for type_filter in filter_
		if not type_filter.get("exclude", True)
		and type_filter.get("type", None) is not None
	]
	
	if len(set(all_excluded_types) & set(all_included_types)) > 0:
		raise ValueError(
				f"Duplicate types in target filters! ({set(all_excluded_types) & set(all_included_types)})"
		)
	
	other_types = any(
			type_filter.get("type", None) is None
			and not type_filter.get("exclude", True)
			for type_filter in filter_
	)
	
	from osn_selenium.dev_tools.utils import TargetsFilters
	
	return TargetsFilters(
			excluded=all_excluded_types,
			included=all_included_types,
			entire=other_types,
	)


def validate_target_type(type_: str, filter_: "TargetsFilters") -> bool:
	"""
	Checks if a target type is valid based on the provided filter configuration.

	Args:
		type_ (str): The target type to check.
		filter_ ("TargetsFilters"): The filter configuration containing included and excluded types.

	Returns:
		bool: True if the target type is valid according to the filter, False otherwise.
	"""
	
	if type_ in filter_.excluded:
		return False
	
	if type_ in filter_.included:
		return True
	
	return filter_.entire


def validate_target_event(event: Any, filter_: "TargetsFilters") -> Optional[bool]:
	"""
	Validates a target event against the provided filter.

	Args:
		event (Any): The event object containing target information.
		filter_ ("TargetsFilters"): The filter to apply.

	Returns:
		Optional[bool]: True if the event target is valid, False otherwise, or None if validation cannot be determined.
	"""
	
	result = None
	
	if hasattr(event, "target_info") and hasattr(event.target_info, "type_"):
		result = validate_target_type(type_=event.target_info.type_, filter_=filter_)
	
	if hasattr(event, "type_"):
		result = validate_target_type(type_=event.type_, filter_=filter_)
	
	return result


async def cdp_command_error(
		self: "LoggingTargetMixin",
		error: BaseException,
		error_mode: Literal["raise", "log", "log_without_args", "pass"],
		command_name: str,
		*args: Any,
		**kwargs: Any,
):
	"""
	Handles errors occurring during CDP command execution based on the specified error mode.

	Args:
		self ("LoggingTargetMixin"): The instance executing the command.
		error (BaseException): The exception that was caught.
		error_mode (Literal["raise", "log", "log_without_args", "pass"]): Strategy for handling the error.
		command_name (str): Name of the CDP command that failed.
		*args (Any): Positional arguments passed to the command.
		**kwargs (Any): Keyword arguments passed to the command.

	Returns:
		Union[Any, ExceptionThrown]: Returns ExceptionThrown if not raising.

	Raises:
		BaseException: The original error if error_mode is "raise".
		ValueError: If an invalid error_mode is provided.
	"""
	
	if error_mode == "raise":
		raise error
	
	if error_mode == "log":
		await self.log_cdp_error(
				error=error,
				extra_data={"cdp_command": command_name, "args": args, "kwargs": kwargs}
		)
	
		return ExceptionThrown(exception=error)
	
	if error_mode == "log_without_args":
		await self.log_cdp_error(error=error, extra_data={"cdp_command": command_name})
	
		return ExceptionThrown(exception=error)
	
	if error_mode == "pass":
		return ExceptionThrown(exception=error)
	
	raise ValueError(f"Wrong error_mode: {error_mode}. Expected: 'raise', 'log', 'pass'.")


async def execute_cdp_command(
		self: "LoggingTargetMixin",
		function: Callable[..., Any],
		cdp_error_mode: Literal["raise", "log", "log_without_args", "pass"] = "raise",
		error_mode: Literal["raise", "log", "log_without_args", "pass"] = "raise",
		command_retries: int = 0,
		*args: Any,
		**kwargs: Any,
) -> Union[Any, ExceptionThrown]:
	"""
	Executes a Chrome DevTools Protocol (CDP) command with specified error handling.

	This function attempts to execute a CDP command via the `cdp_session`.
	It provides different behaviors based on the `error_mode` if an exception occurs:
	- "raise": Re-raises the exception immediately.
	- "log": Logs the exception using the target's logger and returns an `ExceptionThrown` object.
	- "pass": Returns an `ExceptionThrown` object without logging the exception.

	Args:
		self ("LoggingTargetMixin"): The `LoggingTargetMixin` instance through which the command is executed.
		function (Callable[..., Any]): The CDP command function to execute (e.g., `devtools.page.navigate`).
		cdp_error_mode (Literal["raise", "log", "log_without_args", "pass"]): Strategy for connection errors.
		error_mode (Literal["raise", "log", "log_without_args", "pass"]): Strategy for general execution errors.
		command_retries (int): Number of times to retry the command on failure.
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
		await self.log_cdp(
				level="DEBUG",
				message=f"Executing CDP command: {function.__name__}",
				extra_data={"args": args, "kwargs": kwargs}
		)
	
		for i in range(command_retries):
			try:
				return await self.cdp_session.execute(function(*args, **kwargs))
			except* (BaseException):
				await trio.sleep(1.0)
	
		return await self.cdp_session.execute(function(*args, **kwargs))
	except cdp_end_exceptions as error:
		return await cdp_command_error(
				self=self,
				error=error,
				error_mode=cdp_error_mode,
				command_name=function.__name__,
				*args,
				**kwargs
		)
	except BaseException as error:
		return await cdp_command_error(
				self=self,
				error=error,
				error_mode=error_mode,
				command_name=function.__name__,
				*args,
				**kwargs
		)
