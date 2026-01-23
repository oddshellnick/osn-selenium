from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.executors.unified.cdp.indexed_db import (
	UnifiedIndexedDbCDPExecutor
)
from osn_selenium.abstract.executors.cdp.indexed_db import (
	AbstractIndexedDbCDPExecutor
)


__all__ = ["IndexedDbCDPExecutor"]


class IndexedDbCDPExecutor(UnifiedIndexedDbCDPExecutor, AbstractIndexedDbCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedIndexedDbCDPExecutor.__init__(self, execute_function=execute_function)
	
	def clear_object_store(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Dict[str, Any]] = None,
			database_name: str = None,
			object_store_name: str = None
	) -> None:
		return self._clear_object_store_impl(
				security_origin=security_origin,
				storage_key=storage_key,
				storage_bucket=storage_bucket,
				database_name=database_name,
				object_store_name=object_store_name
		)
	
	def delete_database(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Dict[str, Any]] = None,
			database_name: str = None
	) -> None:
		return self._delete_database_impl(
				security_origin=security_origin,
				storage_key=storage_key,
				storage_bucket=storage_bucket,
				database_name=database_name
		)
	
	def delete_object_store_entries(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Dict[str, Any]] = None,
			database_name: str = None,
			object_store_name: str = None,
			key_range: Dict[str, Any] = None
	) -> None:
		return self._delete_object_store_entries_impl(
				security_origin=security_origin,
				storage_key=storage_key,
				storage_bucket=storage_bucket,
				database_name=database_name,
				object_store_name=object_store_name,
				key_range=key_range
		)
	
	def disable(self) -> None:
		return self._disable_impl()
	
	def enable(self) -> None:
		return self._enable_impl()
	
	def get_metadata(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Dict[str, Any]] = None,
			database_name: str = None,
			object_store_name: str = None
	) -> Tuple[float, float]:
		return self._get_metadata_impl(
				security_origin=security_origin,
				storage_key=storage_key,
				storage_bucket=storage_bucket,
				database_name=database_name,
				object_store_name=object_store_name
		)
	
	def request_data(
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
		return self._request_data_impl(
				security_origin=security_origin,
				storage_key=storage_key,
				storage_bucket=storage_bucket,
				database_name=database_name,
				object_store_name=object_store_name,
				index_name=index_name,
				skip_count=skip_count,
				page_size=page_size,
				key_range=key_range
		)
	
	def request_database(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Dict[str, Any]] = None,
			database_name: str = None
	) -> Dict[str, Any]:
		return self._request_database_impl(
				security_origin=security_origin,
				storage_key=storage_key,
				storage_bucket=storage_bucket,
				database_name=database_name
		)
	
	def request_database_names(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Dict[str, Any]] = None
	) -> List[str]:
		return self._request_database_names_impl(
				security_origin=security_origin,
				storage_key=storage_key,
				storage_bucket=storage_bucket
		)
