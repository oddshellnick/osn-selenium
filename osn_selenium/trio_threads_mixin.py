import sys
import trio
from contextlib import asynccontextmanager
from typing import (
	Any,
	AsyncContextManager,
	AsyncIterator,
	Callable,
	ContextManager,
	Coroutine,
	ParamSpec,
	TypeVar
)


__all__ = ["TrioThreadMixin"]

_METHOD_INPUT = ParamSpec("_METHOD_INPUT")
_METHOD_OUTPUT = TypeVar("_METHOD_OUTPUT")


class TrioThreadMixin:
	"""
	Provides utilities for running synchronous functions in a Trio event loop
	with a controlled concurrency, ensuring thread safety and resource limits.
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
	
	@property
	def capacity_limiter(self) -> trio.CapacityLimiter:
		"""
		The Trio CapacityLimiter used for concurrency control.

		Returns:
			trio.CapacityLimiter: The limiter instance.
		"""
		
		return self._capacity_limiter
	
	@property
	def lock(self) -> trio.Lock:
		"""
		The Trio Lock used for synchronization.

		Returns:
			trio.Lock: The lock instance.
		"""
		
		return self._lock
	
	def sync_to_trio(
			self,
			sync_function: Callable[_METHOD_INPUT, _METHOD_OUTPUT],
			lock: bool = True,
	) -> Callable[_METHOD_INPUT, Coroutine[Any, Any, _METHOD_OUTPUT]]:
		"""
		Wraps a synchronous function to run within a Trio thread pool using a lock and limiter.

		Args:
			sync_function (Callable[_METHOD_INPUT, _METHOD_OUTPUT]): The synchronous function to wrap.
			lock (bool): Whether to use the internal lock for synchronization.

		Returns:
			Callable[_METHOD_INPUT, Coroutine[Any, Any, _METHOD_OUTPUT]]: An async wrapper for the sync function.
		"""
		
		async def wrapper(*args: _METHOD_INPUT.args, **kwargs: _METHOD_INPUT.kwargs) -> _METHOD_OUTPUT:
			"""
			Internal async wrapper for the synchronous function.

			Args:
				*args (_METHOD_INPUT.args): Positional arguments for the sync function.
				**kwargs (_METHOD_INPUT.kwargs): Keyword arguments for the sync function.

			Returns:
				_METHOD_OUTPUT: The result of the synchronous function execution.
			"""
			
			def function_with_kwargs(*args_) -> _METHOD_OUTPUT:
				"""
				Helper to pass keyword arguments to trio.to_thread.run_sync.

				Args:
					*args_: Positional arguments passed from the outer scope.

				Returns:
					_METHOD_OUTPUT: Result of the original sync function.
				"""
				
				return sync_function(*args_, **kwargs)
			
			if lock:
				async with self._lock:
					result = await trio.to_thread.run_sync(function_with_kwargs, *args, limiter=self._capacity_limiter)
			else:
				result = await trio.to_thread.run_sync(function_with_kwargs, *args, limiter=self._capacity_limiter)
			
			return result
		
		return wrapper
	
	def sync_to_trio_context(
			self,
			context_manager_factory: Callable[_METHOD_INPUT, ContextManager[_METHOD_OUTPUT]],
			lock: bool = True,
	) -> Callable[_METHOD_INPUT, AsyncContextManager[_METHOD_OUTPUT]]:
		"""
		Converts a synchronous context manager factory to an asynchronous Trio-compatible context manager.

		Args:
			context_manager_factory (Callable[_METHOD_INPUT, ContextManager[_METHOD_OUTPUT]]): A factory function returning a context manager.
			lock (bool): Whether to use the internal lock for synchronization.

		Returns:
			Callable[_METHOD_INPUT, AsyncContextManager[_METHOD_OUTPUT]]: An async function returning an async context manager.
		"""
		
		@asynccontextmanager
		async def wrapper(*args: _METHOD_INPUT.args, **kwargs: _METHOD_INPUT.kwargs) -> AsyncIterator[_METHOD_OUTPUT]:
			"""
			Internal async context manager wrapper.

			Args:
				*args (_METHOD_INPUT.args): Positional arguments for the factory.
				**kwargs (_METHOD_INPUT.kwargs): Keyword arguments for the factory.

			Returns:
				AsyncIterator[_METHOD_OUTPUT]: An async iterator yielding the context resource.
			"""
			
			sync_context_manager = await self.sync_to_trio(sync_function=context_manager_factory, lock=lock)(*args, **kwargs)
			
			enter_ = self.sync_to_trio(sync_function=sync_context_manager.__enter__, lock=lock)
			exit_ = self.sync_to_trio(sync_function=sync_context_manager.__exit__, lock=lock)
			
			try:
				result = await enter_()
			
				yield result
			except Exception as e:
				exc_type, exc_val, exc_tb = sys.exc_info()
			
				if not await exit_(exc_type, exc_val, exc_tb):
					raise e
			else:
				await exit_(None, None, None)
		
		return wrapper
