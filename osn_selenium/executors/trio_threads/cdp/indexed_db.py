import trio
from osn_selenium.base_mixin import TrioThreadMixin
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


class IndexedDbCDPExecutor(
		UnifiedIndexedDbCDPExecutor,
		TrioThreadMixin,
		AbstractIndexedDbCDPExecutor
):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedIndexedDbCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def clear_object_store(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Dict[str, Any]] = None,
			database_name: str = None,
			object_store_name: str = None
	) -> None:
		return await self.sync_to_trio(sync_function=self._clear_object_store_impl)(
				security_origin=security_origin,
				storage_key=storage_key,
				storage_bucket=storage_bucket,
				database_name=database_name,
				object_store_name=object_store_name
		)
	
	async def delete_database(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Dict[str, Any]] = None,
			database_name: str = None
	) -> None:
		return await self.sync_to_trio(sync_function=self._delete_database_impl)(
				security_origin=security_origin,
				storage_key=storage_key,
				storage_bucket=storage_bucket,
				database_name=database_name
		)
	
	async def delete_object_store_entries(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Dict[str, Any]] = None,
			database_name: str = None,
			object_store_name: str = None,
			key_range: Dict[str, Any] = None
	) -> None:
		return await self.sync_to_trio(sync_function=self._delete_object_store_entries_impl)(
				security_origin=security_origin,
				storage_key=storage_key,
				storage_bucket=storage_bucket,
				database_name=database_name,
				object_store_name=object_store_name,
				key_range=key_range
		)
	
	async def disable(self) -> None:
		return await self.sync_to_trio(sync_function=self._disable_impl)()
	
	async def enable(self) -> None:
		return await self.sync_to_trio(sync_function=self._enable_impl)()
	
	async def get_metadata(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Dict[str, Any]] = None,
			database_name: str = None,
			object_store_name: str = None
	) -> Tuple[float, float]:
		return await self.sync_to_trio(sync_function=self._get_metadata_impl)(
				security_origin=security_origin,
				storage_key=storage_key,
				storage_bucket=storage_bucket,
				database_name=database_name,
				object_store_name=object_store_name
		)
	
	async def request_data(
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
		return await self.sync_to_trio(sync_function=self._request_data_impl)(
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
	
	async def request_database(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Dict[str, Any]] = None,
			database_name: str = None
	) -> Dict[str, Any]:
		return await self.sync_to_trio(sync_function=self._request_database_impl)(
				security_origin=security_origin,
				storage_key=storage_key,
				storage_bucket=storage_bucket,
				database_name=database_name
		)
	
	async def request_database_names(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Dict[str, Any]] = None
	) -> List[str]:
		return await self.sync_to_trio(sync_function=self._request_database_names_impl)(
				security_origin=security_origin,
				storage_key=storage_key,
				storage_bucket=storage_bucket
		)
