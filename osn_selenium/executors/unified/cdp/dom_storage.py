from typing import (
	Any,
	Callable,
	Dict,
	List
)


__all__ = ["UnifiedDomStorageCDPExecutor"]


class UnifiedDomStorageCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _clear_impl(self, storage_id: Dict[str, Any]) -> None:
		return self._execute_function("DOMStorage.clear", {"storage_id": storage_id})
	
	def _disable_impl(self) -> None:
		return self._execute_function("DOMStorage.disable", {})
	
	def _enable_impl(self) -> None:
		return self._execute_function("DOMStorage.enable", {})
	
	def _get_dom_storage_items_impl(self, storage_id: Dict[str, Any]) -> List[List[str]]:
		return self._execute_function("DOMStorage.getDOMStorageItems", {"storage_id": storage_id})
	
	def _remove_dom_storage_item_impl(self, storage_id: Dict[str, Any], key: str) -> None:
		return self._execute_function(
				"DOMStorage.removeDOMStorageItem",
				{"storage_id": storage_id, "key": key}
		)
	
	def _set_dom_storage_item_impl(self, storage_id: Dict[str, Any], key: str, value: str) -> None:
		return self._execute_function(
				"DOMStorage.setDOMStorageItem",
				{"storage_id": storage_id, "key": key, "value": value}
		)
