from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional
)


__all__ = ["UnifiedExtensionsCDPExecutor"]


class UnifiedExtensionsCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _clear_storage_items_impl(self, id_: str, storage_area: str) -> None:
		return self._execute_function(
				"Extensions.clearStorageItems",
				{"id_": id_, "storage_area": storage_area}
		)
	
	def _get_storage_items_impl(self, id_: str, storage_area: str, keys: Optional[List[str]] = None) -> Any:
		return self._execute_function(
				"Extensions.getStorageItems",
				{"id_": id_, "storage_area": storage_area, "keys": keys}
		)
	
	def _load_unpacked_impl(self, path: str) -> str:
		return self._execute_function("Extensions.loadUnpacked", {"path": path})
	
	def _remove_storage_items_impl(self, id_: str, storage_area: str, keys: List[str]) -> None:
		return self._execute_function(
				"Extensions.removeStorageItems",
				{"id_": id_, "storage_area": storage_area, "keys": keys}
		)
	
	def _set_storage_items_impl(self, id_: str, storage_area: str, values: Any) -> None:
		return self._execute_function(
				"Extensions.setStorageItems",
				{"id_": id_, "storage_area": storage_area, "values": values}
		)
	
	def _uninstall_impl(self, id_: str) -> None:
		return self._execute_function("Extensions.uninstall", {"id_": id_})
