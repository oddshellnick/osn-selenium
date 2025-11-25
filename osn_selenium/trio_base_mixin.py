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
	@functools.wraps(fn)
	def sync_wrapper(
			self: object,
			*args: METHOD_INPUT.args,
			**kwargs: METHOD_INPUT.kwargs
	) -> METHOD_OUTPUT:
		getattr(self, "_ensure_driver")()
		return fn(self, *args, **kwargs)
	
	@functools.wraps(fn)
	async def async_wrapper(
			self: object,
			*args: METHOD_INPUT.args,
			**kwargs: METHOD_INPUT.kwargs
	) -> METHOD_OUTPUT:
		getattr(self, "_ensure_driver")()
		return await fn(self, *args, **kwargs)
	
	is_coro = inspect.iscoroutinefunction(fn)

	return async_wrapper if is_coro else sync_wrapper


class _TrioThreadMixin:
	def __init__(self, lock: trio.Lock, limiter: trio.CapacityLimiter) -> None:
		self._lock = lock
		self._capacity_limiter = limiter
	
	async def _wrap_to_trio(
			self,
			fn: Callable[METHOD_INPUT, METHOD_OUTPUT],
			*args: METHOD_INPUT.args,
			**kwargs: METHOD_INPUT.kwargs,
	) -> METHOD_OUTPUT:
		if kwargs:
			fn = functools.partial(fn, **kwargs)
		
		async with self._lock:
			return await trio.to_thread.run_sync(fn, *args, limiter=self._capacity_limiter)
