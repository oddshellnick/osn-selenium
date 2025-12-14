from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.abstract.executors.cdp.indexeddb import (
	AbstractIndexedDBCDPExecutor
)


class IndexedDBCDPExecutor(AbstractIndexedDBCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def clear_object_store(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Any] = None,
			database_name: str = None,
			object_store_name: str = None
	) -> None:
		return self._execute_function("IndexedDB.clearObjectStore", locals())
	
	def delete_database(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Any] = None,
			database_name: str = None
	) -> None:
		return self._execute_function("IndexedDB.deleteDatabase", locals())
	
	def delete_object_store_entries(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Any] = None,
			database_name: str = None,
			object_store_name: str = None,
			key_range: Any = None
	) -> None:
		return self._execute_function("IndexedDB.deleteObjectStoreEntries", locals())
	
	def disable(self) -> None:
		return self._execute_function("IndexedDB.disable", locals())
	
	def enable(self) -> None:
		return self._execute_function("IndexedDB.enable", locals())
	
	def get_metadata(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Any] = None,
			database_name: str = None,
			object_store_name: str = None
	) -> Tuple[float]:
		return self._execute_function("IndexedDB.getMetadata", locals())
	
	def request_data(
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
	) -> Tuple[List[Any]]:
		return self._execute_function("IndexedDB.requestData", locals())
	
	def request_database(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Any] = None,
			database_name: str = None
	) -> List[List[Any]]:
		return self._execute_function("IndexedDB.requestDatabase", locals())
	
	def request_database_names(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Any] = None
	) -> List[str]:
		return self._execute_function("IndexedDB.requestDatabaseNames", locals())
