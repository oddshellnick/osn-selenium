import trio
from typing import (
	Callable,
	ParamSpec,
	TypeVar
)


_METHOD_INPUT = ParamSpec("_METHOD_INPUT")
_METHOD_OUTPUT = TypeVar("_METHOD_OUTPUT")


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
