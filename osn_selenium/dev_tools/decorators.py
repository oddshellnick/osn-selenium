import trio
import inspect
import warnings
import functools
from typing import (
	Any,
	Callable,
	ParamSpec,
	TYPE_CHECKING,
	TypeVar
)
from osn_selenium.dev_tools.exception_utils import (
	ExceptionThrown,
	log_exception
)


if TYPE_CHECKING:
	from osn_selenium.dev_tools.manager import DevTools
	from osn_selenium.dev_tools.target.base import BaseMixin
	from osn_selenium.dev_tools._types import devtools_background_func_type

METHOD_INPUT = ParamSpec("METHOD_INPUT")
METHOD_OUTPUT = TypeVar("METHOD_OUTPUT")


def warn_if_active(func: Callable[METHOD_INPUT, METHOD_OUTPUT]) -> Callable[METHOD_INPUT, METHOD_OUTPUT]:
	"""
	Decorator to warn if DevTools operations are attempted while DevTools is active.

	This decorator is used to wrap methods in the DevTools class that should not be called
	while the DevTools event handler context manager is active. It checks the `is_active` flag
	of the DevTools instance. If DevTools is active, it issues a warning; otherwise, it proceeds
	to execute the original method.

	Args:
		func (Callable[METHOD_INPUT, METHOD_OUTPUT]): The function to be wrapped. This should be a method of the DevTools class.

	Returns:
		Callable[METHOD_INPUT, METHOD_OUTPUT]: The wrapped function. When called, it will check if DevTools is active and either
				  execute the original function or issue a warning.
	"""
	
	@functools.wraps(func)
	def sync_wrapper(
			self: "DevTools",
			*args: METHOD_INPUT.args,
			**kwargs: METHOD_INPUT.kwargs
	) -> Any:
		if self.is_active:
			warnings.warn("DevTools is active. Exit dev_tools context before changing settings.")
		
		return func(self, *args, **kwargs)
	
	@functools.wraps(func)
	async def async_wrapper(
			self: "DevTools",
			*args: METHOD_INPUT.args,
			**kwargs: METHOD_INPUT.kwargs
	) -> Any:
		if self.is_active:
			warnings.warn("DevTools is active. Exit dev_tools context before changing settings.")
		
		return await func(self, *args, **kwargs)
	
	if inspect.iscoroutinefunction(func):
		return async_wrapper
	
	if inspect.isfunction(func):
		return sync_wrapper
	
	raise TypeError(
			f"Expected a coroutine function or function, got {type(func).__name__}"
	)


def log_on_error(func: Callable[METHOD_INPUT, METHOD_OUTPUT]) -> Callable[METHOD_INPUT, METHOD_OUTPUT]:
	"""
	Decorator that logs any `BaseException` raised by the decorated async function.

	If an exception occurs, it is logged using `log_exception`, and an `ExceptionThrown`
	object wrapping the exception is returned instead of re-raising it.

	Args:
		func (Callable[METHOD_INPUT, METHOD_OUTPUT]): The asynchronous function to be wrapped.

	Returns:
		Callable[METHOD_INPUT, METHOD_OUTPUT]: The wrapped asynchronous function.
	"""
	
	@functools.wraps(func)
	def sync_wrapper(*args: METHOD_INPUT.args, **kwargs: METHOD_INPUT.kwargs) -> METHOD_OUTPUT:
		try:
			return func(*args, **kwargs)
		except BaseException as exception:
			log_exception(exception)
			return ExceptionThrown(exception)
	
	@functools.wraps(func)
	async def async_wrapper(*args: METHOD_INPUT.args, **kwargs: METHOD_INPUT.kwargs) -> METHOD_OUTPUT:
		try:
			return await func(*args, **kwargs)
		except BaseException as exception:
			log_exception(exception)
			return ExceptionThrown(exception)
	
	if inspect.iscoroutinefunction(func):
		return async_wrapper
	
	if inspect.isfunction(func):
		return sync_wrapper
	
	raise TypeError(
			f"Expected a coroutine function or function, got {type(func).__name__}"
	)


def background_task_decorator(func: "devtools_background_func_type") -> "devtools_background_func_type":
	"""
	Decorator for BaseTargetMixin background tasks to manage their lifecycle.

	This decorator wraps a target's background task function. It ensures that
	`target.background_task_ended` event is set when the function completes,
	allowing the `BaseTargetMixin` to track the task's termination.

	Args:
		func ("devtools_background_func_type"): The asynchronous background task function
											  to be wrapped. It should accept a `BaseTargetMixin` instance.

	Returns:
		"devtools_background_func_type": The wrapped function.
	"""
	
	@functools.wraps(func)
	async def wrapper(target: "BaseMixin") -> Any:
		target.background_task_ended = trio.Event()
		
		await func(target)
		
		target.background_task_ended.set()
	
	return wrapper
