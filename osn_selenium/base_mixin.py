import sys
import trio
import functools
from contextlib import asynccontextmanager
from typing import (
	AsyncGenerator,
	Callable,
	ContextManager,
	Generator,
	ParamSpec,
	TypeVar
)


METHOD_INPUT = ParamSpec("METHOD_INPUT")
METHOD_OUTPUT = TypeVar("METHOD_OUTPUT")


class TrioThreadMixin:
	"""
	Provides utilities for running synchronous functions in a Trio event loop
	with a controlled concurrency, ensuring thread safety and resource limits.

	Attributes:
		_lock (trio.Lock): A Trio Lock to ensure exclusive access for certain operations.
		_capacity_limiter (trio.CapacityLimiter): A Trio CapacityLimiter to control the number
			of concurrent synchronous operations.
	"""
	
	def __init__(self, lock: trio.Lock, limiter: trio.CapacityLimiter) -> None:
		"""
		Initializes the _TrioThreadMixin with a Trio Lock and CapacityLimiter.

		Args:
			lock (trio.Lock): A Trio Lock for synchronization.
			limiter (trio.CapacityLimiter): A limiter to control thread pool concurrency.
		"""
		
		self._lock = lock
		self._capacity_limiter = limiter
	
	async def _sync_to_trio(
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
	
	@asynccontextmanager
	async def _sync_to_trio_context(
			self,
			cm_factory: Callable[METHOD_INPUT, ContextManager[Generator[None, METHOD_OUTPUT, None]]],
			*args: METHOD_INPUT.args,
			**kwargs: METHOD_INPUT.kwargs,
	) -> AsyncGenerator[METHOD_OUTPUT, None]:
		"""
		Wraps a synchronous context manager to be used asynchronously with Trio.

		Args:
			cm_factory (Callable[METHOD_INPUT, ContextManager[Generator[None, METHOD_OUTPUT, None]]]):
				A factory function that returns a synchronous context manager.
			*args (METHOD_INPUT.args): Positional arguments for the context manager factory.
			**kwargs (METHOD_INPUT.kwargs): Keyword arguments for the context manager factory.

		Returns:
			AsyncGenerator[METHOD_OUTPUT, None]: An asynchronous generator yielding the context manager's value.
		"""
		
		sync_cm = await self._sync_to_trio(cm_factory, *args, **kwargs)
		
		try:
			yield await self._sync_to_trio(sync_cm.__enter__)
		except Exception as e:
			exc_type, exc_val, exc_tb = sys.exc_info()
			await self._sync_to_trio(sync_cm.__exit__, exc_type, exc_val, exc_tb)
		
			raise e
		else:
			await self._sync_to_trio(sync_cm.__exit__, None, None, None)
