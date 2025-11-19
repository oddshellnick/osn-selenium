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
from osn_selenium.executors.unified.cdp.cache_storage import (
	UnifiedCacheStorageCDPExecutor
)
from osn_selenium.abstract.executors.cdp.cache_storage import (
	AbstractCacheStorageCDPExecutor
)


__all__ = ["CacheStorageCDPExecutor"]


class CacheStorageCDPExecutor(
		UnifiedCacheStorageCDPExecutor,
		TrioThreadMixin,
		AbstractCacheStorageCDPExecutor
):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedCacheStorageCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def delete_cache(self, cache_id: str) -> None:
		return await self.sync_to_trio(sync_function=self._delete_cache_impl)(cache_id=cache_id)
	
	async def delete_entry(self, cache_id: str, request: str) -> None:
		return await self.sync_to_trio(sync_function=self._delete_entry_impl)(cache_id=cache_id, request=request)
	
	async def request_cache_names(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Dict[str, Any]] = None
	) -> List[Dict[str, Any]]:
		return await self.sync_to_trio(sync_function=self._request_cache_names_impl)(
				security_origin=security_origin,
				storage_key=storage_key,
				storage_bucket=storage_bucket
		)
	
	async def request_cached_response(
			self,
			cache_id: str,
			request_url: str,
			request_headers: List[Dict[str, Any]]
	) -> Dict[str, Any]:
		return await self.sync_to_trio(sync_function=self._request_cached_response_impl)(
				cache_id=cache_id,
				request_url=request_url,
				request_headers=request_headers
		)
	
	async def request_entries(
			self,
			cache_id: str,
			skip_count: Optional[int] = None,
			page_size: Optional[int] = None,
			path_filter: Optional[str] = None
	) -> Tuple[List[Dict[str, Any]], float]:
		return await self.sync_to_trio(sync_function=self._request_entries_impl)(
				cache_id=cache_id,
				skip_count=skip_count,
				page_size=page_size,
				path_filter=path_filter
		)
