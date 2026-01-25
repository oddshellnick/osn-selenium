from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)


__all__ = ["UnifiedIndexedDbCDPExecutor"]


class UnifiedIndexedDbCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _clear_object_store_impl(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Dict[str, Any]] = None,
			database_name: str = None,
			object_store_name: str = None
	) -> None:
		return self._execute_function(
				"IndexedDB.clearObjectStore",
				{
					"security_origin": security_origin,
					"storage_key": storage_key,
					"storage_bucket": storage_bucket,
					"database_name": database_name,
					"object_store_name": object_store_name
				}
		)
	
	def _delete_database_impl(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Dict[str, Any]] = None,
			database_name: str = None
	) -> None:
		return self._execute_function(
				"IndexedDB.deleteDatabase",
				{
					"security_origin": security_origin,
					"storage_key": storage_key,
					"storage_bucket": storage_bucket,
					"database_name": database_name
				}
		)
	
	def _delete_object_store_entries_impl(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Dict[str, Any]] = None,
			database_name: str = None,
			object_store_name: str = None,
			key_range: Dict[str, Any] = None
	) -> None:
		return self._execute_function(
				"IndexedDB.deleteObjectStoreEntries",
				{
					"security_origin": security_origin,
					"storage_key": storage_key,
					"storage_bucket": storage_bucket,
					"database_name": database_name,
					"object_store_name": object_store_name,
					"key_range": key_range
				}
		)
	
	def _disable_impl(self) -> None:
		return self._execute_function("IndexedDB.disable", {})
	
	def _enable_impl(self) -> None:
		return self._execute_function("IndexedDB.enable", {})
	
	def _get_metadata_impl(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Dict[str, Any]] = None,
			database_name: str = None,
			object_store_name: str = None
	) -> Tuple[float, float]:
		return self._execute_function(
				"IndexedDB.getMetadata",
				{
					"security_origin": security_origin,
					"storage_key": storage_key,
					"storage_bucket": storage_bucket,
					"database_name": database_name,
					"object_store_name": object_store_name
				}
		)
	
	def _request_data_impl(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Dict[str, Any]] = None,
			database_name: str = None,
			object_store_name: str = None,
			index_name: Optional[str] = None,
			skip_count: int = None,
			page_size: int = None,
			key_range: Optional[Dict[str, Any]] = None
	) -> Tuple[List[Dict[str, Any]], bool]:
		return self._execute_function(
				"IndexedDB.requestData",
				{
					"security_origin": security_origin,
					"storage_key": storage_key,
					"storage_bucket": storage_bucket,
					"database_name": database_name,
					"object_store_name": object_store_name,
					"index_name": index_name,
					"skip_count": skip_count,
					"page_size": page_size,
					"key_range": key_range
				}
		)
	
	def _request_database_impl(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Dict[str, Any]] = None,
			database_name: str = None
	) -> Dict[str, Any]:
		return self._execute_function(
				"IndexedDB.requestDatabase",
				{
					"security_origin": security_origin,
					"storage_key": storage_key,
					"storage_bucket": storage_bucket,
					"database_name": database_name
				}
		)
	
	def _request_database_names_impl(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Dict[str, Any]] = None
	) -> List[str]:
		return self._execute_function(
				"IndexedDB.requestDatabaseNames",
				{
					"security_origin": security_origin,
					"storage_key": storage_key,
					"storage_bucket": storage_bucket
				}
		)
