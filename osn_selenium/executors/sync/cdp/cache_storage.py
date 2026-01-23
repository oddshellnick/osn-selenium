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


class CacheStorageCDPExecutor(UnifiedCacheStorageCDPExecutor, AbstractCacheStorageCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedCacheStorageCDPExecutor.__init__(self, execute_function=execute_function)
	
	def delete_cache(self, cache_id: str) -> None:
		return self._delete_cache_impl(cache_id=cache_id)
	
	def delete_entry(self, cache_id: str, request: str) -> None:
		return self._delete_entry_impl(cache_id=cache_id, request=request)
	
	def request_cache_names(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Dict[str, Any]] = None
	) -> List[Dict[str, Any]]:
		return self._request_cache_names_impl(
				security_origin=security_origin,
				storage_key=storage_key,
				storage_bucket=storage_bucket
		)
	
	def request_cached_response(
			self,
			cache_id: str,
			request_url: str,
			request_headers: List[Dict[str, Any]]
	) -> Dict[str, Any]:
		return self._request_cached_response_impl(
				cache_id=cache_id,
				request_url=request_url,
				request_headers=request_headers
		)
	
	def request_entries(
			self,
			cache_id: str,
			skip_count: Optional[int] = None,
			page_size: Optional[int] = None,
			path_filter: Optional[str] = None
	) -> Tuple[List[Dict[str, Any]], float]:
		return self._request_entries_impl(
				cache_id=cache_id,
				skip_count=skip_count,
				page_size=page_size,
				path_filter=path_filter
		)
