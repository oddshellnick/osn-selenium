import inspect
import functools
from typing import (
	Any,
	Callable,
	ParamSpec,
	TypeVar
)
from osn_selenium.exceptions.instance import NotExpectedTypeError


__all__ = ["requires_driver"]

_METHOD_INPUT = ParamSpec("_METHOD_INPUT")
_METHOD_OUTPUT = TypeVar("_METHOD_OUTPUT")
_METHOD = TypeVar("_METHOD", bound=Callable[..., Any])


def requires_driver(func: _METHOD) -> _METHOD:
	"""
	A decorator that ensures a '_ensure_driver' method is called before
	executing the decorated method.

	This decorator handles both synchronous and asynchronous methods,
	calling '_ensure_driver' on the instance (self) before delegating
	to the original method.

	Args:
		func (_METHOD): The method to decorate.

	Returns:
		_METHOD: The wrapped synchronous or asynchronous method.
	"""
	
	@functools.wraps(func)
	def sync_wrapper(
			self: object,
			*args: _METHOD_INPUT.args,
			**kwargs: _METHOD_INPUT.kwargs
	) -> _METHOD_OUTPUT:
		"""
		Synchronous wrapper for methods decorated with requires_driver.

		Args:
			self (object): The instance on which the method is called.
			*args (_METHOD_INPUT.args): Positional arguments for the wrapped method.
			**kwargs (_METHOD_INPUT.kwargs): Keyword arguments for the wrapped method.

		Returns:
			_METHOD_OUTPUT: The result of the wrapped method.
		"""
		
		getattr(self, "_ensure_driver")()
		return func(self, *args, **kwargs)
	
	@functools.wraps(func)
	async def async_wrapper(
			self: object,
			*args: _METHOD_INPUT.args,
			**kwargs: _METHOD_INPUT.kwargs
	) -> _METHOD_OUTPUT:
		"""
		Asynchronous wrapper for methods decorated with requires_driver.

		Args:
			self (object): The instance on which the method is called.
			*args (_METHOD_INPUT.args): Positional arguments for the wrapped method.
			**kwargs (_METHOD_INPUT.kwargs): Keyword arguments for the wrapped method.

		Returns:
			_METHOD_OUTPUT: The result of the wrapped method.
		"""
		
		getattr(self, "_ensure_driver")()
		return await func(self, *args, **kwargs)
	
	if inspect.iscoroutinefunction(func):
		return async_wrapper
	
	if inspect.isfunction(func):
		return sync_wrapper
	
	raise NotExpectedTypeError(expected_type=["coroutine function", "function"], received_instance=func)
