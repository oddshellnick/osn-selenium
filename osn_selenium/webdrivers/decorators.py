import inspect
import functools
from typing import (
	Any,
	Callable,
	ParamSpec,
	TypeVar,
)


_METHOD_INPUT = ParamSpec("_METHOD_INPUT")
_METHOD_OUTPUT = TypeVar("_METHOD_OUTPUT")
_METHOD = TypeVar("_METHOD", bound=Callable[..., Any])


def requires_driver(fn: _METHOD) -> _METHOD:
	"""
	A decorator that ensures a '_ensure_driver' method is called before
	executing the decorated method.

	This decorator handles both synchronous and asynchronous methods,
	calling '_ensure_driver' on the instance (self) before delegating
	to the original method.

	Args:
		fn (_METHOD): The method to decorate.

	Returns:
		_METHOD: The wrapped synchronous or asynchronous method.
	"""
	
	@functools.wraps(fn)
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
		return fn(self, *args, **kwargs)
	
	@functools.wraps(fn)
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
		return await fn(self, *args, **kwargs)
	
	if inspect.iscoroutinefunction(fn):
		return async_wrapper
	
	if inspect.isfunction(fn):
		return sync_wrapper
	
	raise TypeError(f"Expected a coroutine function or function, got {type(fn).__name__}")
