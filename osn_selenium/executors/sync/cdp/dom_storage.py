from typing import (
	Any,
	Callable,
	Dict,
	List
)
from osn_selenium.abstract.executors.cdp.dom_storage import (
	AbstractDomStorageCDPExecutor
)


class DomStorageCDPExecutor(AbstractDomStorageCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def clear(self, storage_id: Any) -> None:
		return self._execute_function("DOMStorage.clear", locals())
	
	def disable(self) -> None:
		return self._execute_function("DOMStorage.disable", locals())
	
	def enable(self) -> None:
		return self._execute_function("DOMStorage.enable", locals())
	
	def get_dom_storage_items(self, storage_id: Any) -> List[List[Any]]:
		return self._execute_function("DOMStorage.getDOMStorageItems", locals())
	
	def remove_dom_storage_item(self, storage_id: Any, key: str) -> None:
		return self._execute_function("DOMStorage.removeDOMStorageItem", locals())
	
	def set_dom_storage_item(self, storage_id: Any, key: str, value: str) -> None:
		return self._execute_function("DOMStorage.setDOMStorageItem", locals())
