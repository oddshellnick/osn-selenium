import trio
from osn_selenium.base_mixin import TrioThreadMixin
from typing import (
	Any,
	Callable,
	Dict,
	Optional,
	Tuple
)
from osn_selenium.executors.unified.cdp.io import UnifiedIoCDPExecutor
from osn_selenium.abstract.executors.cdp.io import (
	AbstractIoCDPExecutor
)


__all__ = ["IoCDPExecutor"]


class IoCDPExecutor(UnifiedIoCDPExecutor, TrioThreadMixin, AbstractIoCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedIoCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def close(self, handle: str) -> None:
		return await self.sync_to_trio(sync_function=self._close_impl)(handle=handle)
	
	async def read(
			self,
			handle: str,
			offset: Optional[int] = None,
			size: Optional[int] = None
	) -> Tuple[Optional[bool], str, bool]:
		return await self.sync_to_trio(sync_function=self._read_impl)(handle=handle, offset=offset, size=size)
	
	async def resolve_blob(self, object_id: str) -> str:
		return await self.sync_to_trio(sync_function=self._resolve_blob_impl)(object_id=object_id)
