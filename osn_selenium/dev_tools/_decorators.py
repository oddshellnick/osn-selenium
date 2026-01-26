import trio
import inspect
import warnings
import functools
from osn_selenium.exceptions.devtools import ExceptionThrown
from osn_selenium.exceptions.instance import NotExpectedTypeError
from osn_selenium.dev_tools._exception_helpers import log_exception
from typing import (
	Any,
	Callable,
	ParamSpec,
	TYPE_CHECKING,
	TypeVar,
	Union
)


__all__ = ["background_task_decorator", "log_on_error", "warn_if_active"]

if TYPE_CHECKING:
	from osn_selenium.dev_tools.manager import DevTools
	from osn_selenium.dev_tools.target.base import BaseMixin
	from osn_selenium.dev_tools.target import DevToolsTarget
	from osn_selenium.dev_tools._typehints import DEVTOOLS_BACKGROUND_FUNCTION_TYPEHINT

_METHOD_INPUT = ParamSpec("_METHOD_INPUT")
_METHOD_OUTPUT = TypeVar("_METHOD_OUTPUT")
_METHOD = TypeVar("_METHOD", bound=Callable[..., Any])


def warn_if_active(func: _METHOD) -> _METHOD:
	"""
	Decorator to warn if DevTools operations are attempted while DevTools is active.

	This decorator is used to wrap methods in the DevTools class that should not be called
	while the DevTools event handler context manager is active. It checks the `is_active` flag
	of the DevTools instance. If DevTools is active, it issues a warning; otherwise, it proceeds
	to execute the original method.

	Args:
		func (_METHOD): The function to be wrapped. This should be a method of the DevTools class.

	Returns:
		_METHOD: The wrapped function. When called, it will check if DevTools is active and either
				  execute the original function or issue a warning.
	"""
	
	@functools.wraps(func)
	def sync_wrapper(
			self: "DevTools",
			*args: _METHOD_INPUT.args,
			**kwargs: _METHOD_INPUT.kwargs
	) -> Any:
		if self.is_active:
			warnings.warn("DevTools is active. Exit dev_tools context before changing settings.")
		
		return func(self, *args, **kwargs)
	
	@functools.wraps(func)
	async def async_wrapper(
			self: "DevTools",
			*args: _METHOD_INPUT.args,
			**kwargs: _METHOD_INPUT.kwargs
	) -> Any:
		if self.is_active:
			warnings.warn("DevTools is active. Exit dev_tools context before changing settings.")
		
		return await func(self, *args, **kwargs)
	
	if inspect.iscoroutinefunction(func):
		return async_wrapper
	
	if inspect.isfunction(func):
		return sync_wrapper
	
	raise NotExpectedTypeError(expected_type=["coroutine function", "function"], received_instance=func)


def log_on_error(func: _METHOD) -> _METHOD:
	"""
	Decorator that logs any `BaseException` raised by the decorated async function.

	If an exception occurs, it is logged using `log_exception`, and an `ExceptionThrown`
	object wrapping the exception is returned instead of re-raising it.

	Args:
		func (_METHOD): The asynchronous function to be wrapped.

	Returns:
		_METHOD: The wrapped asynchronous function.
	"""
	
	@functools.wraps(func)
	def sync_wrapper(*args: _METHOD_INPUT.args, **kwargs: _METHOD_INPUT.kwargs) -> _METHOD_OUTPUT:
		try:
			return func(*args, **kwargs)
		except BaseException as exception:
			log_exception(exception)
			return ExceptionThrown(exception)
	
	@functools.wraps(func)
	async def async_wrapper(*args: _METHOD_INPUT.args, **kwargs: _METHOD_INPUT.kwargs) -> _METHOD_OUTPUT:
		try:
			return await func(*args, **kwargs)
		except BaseException as exception:
			log_exception(exception)
			return ExceptionThrown(exception)
	
	if inspect.iscoroutinefunction(func):
		return async_wrapper
	
	if inspect.isfunction(func):
		return sync_wrapper
	
	raise NotExpectedTypeError(expected_type=["coroutine function", "function"], received_instance=func)


def background_task_decorator(func: "DEVTOOLS_BACKGROUND_FUNCTION_TYPEHINT") -> "DEVTOOLS_BACKGROUND_FUNCTION_TYPEHINT":
	"""
	Decorator for target background tasks to manage their lifecycle.

	This decorator wraps a target's background task function. It ensures that
	`target.background_task_ended` event is set when the function completes,
	allowing the `BaseTargetMixin` to track the task's termination.

	Args:
		func ("DEVTOOLS_BACKGROUND_FUNCTION_TYPEHINT"): The asynchronous background task function
		to be wrapped. It should accept a target instance.

	Returns:
		"DEVTOOLS_BACKGROUND_FUNCTION_TYPEHINT": The wrapped function.
	"""
	
	@functools.wraps(func)
	async def wrapper(target: Union["BaseMixin", "DevToolsTarget"]) -> Any:
		if not target.about_to_stop_event.is_set():
			with trio.CancelScope() as cancel_scope:
				target.cancel_scopes["background_task"] = cancel_scope
		
				try:
					target.background_task_ended = trio.Event()
		
					await func(target)
		
					target.background_task_ended.set()
				finally:
					target.cancel_scopes.pop("background_task")
	
	return wrapper
