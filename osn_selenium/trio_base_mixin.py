import trio
import functools
from typing import (
	Callable,
	ParamSpec,
	TypeVar
)


METHOD_INPUT = ParamSpec("METHOD_INPUT")
METHOD_OUTPUT = TypeVar("METHOD_OUTPUT")


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
