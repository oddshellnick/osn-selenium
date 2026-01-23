from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.executors.unified.cdp.storage import (
	UnifiedStorageCDPExecutor
)
from osn_selenium.abstract.executors.cdp.storage import (
	AbstractStorageCDPExecutor
)


__all__ = ["StorageCDPExecutor"]


class StorageCDPExecutor(UnifiedStorageCDPExecutor, AbstractStorageCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedStorageCDPExecutor.__init__(self, execute_function=execute_function)
	
	def clear_cookies(self, browser_context_id: Optional[str] = None) -> None:
		return self._clear_cookies_impl(browser_context_id=browser_context_id)
	
	def clear_data_for_origin(self, origin: str, storage_types: str) -> None:
		return self._clear_data_for_origin_impl(origin=origin, storage_types=storage_types)
	
	def clear_data_for_storage_key(self, storage_key: str, storage_types: str) -> None:
		return self._clear_data_for_storage_key_impl(storage_key=storage_key, storage_types=storage_types)
	
	def clear_shared_storage_entries(self, owner_origin: str) -> None:
		return self._clear_shared_storage_entries_impl(owner_origin=owner_origin)
	
	def clear_trust_tokens(self, issuer_origin: str) -> bool:
		return self._clear_trust_tokens_impl(issuer_origin=issuer_origin)
	
	def delete_shared_storage_entry(self, owner_origin: str, key: str) -> None:
		return self._delete_shared_storage_entry_impl(owner_origin=owner_origin, key=key)
	
	def delete_storage_bucket(self, bucket: Dict[str, Any]) -> None:
		return self._delete_storage_bucket_impl(bucket=bucket)
	
	def get_affected_urls_for_third_party_cookie_metadata(self, first_party_url: str, third_party_urls: List[str]) -> List[str]:
		return self._get_affected_urls_for_third_party_cookie_metadata_impl(first_party_url=first_party_url, third_party_urls=third_party_urls)
	
	def get_cookies(self, browser_context_id: Optional[str] = None) -> List[Dict[str, Any]]:
		return self._get_cookies_impl(browser_context_id=browser_context_id)
	
	def get_interest_group_details(self, owner_origin: str, name: str) -> Any:
		return self._get_interest_group_details_impl(owner_origin=owner_origin, name=name)
	
	def get_related_website_sets(self) -> List[Dict[str, Any]]:
		return self._get_related_website_sets_impl()
	
	def get_shared_storage_entries(self, owner_origin: str) -> List[Dict[str, Any]]:
		return self._get_shared_storage_entries_impl(owner_origin=owner_origin)
	
	def get_shared_storage_metadata(self, owner_origin: str) -> Dict[str, Any]:
		return self._get_shared_storage_metadata_impl(owner_origin=owner_origin)
	
	def get_storage_key(self, frame_id: Optional[str] = None) -> str:
		return self._get_storage_key_impl(frame_id=frame_id)
	
	def get_storage_key_for_frame(self, frame_id: str) -> str:
		return self._get_storage_key_for_frame_impl(frame_id=frame_id)
	
	def get_trust_tokens(self) -> List[Dict[str, Any]]:
		return self._get_trust_tokens_impl()
	
	def get_usage_and_quota(self, origin: str) -> Tuple[float, float, bool, List[Dict[str, Any]]]:
		return self._get_usage_and_quota_impl(origin=origin)
	
	def override_quota_for_origin(self, origin: str, quota_size: Optional[float] = None) -> None:
		return self._override_quota_for_origin_impl(origin=origin, quota_size=quota_size)
	
	def reset_shared_storage_budget(self, owner_origin: str) -> None:
		return self._reset_shared_storage_budget_impl(owner_origin=owner_origin)
	
	def run_bounce_tracking_mitigations(self) -> List[str]:
		return self._run_bounce_tracking_mitigations_impl()
	
	def send_pending_attribution_reports(self) -> int:
		return self._send_pending_attribution_reports_impl()
	
	def set_attribution_reporting_local_testing_mode(self, enabled: bool) -> None:
		return self._set_attribution_reporting_local_testing_mode_impl(enabled=enabled)
	
	def set_attribution_reporting_tracking(self, enable: bool) -> None:
		return self._set_attribution_reporting_tracking_impl(enable=enable)
	
	def set_cookies(
			self,
			cookies: List[Dict[str, Any]],
			browser_context_id: Optional[str] = None
	) -> None:
		return self._set_cookies_impl(cookies=cookies, browser_context_id=browser_context_id)
	
	def set_interest_group_auction_tracking(self, enable: bool) -> None:
		return self._set_interest_group_auction_tracking_impl(enable=enable)
	
	def set_interest_group_tracking(self, enable: bool) -> None:
		return self._set_interest_group_tracking_impl(enable=enable)
	
	def set_protected_audience_k_anonymity(self, owner: str, name: str, hashes: List[str]) -> None:
		return self._set_protected_audience_k_anonymity_impl(owner=owner, name=name, hashes=hashes)
	
	def set_shared_storage_entry(
			self,
			owner_origin: str,
			key: str,
			value: str,
			ignore_if_present: Optional[bool] = None
	) -> None:
		return self._set_shared_storage_entry_impl(
				owner_origin=owner_origin,
				key=key,
				value=value,
				ignore_if_present=ignore_if_present
		)
	
	def set_shared_storage_tracking(self, enable: bool) -> None:
		return self._set_shared_storage_tracking_impl(enable=enable)
	
	def set_storage_bucket_tracking(self, storage_key: str, enable: bool) -> None:
		return self._set_storage_bucket_tracking_impl(storage_key=storage_key, enable=enable)
	
	def track_cache_storage_for_origin(self, origin: str) -> None:
		return self._track_cache_storage_for_origin_impl(origin=origin)
	
	def track_cache_storage_for_storage_key(self, storage_key: str) -> None:
		return self._track_cache_storage_for_storage_key_impl(storage_key=storage_key)
	
	def track_indexed_db_for_origin(self, origin: str) -> None:
		return self._track_indexed_db_for_origin_impl(origin=origin)
	
	def track_indexed_db_for_storage_key(self, storage_key: str) -> None:
		return self._track_indexed_db_for_storage_key_impl(storage_key=storage_key)
	
	def untrack_cache_storage_for_origin(self, origin: str) -> None:
		return self._untrack_cache_storage_for_origin_impl(origin=origin)
	
	def untrack_cache_storage_for_storage_key(self, storage_key: str) -> None:
		return self._untrack_cache_storage_for_storage_key_impl(storage_key=storage_key)
	
	def untrack_indexed_db_for_origin(self, origin: str) -> None:
		return self._untrack_indexed_db_for_origin_impl(origin=origin)
	
	def untrack_indexed_db_for_storage_key(self, storage_key: str) -> None:
		return self._untrack_indexed_db_for_storage_key_impl(storage_key=storage_key)
