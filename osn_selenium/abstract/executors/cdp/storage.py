from abc import ABC, abstractmethod
from typing import (
	Any,
	Dict,
	List,
	Optional,
	Tuple
)


__all__ = ["AbstractStorageCDPExecutor"]


class AbstractStorageCDPExecutor(ABC):
	@abstractmethod
	def clear_cookies(self, browser_context_id: Optional[str] = None) -> None:
		...
	
	@abstractmethod
	def clear_data_for_origin(self, origin: str, storage_types: str) -> None:
		...
	
	@abstractmethod
	def clear_data_for_storage_key(self, storage_key: str, storage_types: str) -> None:
		...
	
	@abstractmethod
	def clear_shared_storage_entries(self, owner_origin: str) -> None:
		...
	
	@abstractmethod
	def clear_trust_tokens(self, issuer_origin: str) -> bool:
		...
	
	@abstractmethod
	def delete_shared_storage_entry(self, owner_origin: str, key: str) -> None:
		...
	
	@abstractmethod
	def delete_storage_bucket(self, bucket: Dict[str, Any]) -> None:
		...
	
	@abstractmethod
	def get_affected_urls_for_third_party_cookie_metadata(self, first_party_url: str, third_party_urls: List[str]) -> List[str]:
		...
	
	@abstractmethod
	def get_cookies(self, browser_context_id: Optional[str] = None) -> List[Dict[str, Any]]:
		...
	
	@abstractmethod
	def get_interest_group_details(self, owner_origin: str, name: str) -> Any:
		...
	
	@abstractmethod
	def get_related_website_sets(self) -> List[Dict[str, Any]]:
		...
	
	@abstractmethod
	def get_shared_storage_entries(self, owner_origin: str) -> List[Dict[str, Any]]:
		...
	
	@abstractmethod
	def get_shared_storage_metadata(self, owner_origin: str) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def get_storage_key(self, frame_id: Optional[str] = None) -> str:
		...
	
	@abstractmethod
	def get_storage_key_for_frame(self, frame_id: str) -> str:
		...
	
	@abstractmethod
	def get_trust_tokens(self) -> List[Dict[str, Any]]:
		...
	
	@abstractmethod
	def get_usage_and_quota(self, origin: str) -> Tuple[float, float, bool, List[Dict[str, Any]]]:
		...
	
	@abstractmethod
	def override_quota_for_origin(self, origin: str, quota_size: Optional[float] = None) -> None:
		...
	
	@abstractmethod
	def reset_shared_storage_budget(self, owner_origin: str) -> None:
		...
	
	@abstractmethod
	def run_bounce_tracking_mitigations(self) -> List[str]:
		...
	
	@abstractmethod
	def send_pending_attribution_reports(self) -> int:
		...
	
	@abstractmethod
	def set_attribution_reporting_local_testing_mode(self, enabled: bool) -> None:
		...
	
	@abstractmethod
	def set_attribution_reporting_tracking(self, enable: bool) -> None:
		...
	
	@abstractmethod
	def set_cookies(
			self,
			cookies: List[Dict[str, Any]],
			browser_context_id: Optional[str] = None
	) -> None:
		...
	
	@abstractmethod
	def set_interest_group_auction_tracking(self, enable: bool) -> None:
		...
	
	@abstractmethod
	def set_interest_group_tracking(self, enable: bool) -> None:
		...
	
	@abstractmethod
	def set_protected_audience_k_anonymity(self, owner: str, name: str, hashes: List[str]) -> None:
		...
	
	@abstractmethod
	def set_shared_storage_entry(
			self,
			owner_origin: str,
			key: str,
			value: str,
			ignore_if_present: Optional[bool] = None
	) -> None:
		...
	
	@abstractmethod
	def set_shared_storage_tracking(self, enable: bool) -> None:
		...
	
	@abstractmethod
	def set_storage_bucket_tracking(self, storage_key: str, enable: bool) -> None:
		...
	
	@abstractmethod
	def track_cache_storage_for_origin(self, origin: str) -> None:
		...
	
	@abstractmethod
	def track_cache_storage_for_storage_key(self, storage_key: str) -> None:
		...
	
	@abstractmethod
	def track_indexed_db_for_origin(self, origin: str) -> None:
		...
	
	@abstractmethod
	def track_indexed_db_for_storage_key(self, storage_key: str) -> None:
		...
	
	@abstractmethod
	def untrack_cache_storage_for_origin(self, origin: str) -> None:
		...
	
	@abstractmethod
	def untrack_cache_storage_for_storage_key(self, storage_key: str) -> None:
		...
	
	@abstractmethod
	def untrack_indexed_db_for_origin(self, origin: str) -> None:
		...
	
	@abstractmethod
	def untrack_indexed_db_for_storage_key(self, storage_key: str) -> None:
		...
