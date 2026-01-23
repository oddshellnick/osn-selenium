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


class DomStorageCDPExecutor(UnifiedDomStorageCDPExecutor, AbstractDomStorageCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedDomStorageCDPExecutor.__init__(self, execute_function=execute_function)
	
	def clear(self, storage_id: Dict[str, Any]) -> None:
		return self._clear_impl(storage_id=storage_id)
	
	def disable(self) -> None:
		return self._disable_impl()
	
	def enable(self) -> None:
		return self._enable_impl()
	
	def get_dom_storage_items(self, storage_id: Dict[str, Any]) -> List[List[str]]:
		return self._get_dom_storage_items_impl(storage_id=storage_id)
	
	def remove_dom_storage_item(self, storage_id: Dict[str, Any], key: str) -> None:
		return self._remove_dom_storage_item_impl(storage_id=storage_id, key=key)
	
	def set_dom_storage_item(self, storage_id: Dict[str, Any], key: str, value: str) -> None:
		return self._set_dom_storage_item_impl(storage_id=storage_id, key=key, value=value)
