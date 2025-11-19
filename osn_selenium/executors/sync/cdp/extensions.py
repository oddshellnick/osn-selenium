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


class ExtensionsCDPExecutor(UnifiedExtensionsCDPExecutor, AbstractExtensionsCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedExtensionsCDPExecutor.__init__(self, execute_function=execute_function)
	
	def clear_storage_items(self, id_: str, storage_area: str) -> None:
		return self._clear_storage_items_impl(id_=id_, storage_area=storage_area)
	
	def get_storage_items(self, id_: str, storage_area: str, keys: Optional[List[str]] = None) -> Any:
		return self._get_storage_items_impl(id_=id_, storage_area=storage_area, keys=keys)
	
	def load_unpacked(self, path: str) -> str:
		return self._load_unpacked_impl(path=path)
	
	def remove_storage_items(self, id_: str, storage_area: str, keys: List[str]) -> None:
		return self._remove_storage_items_impl(id_=id_, storage_area=storage_area, keys=keys)
	
	def set_storage_items(self, id_: str, storage_area: str, values: Any) -> None:
		return self._set_storage_items_impl(id_=id_, storage_area=storage_area, values=values)
	
	def uninstall(self, id_: str) -> None:
		return self._uninstall_impl(id_=id_)
