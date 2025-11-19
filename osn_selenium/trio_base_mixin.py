import trio
import inspect
import functools
from typing import (
	Callable,
	ParamSpec,
	TypeVar
)


_METHOD_INPUT = ParamSpec("_METHOD_INPUT")
_METHOD_OUTPUT = TypeVar("_METHOD_OUTPUT")


def requires_driver(fn: Callable[_METHOD_INPUT, _METHOD_OUTPUT]) -> Callable[_METHOD_INPUT, _METHOD_OUTPUT]:
	@functools.wraps(fn)
	def sync_wrapper(
			self: object,
			*args: _METHOD_INPUT.args,
			**kwargs: _METHOD_INPUT.kwargs
	) -> _METHOD_OUTPUT:
		getattr(self, "_ensure_driver")()
		return fn(self, *args, **kwargs)
	
	@functools.wraps(fn)
	async def async_wrapper(
			self: object,
			*args: _METHOD_INPUT.args,
			**kwargs: _METHOD_INPUT.kwargs
	) -> _METHOD_OUTPUT:
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
			fn: Callable[_METHOD_INPUT, _METHOD_OUTPUT],
			*args: _METHOD_INPUT.args,
			**kwargs: _METHOD_INPUT.kwargs,
	) -> _METHOD_OUTPUT:
		def placeholder(*args_):
			return fn(*args_, **kwargs)
		
		async with self._lock:
			return await trio.to_thread.run_sync(placeholder, *args, limiter=self._capacity_limiter)
