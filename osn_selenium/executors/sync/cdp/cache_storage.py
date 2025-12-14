from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.abstract.executors.cdp.cache_storage import (
	AbstractCacheStorageCDPExecutor
)


class CacheStorageCDPExecutor(AbstractCacheStorageCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def delete_cache(self, cache_id: str) -> None:
		return self._execute_function("CacheStorage.deleteCache", locals())
	
	def delete_entry(self, cache_id: str, request: str) -> None:
		return self._execute_function("CacheStorage.deleteEntry", locals())
	
	def request_cache_names(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Any] = None
	) -> List[Any]:
		return self._execute_function("CacheStorage.requestCacheNames", locals())
	
	def request_cached_response(self, cache_id: str, request_url: str, request_headers: List[Any]) -> Any:
		return self._execute_function("CacheStorage.requestCachedResponse", locals())
	
	def request_entries(
			self,
			cache_id: str,
			skip_count: Optional[int] = None,
			page_size: Optional[int] = None,
			path_filter: Optional[str] = None
	) -> Tuple[List[Any], float]:
		return self._execute_function("CacheStorage.requestEntries", locals())
