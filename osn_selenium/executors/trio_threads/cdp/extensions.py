from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	List,
	Optional
)
from osn_selenium.abstract.executors.cdp.extensions import (
	AbstractExtensionsCDPExecutor
)


class ExtensionsCDPExecutor(AbstractExtensionsCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def clear_storage_items(self, id_: str, storage_area: str) -> None:
		return await self._execute_function("Extensions.clearStorageItems", locals())
	
	async def get_storage_items(self, id_: str, storage_area: str, keys: Optional[List[str]] = None) -> dict:
		return await self._execute_function("Extensions.getStorageItems", locals())
	
	async def load_unpacked(self, path: str) -> str:
		return await self._execute_function("Extensions.loadUnpacked", locals())
	
	async def remove_storage_items(self, id_: str, storage_area: str, keys: List[str]) -> None:
		return await self._execute_function("Extensions.removeStorageItems", locals())
	
	async def set_storage_items(self, id_: str, storage_area: str, values: dict) -> None:
		return await self._execute_function("Extensions.setStorageItems", locals())
	
	async def uninstall(self, id_: str) -> None:
		return await self._execute_function("Extensions.uninstall", locals())
