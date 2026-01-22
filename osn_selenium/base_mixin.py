import sys
import trio
from contextlib import asynccontextmanager
from typing import (
	AsyncGenerator,
	Callable,
	ContextManager,
	Generator,
	ParamSpec,
	TypeVar
)


_METHOD_INPUT = ParamSpec("_METHOD_INPUT")
_METHOD_OUTPUT = TypeVar("_METHOD_OUTPUT")


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
		Initializes the TrioThreadMixin with a Trio Lock and CapacityLimiter.

		Args:
			lock (trio.Lock): A Trio Lock for synchronization.
			limiter (trio.CapacityLimiter): A limiter to control thread pool concurrency.
		"""
		
		self._lock = lock
		self._capacity_limiter = limiter
	
	async def _sync_to_trio(
			self,
			fn: Callable[_METHOD_INPUT, _METHOD_OUTPUT],
			*args: _METHOD_INPUT.args,
			**kwargs: _METHOD_INPUT.kwargs,
	) -> _METHOD_OUTPUT:
		"""
		Wraps a synchronous function to be run in a Trio thread.

		This method ensures that the function is run safely within the Trio
		event loop, using the instance's lock for exclusive access and
		the capacity limiter to control concurrency.

		Args:
			fn (_METHOD): The synchronous function to run.
			*args (_METHOD_INPUT.args): Positional arguments to pass to the function.
			**kwargs (_METHOD_INPUT.kwargs): Keyword arguments to pass to the function.

		Returns:
			_METHOD_OUTPUT: The result of the synchronous function.
		"""
		
		def function_with_kwargs(*args_) -> _METHOD_OUTPUT:
			return fn(*args_, **kwargs)
		
		async with self._lock:
			result = await trio.to_thread.run_sync(function_with_kwargs, *args, limiter=self._capacity_limiter)
		
			return result
	
	@asynccontextmanager
	async def _sync_to_trio_context(
			self,
			cm_factory: Callable[_METHOD_INPUT, ContextManager[Generator[None, _METHOD_OUTPUT, None]]],
			*args: _METHOD_INPUT.args,
			**kwargs: _METHOD_INPUT.kwargs,
	) -> AsyncGenerator[_METHOD_OUTPUT, None]:
		"""
		Wraps a synchronous context manager to be used asynchronously with Trio.

		Args:
			cm_factory (Callable[_METHOD_INPUT, ContextManager[Generator[None, _METHOD_OUTPUT, None]]]):
				A factory function that returns a synchronous context manager.
			*args (_METHOD_INPUT.args): Positional arguments for the context manager factory.
			**kwargs (_METHOD_INPUT.kwargs): Keyword arguments for the context manager factory.

		Returns:
			AsyncGenerator[_METHOD_OUTPUT, None]: An asynchronous generator yielding the context manager's value.
		"""
		
		sync_context_manager = await self._sync_to_trio(cm_factory, *args, **kwargs)
		
		try:
			yield await self._sync_to_trio(sync_context_manager.__enter__)
		except Exception as e:
			exc_type, exc_val, exc_tb = sys.exc_info()
			await self._sync_to_trio(sync_context_manager.__exit__, exc_type, exc_val, exc_tb)
		
			raise e
		else:
			await self._sync_to_trio(sync_context_manager.__exit__, None, None, None)
