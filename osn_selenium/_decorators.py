import inspect
import functools
from osn_selenium.exceptions.base import ExceptionThrown
from osn_selenium._exception_helpers import log_exception
from typing import (
	Any,
	Callable,
	ParamSpec,
	TypeVar
)
from osn_selenium.exceptions.instance import NotExpectedTypeError


__all__ = ["log_on_error"]

_METHOD_INPUT = ParamSpec("_METHOD_INPUT")
_METHOD_OUTPUT = TypeVar("_METHOD_OUTPUT")
_METHOD = TypeVar("_METHOD", bound=Callable[..., Any])


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
