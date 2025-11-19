import trio
from trio import CapacityLimiter
from functools import partial, wraps
from typing import (
	Any,
	Callable,
	Coroutine,
	Optional,
	ParamSpec,
	TypeVar
)


def trio_async_wrap(
		func: Callable[TrioWrapInput, TrioWrapOutput],
		trio_capacity_limiter: Optional[CapacityLimiter] = None
) -> Callable[TrioWrapInput, Coroutine[Any, Any, TrioWrapOutput]]:
	@wraps(func)
	async def wrapper(*args: TrioWrapInput.args, **kwargs: TrioWrapInput.kwargs) -> TrioWrapOutput:
		if trio_capacity_limiter is not None:
			async with trio_capacity_limiter:
				func_with_kwargs = partial(func, **kwargs)
				return await trio.to_thread.run_sync(func_with_kwargs, *args, limiter=trio_capacity_limiter)
		else:
			func_with_kwargs = partial(func, **kwargs)
			return await trio.to_thread.run_sync(func_with_kwargs, *args, limiter=trio_capacity_limiter)
	
	return wrapper


def build_cdp_kwargs(**kwargs):
	dict_ = {}
	
	for key, value in kwargs.items():
		if value is not None:
			dict_[key] = value
	
	return dict_


TrioWrapInput = ParamSpec("TrioWrapInput")
TrioWrapOutput = TypeVar("TrioWrapOutput")
