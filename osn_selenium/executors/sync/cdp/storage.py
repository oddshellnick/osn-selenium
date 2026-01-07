from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.abstract.executors.cdp.storage import (
	AbstractStorageCDPExecutor
)


class StorageCDPExecutor(AbstractStorageCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def clear_cookies(self, browser_context_id: Optional[str] = None) -> None:
		return self._execute_function("Storage.clearCookies", locals())
	
	def clear_data_for_origin(self, origin: str, storage_types: str) -> None:
		return self._execute_function("Storage.clearDataForOrigin", locals())
	
	def clear_data_for_storage_key(self, storage_key: str, storage_types: str) -> None:
		return self._execute_function("Storage.clearDataForStorageKey", locals())
	
	def clear_shared_storage_entries(self, owner_origin: str) -> None:
		return self._execute_function("Storage.clearSharedStorageEntries", locals())
	
	def clear_trust_tokens(self, issuer_origin: str) -> bool:
		return self._execute_function("Storage.clearTrustTokens", locals())
	
	def delete_shared_storage_entry(self, owner_origin: str, key: str) -> None:
		return self._execute_function("Storage.deleteSharedStorageEntry", locals())
	
	def delete_storage_bucket(self, bucket: Any) -> None:
		return self._execute_function("Storage.deleteStorageBucket", locals())
	
	def get_affected_urls_for_third_party_cookie_metadata(self, first_party_url: str, third_party_urls: List[str]) -> List[str]:
		return self._execute_function("Storage.getAffectedUrlsForThirdPartyCookieMetadata", locals())
	
	def get_cookies(self, browser_context_id: Optional[str] = None) -> List[Any]:
		return self._execute_function("Storage.getCookies", locals())
	
	def get_interest_group_details(self, owner_origin: str, name: str) -> dict:
		return self._execute_function("Storage.getInterestGroupDetails", locals())
	
	def get_related_website_sets(self) -> List[List[str]]:
		return self._execute_function("Storage.getRelatedWebsiteSets", locals())
	
	def get_shared_storage_entries(self, owner_origin: str) -> List[Any]:
		return self._execute_function("Storage.getSharedStorageEntries", locals())
	
	def get_shared_storage_metadata(self, owner_origin: str) -> Any:
		return self._execute_function("Storage.getSharedStorageMetadata", locals())
	
	def get_storage_key(self, frame_id: Optional[str] = None) -> str:
		return self._execute_function("Storage.getStorageKey", locals())
	
	def get_storage_key_for_frame(self, frame_id: str) -> str:
		return self._execute_function("Storage.getStorageKeyForFrame", locals())
	
	def get_trust_tokens(self) -> List[Any]:
		return self._execute_function("Storage.getTrustTokens", locals())
	
	def get_usage_and_quota(self, origin: str) -> Tuple[float]:
		return self._execute_function("Storage.getUsageAndQuota", locals())
	
	def override_quota_for_origin(self, origin: str, quota_size: Optional[float] = None) -> None:
		return self._execute_function("Storage.overrideQuotaForOrigin", locals())
	
	def reset_shared_storage_budget(self, owner_origin: str) -> None:
		return self._execute_function("Storage.resetSharedStorageBudget", locals())
	
	def run_bounce_tracking_mitigations(self) -> List[str]:
		return self._execute_function("Storage.runBounceTrackingMitigations", locals())
	
	def send_pending_attribution_reports(self) -> int:
		return self._execute_function("Storage.sendPendingAttributionReports", locals())
	
	def set_attribution_reporting_local_testing_mode(self, enabled: bool) -> None:
		return self._execute_function("Storage.setAttributionReportingLocalTestingMode", locals())
	
	def set_attribution_reporting_tracking(self, enable: bool) -> None:
		return self._execute_function("Storage.setAttributionReportingTracking", locals())
	
	def set_cookies(self, cookies: List[Any], browser_context_id: Optional[str] = None) -> None:
		return self._execute_function("Storage.setCookies", locals())
	
	def set_interest_group_auction_tracking(self, enable: bool) -> None:
		return self._execute_function("Storage.setInterestGroupAuctionTracking", locals())
	
	def set_interest_group_tracking(self, enable: bool) -> None:
		return self._execute_function("Storage.setInterestGroupTracking", locals())
	
	def set_protected_audience_k_anonymity(self, owner: str, name: str, hashes: List[str]) -> None:
		return self._execute_function("Storage.setProtectedAudienceKAnonymity", locals())
	
	def set_shared_storage_entry(
			self,
			owner_origin: str,
			key: str,
			value: str,
			ignore_if_present: Optional[bool] = None
	) -> None:
		return self._execute_function("Storage.setSharedStorageEntry", locals())
	
	def set_shared_storage_tracking(self, enable: bool) -> None:
		return self._execute_function("Storage.setSharedStorageTracking", locals())
	
	def set_storage_bucket_tracking(self, storage_key: str, enable: bool) -> None:
		return self._execute_function("Storage.setStorageBucketTracking", locals())
	
	def track_cache_storage_for_origin(self, origin: str) -> None:
		return self._execute_function("Storage.trackCacheStorageForOrigin", locals())
	
	def track_cache_storage_for_storage_key(self, storage_key: str) -> None:
		return self._execute_function("Storage.trackCacheStorageForStorageKey", locals())
	
	def track_indexed_db_for_origin(self, origin: str) -> None:
		return self._execute_function("Storage.trackIndexedDBForOrigin", locals())
	
	def track_indexed_db_for_storage_key(self, storage_key: str) -> None:
		return self._execute_function("Storage.trackIndexedDBForStorageKey", locals())
	
	def untrack_cache_storage_for_origin(self, origin: str) -> None:
		return self._execute_function("Storage.untrackCacheStorageForOrigin", locals())
	
	def untrack_cache_storage_for_storage_key(self, storage_key: str) -> None:
		return self._execute_function("Storage.untrackCacheStorageForStorageKey", locals())
	
	def untrack_indexed_db_for_origin(self, origin: str) -> None:
		return self._execute_function("Storage.untrackIndexedDBForOrigin", locals())
	
	def untrack_indexed_db_for_storage_key(self, storage_key: str) -> None:
		return self._execute_function("Storage.untrackIndexedDBForStorageKey", locals())
