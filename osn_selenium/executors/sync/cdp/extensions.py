from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional
)
from osn_selenium.abstract.executors.cdp.extensions import (
	AbstractExtensionsCDPExecutor
)


class ExtensionsCDPExecutor(AbstractExtensionsCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def clear_storage_items(self, id_: str, storage_area: str) -> None:
		return self._execute_function("Extensions.clearStorageItems", locals())
	
	def get_storage_items(self, id_: str, storage_area: str, keys: Optional[List[str]] = None) -> dict:
		return self._execute_function("Extensions.getStorageItems", locals())
	
	def load_unpacked(self, path: str) -> str:
		return self._execute_function("Extensions.loadUnpacked", locals())
	
	def remove_storage_items(self, id_: str, storage_area: str, keys: List[str]) -> None:
		return self._execute_function("Extensions.removeStorageItems", locals())
	
	def set_storage_items(self, id_: str, storage_area: str, values: dict) -> None:
		return self._execute_function("Extensions.setStorageItems", locals())
	
	def uninstall(self, id_: str) -> None:
		return self._execute_function("Extensions.uninstall", locals())
