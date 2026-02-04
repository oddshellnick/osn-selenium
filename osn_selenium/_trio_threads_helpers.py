import sys
import trio
import contextvars
from contextlib import asynccontextmanager
from typing import (
	Any,
	AsyncContextManager,
	AsyncIterator,
	Callable,
	ContextManager,
	Coroutine,
	ParamSpec,
	Tuple,
	TypeVar
)


__all__ = ["sync_to_trio", "sync_to_trio_context"]

_METHOD_INPUT = ParamSpec("_METHOD_INPUT")
_METHOD_OUTPUT = TypeVar("_METHOD_OUTPUT")


def sync_to_trio_context(
		context_manager_factory: Callable[_METHOD_INPUT, ContextManager[_METHOD_OUTPUT]],
		lock_object: trio.Lock,
		capacity_limiter_object: trio.CapacityLimiter,
		lock: bool,
		exchange_context: bool,
) -> Callable[_METHOD_INPUT, AsyncContextManager[_METHOD_OUTPUT]]:
	"""
	Converts a synchronous context manager factory to an asynchronous Trio-compatible context manager.

	Args:
		context_manager_factory (Callable[_METHOD_INPUT, ContextManager[_METHOD_OUTPUT]]): Factory function returning a context manager.
		lock_object (trio.Lock): Trio lock for synchronization.
		capacity_limiter_object (trio.CapacityLimiter): Trio capacity limiter.
		lock (bool): Whether to use the internal lock for synchronization.
		exchange_context (bool): Whether to synchronize context variables between threads.

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
		
		sync_context_manager = await sync_to_trio(
				sync_function=context_manager_factory,
				lock_object=lock_object,
				capacity_limiter_object=capacity_limiter_object,
				lock=lock,
				exchange_context=exchange_context,
		)(*args, **kwargs)
		
		enter_ = sync_to_trio(
				sync_function=sync_context_manager.__enter__,
				lock_object=lock_object,
				capacity_limiter_object=capacity_limiter_object,
				lock=lock,
				exchange_context=exchange_context,
		)
		exit_ = sync_to_trio(
				sync_function=sync_context_manager.__exit__,
				lock_object=lock_object,
				capacity_limiter_object=capacity_limiter_object,
				lock=lock,
				exchange_context=exchange_context,
		)
		
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


def sync_to_trio(
		sync_function: Callable[_METHOD_INPUT, _METHOD_OUTPUT],
		lock_object: trio.Lock,
		capacity_limiter_object: trio.CapacityLimiter,
		lock: bool,
		exchange_context: bool,
) -> Callable[_METHOD_INPUT, Coroutine[Any, Any, _METHOD_OUTPUT]]:
	"""
	Wraps a synchronous function to run within a Trio thread pool using a lock and limiter.

	Args:
		sync_function (Callable[_METHOD_INPUT, _METHOD_OUTPUT]): The synchronous function to wrap.
		lock_object (trio.Lock): Trio lock for synchronization.
		capacity_limiter_object (trio.CapacityLimiter): Trio capacity limiter.
		lock (bool): Whether to use the provided lock.
		exchange_context (bool): Whether to synchronize context variables between threads.

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
		
		def function_with_kwargs(*args_) -> Tuple[_METHOD_OUTPUT, contextvars.Context]:
			"""
		Helper to pass keyword arguments to trio.to_thread.run_sync.

		Args:
			*args_: Positional arguments passed from the outer scope.

		Returns:
			Tuple[_METHOD_OUTPUT, contextvars.Context]: Result of original sync function and the thread context.
		"""
			
			sync_result = sync_function(*args_, **kwargs)
			context_vars = contextvars.copy_context()
			
			return sync_result, context_vars
		
		if lock:
			async with lock_object:
				result, child_context_vars = await trio.to_thread.run_sync(function_with_kwargs, *args, limiter=capacity_limiter_object)
		else:
			result, child_context_vars = await trio.to_thread.run_sync(function_with_kwargs, *args, limiter=capacity_limiter_object)
		
		if exchange_context:
			for var, value in child_context_vars.items():
				var.set(value)
		
		return result
	
	return wrapper
