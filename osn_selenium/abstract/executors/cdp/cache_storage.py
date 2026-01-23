from abc import ABC, abstractmethod
from typing import (
	Any,
	Dict,
	List,
	Optional,
	Tuple
)


__all__ = ["AbstractCacheStorageCDPExecutor"]


class AbstractCacheStorageCDPExecutor(ABC):
	@abstractmethod
	def delete_cache(self, cache_id: str) -> None:
		...
	
	@abstractmethod
	def delete_entry(self, cache_id: str, request: str) -> None:
		...
	
	@abstractmethod
	def request_cache_names(
			self,
			security_origin: Optional[str] = None,
			storage_key: Optional[str] = None,
			storage_bucket: Optional[Dict[str, Any]] = None
	) -> List[Dict[str, Any]]:
		...
	
	@abstractmethod
	def request_cached_response(
			self,
			cache_id: str,
			request_url: str,
			request_headers: List[Dict[str, Any]]
	) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def request_entries(
			self,
			cache_id: str,
			skip_count: Optional[int] = None,
			page_size: Optional[int] = None,
			path_filter: Optional[str] = None
	) -> Tuple[List[Dict[str, Any]], float]:
		...
