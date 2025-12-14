import trio
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
	
	is_coro: bool = inspect.iscoroutinefunction(fn)
	
	return async_wrapper if is_coro else sync_wrapper


class _TrioThreadMixin:
	"""
	Provides utilities for running synchronous functions in a Trio event loop
	with a controlled concurrency, ensuring thread safety and resource limits.
	"""
	
	def __init__(self, lock: trio.Lock, limiter: trio.CapacityLimiter) -> None:
		"""
		Initializes the _TrioThreadMixin with a Trio Lock and CapacityLimiter.

		Args:
			lock (trio.Lock): A Trio Lock to ensure exclusive access for certain operations.
			limiter (trio.CapacityLimiter): A Trio CapacityLimiter to control the number
											of concurrent synchronous operations.
		"""
		
		self._lock: trio.Lock = lock
		self._capacity_limiter: trio.CapacityLimiter = limiter
	
	async def _wrap_to_trio(
			self,
			fn: Callable[METHOD_INPUT, METHOD_OUTPUT],
			*args: METHOD_INPUT.args,
			**kwargs: METHOD_INPUT.kwargs,
	) -> METHOD_OUTPUT:
		"""
		Wraps a synchronous function to be run in a Trio thread.

		This method ensures that the function is run safely within the Trio
		event loop, using the instance's lock for exclusive access and
		the capacity limiter to control concurrency.

		Args:
			fn (Callable[METHOD_INPUT, METHOD_OUTPUT]): The synchronous function to run.
			*args (METHOD_INPUT.args): Positional arguments to pass to the function.
			**kwargs (METHOD_INPUT.kwargs): Keyword arguments to pass to the function.

		Returns:
			METHOD_OUTPUT: The result of the synchronous function.
		"""
		
		if kwargs:
			fn = functools.partial(fn, **kwargs)
		
		async with self._lock:
			return await trio.to_thread.run_sync(fn, *args, limiter=self._capacity_limiter)
