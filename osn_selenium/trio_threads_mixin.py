import trio
from osn_selenium._trio_threads_helpers import (
	sync_to_trio,
	sync_to_trio_context
)
from typing import (
	Any,
	AsyncContextManager,
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
			exchange_context:bool = True,
	) -> Callable[_METHOD_INPUT, Coroutine[Any, Any, _METHOD_OUTPUT]]:
		"""
		Wraps a synchronous function to run within a Trio thread pool using a lock and limiter.

		Args:
			sync_function (Callable[_METHOD_INPUT, _METHOD_OUTPUT]): The synchronous function to wrap.
			lock (bool): Whether to use the internal lock for synchronization.
			exchange_context (bool): Whether to synchronize context variables between threads.

		Returns:
			Callable[_METHOD_INPUT, Coroutine[Any, Any, _METHOD_OUTPUT]]: An async wrapper for the sync function.
		"""
		
		return sync_to_trio(
				sync_function=sync_function,
				lock_object=self._lock,
				capacity_limiter_object=self._capacity_limiter,
				lock=lock,
				exchange_context=exchange_context,
		)
	
	def sync_to_trio_context(
			self,
			context_manager_factory: Callable[_METHOD_INPUT, ContextManager[_METHOD_OUTPUT]],
			lock: bool = True,
			exchange_context:bool = True,
	) -> Callable[_METHOD_INPUT, AsyncContextManager[_METHOD_OUTPUT]]:
		"""
		Converts a synchronous context manager factory to an asynchronous Trio-compatible context manager.

		Args:
			context_manager_factory (Callable[_METHOD_INPUT, ContextManager[_METHOD_OUTPUT]]): A factory function returning a context manager.
			lock (bool): Whether to use the internal lock for synchronization.
			exchange_context (bool): Whether to synchronize context variables between threads.

		Returns:
			Callable[_METHOD_INPUT, AsyncContextManager[_METHOD_OUTPUT]]: An async function returning an async context manager.
		"""
		
		return sync_to_trio_context(
				context_manager_factory=context_manager_factory,
				lock_object=self._lock,
				capacity_limiter_object=self._capacity_limiter,
				lock=lock,
				exchange_context=exchange_context,
		)
