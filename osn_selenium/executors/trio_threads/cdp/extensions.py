import trio
from osn_selenium.base_mixin import TrioThreadMixin
from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional
)
from osn_selenium.executors.unified.cdp.extensions import (
	UnifiedExtensionsCDPExecutor
)
from osn_selenium.abstract.executors.cdp.extensions import (
	AbstractExtensionsCDPExecutor
)


__all__ = ["ExtensionsCDPExecutor"]


class ExtensionsCDPExecutor(
		UnifiedExtensionsCDPExecutor,
		TrioThreadMixin,
		AbstractExtensionsCDPExecutor
):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedExtensionsCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def clear_storage_items(self, id_: str, storage_area: str) -> None:
		return await self.sync_to_trio(sync_function=self._clear_storage_items_impl)(id_=id_, storage_area=storage_area)
	
	async def get_storage_items(self, id_: str, storage_area: str, keys: Optional[List[str]] = None) -> Any:
		return await self.sync_to_trio(sync_function=self._get_storage_items_impl)(id_=id_, storage_area=storage_area, keys=keys)
	
	async def load_unpacked(self, path: str) -> str:
		return await self.sync_to_trio(sync_function=self._load_unpacked_impl)(path=path)
	
	async def remove_storage_items(self, id_: str, storage_area: str, keys: List[str]) -> None:
		return await self.sync_to_trio(sync_function=self._remove_storage_items_impl)(id_=id_, storage_area=storage_area, keys=keys)
	
	async def set_storage_items(self, id_: str, storage_area: str, values: Any) -> None:
		return await self.sync_to_trio(sync_function=self._set_storage_items_impl)(id_=id_, storage_area=storage_area, values=values)
	
	async def uninstall(self, id_: str) -> None:
		return await self.sync_to_trio(sync_function=self._uninstall_impl)(id_=id_)
