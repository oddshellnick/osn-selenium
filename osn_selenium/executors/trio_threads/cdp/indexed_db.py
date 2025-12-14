from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.abstract.executors.cdp.indexed_db import (
	AbstractIndexedDbCDPExecutor
)


class IndexedDbCDPExecutor(AbstractIndexedDbCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def clear_object_store(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Any] = None,
			database_name: str = None,
			object_store_name: str = None
	) -> None:
		return await self._execute_function("IndexedDB.clearObjectStore", locals())
	
	async def delete_database(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Any] = None,
			database_name: str = None
	) -> None:
		return await self._execute_function("IndexedDB.deleteDatabase", locals())
	
	async def delete_object_store_entries(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Any] = None,
			database_name: str = None,
			object_store_name: str = None,
			key_range: Any = None
	) -> None:
		return await self._execute_function("IndexedDB.deleteObjectStoreEntries", locals())
	
	async def disable(self) -> None:
		return await self._execute_function("IndexedDB.disable", locals())
	
	async def enable(self) -> None:
		return await self._execute_function("IndexedDB.enable", locals())
	
	async def get_metadata(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Any] = None,
			database_name: str = None,
			object_store_name: str = None
	) -> Tuple[float, float]:
		return await self._execute_function("IndexedDB.getMetadata", locals())
	
	async def request_data(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Any] = None,
			database_name: str = None,
			object_store_name: str = None,
			index_name: Optional[str] = None,
			skip_count: int = None,
			page_size: int = None,
			key_range: Optional[Any] = None
	) -> Tuple[List[Any], bool]:
		return await self._execute_function("IndexedDB.requestData", locals())
	
	async def request_database(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Any] = None,
			database_name: str = None
	) -> Any:
		return await self._execute_function("IndexedDB.requestDatabase", locals())
	
	async def request_database_names(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Any] = None
	) -> List[str]:
		return await self._execute_function("IndexedDB.requestDatabaseNames", locals())
