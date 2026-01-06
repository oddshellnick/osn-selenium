import inspect
import functools
from typing import (
	Callable,
	ParamSpec,
	TypeVar
)


METHOD_INPUT = ParamSpec("METHOD_INPUT")
METHOD_OUTPUT = TypeVar("METHOD_OUTPUT")


def requires_driver(fn: Callable[METHOD_INPUT, METHOD_OUTPUT]) -> Callable[METHOD_INPUT, METHOD_OUTPUT]:
	"""
	A decorator that ensures a '_ensure_driver' method is called before
	executing the decorated method.

	This decorator handles both synchronous and asynchronous methods,
	calling '_ensure_driver' on the instance (self) before delegating
	to the original method.

	Args:
		fn (Callable[METHOD_INPUT, METHOD_OUTPUT]): The method to decorate.

	Returns:
		Callable[METHOD_INPUT, METHOD_OUTPUT]: The wrapped synchronous or asynchronous method.
	"""
	
	@functools.wraps(fn)
	def sync_wrapper(self: object, *args: METHOD_INPUT.args, **kwargs: METHOD_INPUT.kwargs) -> METHOD_OUTPUT:
		"""
		Synchronous wrapper for methods decorated with requires_driver.

		Args:
			self (object): The instance on which the method is called.
			*args (METHOD_INPUT.args): Positional arguments for the wrapped method.
			**kwargs (METHOD_INPUT.kwargs): Keyword arguments for the wrapped method.

		Returns:
			METHOD_OUTPUT: The result of the wrapped method.
		"""
		
		getattr(self, "_ensure_driver")()
		return fn(self, *args, **kwargs)
	
	@functools.wraps(fn)
	async def async_wrapper(self: object, *args: METHOD_INPUT.args, **kwargs: METHOD_INPUT.kwargs) -> METHOD_OUTPUT:
		"""
		Asynchronous wrapper for methods decorated with requires_driver.

		Args:
			self (object): The instance on which the method is called.
			*args (METHOD_INPUT.args): Positional arguments for the wrapped method.
			**kwargs (METHOD_INPUT.kwargs): Keyword arguments for the wrapped method.

		Returns:
			METHOD_OUTPUT: The result of the wrapped method.
		"""
		
		getattr(self, "_ensure_driver")()
		return await fn(self, *args, **kwargs)
	
	if inspect.iscoroutinefunction(fn):
		return async_wrapper
	
	if inspect.isfunction(fn):
		return sync_wrapper
	
	raise TypeError(f"Expected a coroutine function or function, got {type(fn).__name__}")
