from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	List
)
from osn_selenium.abstract.executors.cdp.dom_storage import (
	AbstractDomStorageCDPExecutor
)


class DomStorageCDPExecutor(AbstractDomStorageCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def clear(self, storage_id: Any) -> None:
		return await self._execute_function("DOMStorage.clear", locals())
	
	async def disable(self) -> None:
		return await self._execute_function("DOMStorage.disable", locals())
	
	async def enable(self) -> None:
		return await self._execute_function("DOMStorage.enable", locals())
	
	async def get_dom_storage_items(self, storage_id: Any) -> List[List[Any]]:
		return await self._execute_function("DOMStorage.getDOMStorageItems", locals())
	
	async def remove_dom_storage_item(self, storage_id: Any, key: str) -> None:
		return await self._execute_function("DOMStorage.removeDOMStorageItem", locals())
	
	async def set_dom_storage_item(self, storage_id: Any, key: str, value: str) -> None:
		return await self._execute_function("DOMStorage.setDOMStorageItem", locals())
