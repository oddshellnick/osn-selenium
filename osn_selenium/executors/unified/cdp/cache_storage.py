from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)


__all__ = ["UnifiedCacheStorageCDPExecutor"]


class UnifiedCacheStorageCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _delete_cache_impl(self, cache_id: str) -> None:
		return self._execute_function("CacheStorage.deleteCache", {"cache_id": cache_id})
	
	def _delete_entry_impl(self, cache_id: str, request: str) -> None:
		return self._execute_function("CacheStorage.deleteEntry", {"cache_id": cache_id, "request": request})
	
	def _request_cache_names_impl(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Dict[str, Any]] = None
	) -> List[Dict[str, Any]]:
		return self._execute_function(
				"CacheStorage.requestCacheNames",
				{
					"security_origin": security_origin,
					"storage_key": storage_key,
					"storage_bucket": storage_bucket
				}
		)
	
	def _request_cached_response_impl(
			self,
			cache_id: str,
			request_url: str,
			request_headers: List[Dict[str, Any]]
	) -> Dict[str, Any]:
		return self._execute_function(
				"CacheStorage.requestCachedResponse",
				{
					"cache_id": cache_id,
					"request_url": request_url,
					"request_headers": request_headers
				}
		)
	
	def _request_entries_impl(
			self,
			cache_id: str,
			skip_count: Optional[int] = None,
			page_size: Optional[int] = None,
			path_filter: Optional[str] = None
	) -> Tuple[List[Dict[str, Any]], float]:
		return self._execute_function(
				"CacheStorage.requestEntries",
				{
					"cache_id": cache_id,
					"skip_count": skip_count,
					"page_size": page_size,
					"path_filter": path_filter
				}
		)
