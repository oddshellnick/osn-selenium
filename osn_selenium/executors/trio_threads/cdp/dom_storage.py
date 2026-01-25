import trio
from osn_selenium.base_mixin import TrioThreadMixin
from typing import (
	Any,
	Callable,
	Dict,
	List
)
from osn_selenium.executors.unified.cdp.dom_storage import (
	UnifiedDomStorageCDPExecutor
)
from osn_selenium.abstract.executors.cdp.dom_storage import (
	AbstractDomStorageCDPExecutor
)


__all__ = ["DomStorageCDPExecutor"]


class DomStorageCDPExecutor(
		UnifiedDomStorageCDPExecutor,
		TrioThreadMixin,
		AbstractDomStorageCDPExecutor
):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedDomStorageCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def clear(self, storage_id: Dict[str, Any]) -> None:
		return await self.sync_to_trio(sync_function=self._clear_impl)(storage_id=storage_id)
	
	async def disable(self) -> None:
		return await self.sync_to_trio(sync_function=self._disable_impl)()
	
	async def enable(self) -> None:
		return await self.sync_to_trio(sync_function=self._enable_impl)()
	
	async def get_dom_storage_items(self, storage_id: Dict[str, Any]) -> List[List[str]]:
		return await self.sync_to_trio(sync_function=self._get_dom_storage_items_impl)(storage_id=storage_id)
	
	async def remove_dom_storage_item(self, storage_id: Dict[str, Any], key: str) -> None:
		return await self.sync_to_trio(sync_function=self._remove_dom_storage_item_impl)(storage_id=storage_id, key=key)
	
	async def set_dom_storage_item(self, storage_id: Dict[str, Any], key: str, value: str) -> None:
		return await self.sync_to_trio(sync_function=self._set_dom_storage_item_impl)(storage_id=storage_id, key=key, value=value)
