import trio
import random
from typing import (
	Any,
	Callable,
	Literal,
	TYPE_CHECKING,
	Union
)
from osn_selenium.exceptions.configuration import (
	NotExpectedValueError
)
from osn_selenium.exceptions.devtools import (
	CDPEndExceptions,
	ExceptionThrown
)


__all__ = ["cdp_command_error", "execute_cdp_command", "wait_one"]

if TYPE_CHECKING:
	from osn_selenium.dev_tools.target.logging import LoggingMixin as LoggingTargetMixin


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
		NotExpectedValueError: If an invalid error_mode is provided.
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
	
	raise NotExpectedValueError(
			value_name="error_mode",
			value=error_mode,
			valid_values=["raise", "log", "pass"]
	)


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
		CDPEndExceptions: If a CDP-related connection error occurs, these are always re-raised.
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
			except* (BaseException,):
				await trio.sleep(random.uniform(0.5, 1.5))
	
		return await self.cdp_session.execute(function(*args, **kwargs))
	except CDPEndExceptions as error:
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
