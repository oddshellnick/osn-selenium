from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)


__all__ = ["UnifiedStorageCDPExecutor"]


class UnifiedStorageCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _clear_cookies_impl(self, browser_context_id: Optional[str] = None) -> None:
		return self._execute_function("Storage.clearCookies", {"browser_context_id": browser_context_id})
	
	def _clear_data_for_origin_impl(self, origin: str, storage_types: str) -> None:
		return self._execute_function(
				"Storage.clearDataForOrigin",
				{"origin": origin, "storage_types": storage_types}
		)
	
	def _clear_data_for_storage_key_impl(self, storage_key: str, storage_types: str) -> None:
		return self._execute_function(
				"Storage.clearDataForStorageKey",
				{"storage_key": storage_key, "storage_types": storage_types}
		)
	
	def _clear_shared_storage_entries_impl(self, owner_origin: str) -> None:
		return self._execute_function("Storage.clearSharedStorageEntries", {"owner_origin": owner_origin})
	
	def _clear_trust_tokens_impl(self, issuer_origin: str) -> bool:
		return self._execute_function("Storage.clearTrustTokens", {"issuer_origin": issuer_origin})
	
	def _delete_shared_storage_entry_impl(self, owner_origin: str, key: str) -> None:
		return self._execute_function(
				"Storage.deleteSharedStorageEntry",
				{"owner_origin": owner_origin, "key": key}
		)
	
	def _delete_storage_bucket_impl(self, bucket: Dict[str, Any]) -> None:
		return self._execute_function("Storage.deleteStorageBucket", {"bucket": bucket})
	
	def _get_affected_urls_for_third_party_cookie_metadata_impl(self, first_party_url: str, third_party_urls: List[str]) -> List[str]:
		return self._execute_function(
				"Storage.getAffectedUrlsForThirdPartyCookieMetadata",
				{
					"first_party_url": first_party_url,
					"third_party_urls": third_party_urls
				}
		)
	
	def _get_cookies_impl(self, browser_context_id: Optional[str] = None) -> List[Dict[str, Any]]:
		return self._execute_function("Storage.getCookies", {"browser_context_id": browser_context_id})
	
	def _get_interest_group_details_impl(self, owner_origin: str, name: str) -> Any:
		return self._execute_function(
				"Storage.getInterestGroupDetails",
				{"owner_origin": owner_origin, "name": name}
		)
	
	def _get_related_website_sets_impl(self) -> List[Dict[str, Any]]:
		return self._execute_function("Storage.getRelatedWebsiteSets", {})
	
	def _get_shared_storage_entries_impl(self, owner_origin: str) -> List[Dict[str, Any]]:
		return self._execute_function("Storage.getSharedStorageEntries", {"owner_origin": owner_origin})
	
	def _get_shared_storage_metadata_impl(self, owner_origin: str) -> Dict[str, Any]:
		return self._execute_function("Storage.getSharedStorageMetadata", {"owner_origin": owner_origin})
	
	def _get_storage_key_for_frame_impl(self, frame_id: str) -> str:
		return self._execute_function("Storage.getStorageKeyForFrame", {"frame_id": frame_id})
	
	def _get_storage_key_impl(self, frame_id: Optional[str] = None) -> str:
		return self._execute_function("Storage.getStorageKey", {"frame_id": frame_id})
	
	def _get_trust_tokens_impl(self) -> List[Dict[str, Any]]:
		return self._execute_function("Storage.getTrustTokens", {})
	
	def _get_usage_and_quota_impl(self, origin: str) -> Tuple[float, float, bool, List[Dict[str, Any]]]:
		return self._execute_function("Storage.getUsageAndQuota", {"origin": origin})
	
	def _override_quota_for_origin_impl(self, origin: str, quota_size: Optional[float] = None) -> None:
		return self._execute_function(
				"Storage.overrideQuotaForOrigin",
				{"origin": origin, "quota_size": quota_size}
		)
	
	def _reset_shared_storage_budget_impl(self, owner_origin: str) -> None:
		return self._execute_function("Storage.resetSharedStorageBudget", {"owner_origin": owner_origin})
	
	def _run_bounce_tracking_mitigations_impl(self) -> List[str]:
		return self._execute_function("Storage.runBounceTrackingMitigations", {})
	
	def _send_pending_attribution_reports_impl(self) -> int:
		return self._execute_function("Storage.sendPendingAttributionReports", {})
	
	def _set_attribution_reporting_local_testing_mode_impl(self, enabled: bool) -> None:
		return self._execute_function("Storage.setAttributionReportingLocalTestingMode", {"enabled": enabled})
	
	def _set_attribution_reporting_tracking_impl(self, enable: bool) -> None:
		return self._execute_function("Storage.setAttributionReportingTracking", {"enable": enable})
	
	def _set_cookies_impl(
			self,
			cookies: List[Dict[str, Any]],
			browser_context_id: Optional[str] = None
	) -> None:
		return self._execute_function(
				"Storage.setCookies",
				{"cookies": cookies, "browser_context_id": browser_context_id}
		)
	
	def _set_interest_group_auction_tracking_impl(self, enable: bool) -> None:
		return self._execute_function("Storage.setInterestGroupAuctionTracking", {"enable": enable})
	
	def _set_interest_group_tracking_impl(self, enable: bool) -> None:
		return self._execute_function("Storage.setInterestGroupTracking", {"enable": enable})
	
	def _set_protected_audience_k_anonymity_impl(self, owner: str, name: str, hashes: List[str]) -> None:
		return self._execute_function(
				"Storage.setProtectedAudienceKAnonymity",
				{"owner": owner, "name": name, "hashes": hashes}
		)
	
	def _set_shared_storage_entry_impl(
			self,
			owner_origin: str,
			key: str,
			value: str,
			ignore_if_present: Optional[bool] = None
	) -> None:
		return self._execute_function(
				"Storage.setSharedStorageEntry",
				{
					"owner_origin": owner_origin,
					"key": key,
					"value": value,
					"ignore_if_present": ignore_if_present
				}
		)
	
	def _set_shared_storage_tracking_impl(self, enable: bool) -> None:
		return self._execute_function("Storage.setSharedStorageTracking", {"enable": enable})
	
	def _set_storage_bucket_tracking_impl(self, storage_key: str, enable: bool) -> None:
		return self._execute_function(
				"Storage.setStorageBucketTracking",
				{"storage_key": storage_key, "enable": enable}
		)
	
	def _track_cache_storage_for_origin_impl(self, origin: str) -> None:
		return self._execute_function("Storage.trackCacheStorageForOrigin", {"origin": origin})
	
	def _track_cache_storage_for_storage_key_impl(self, storage_key: str) -> None:
		return self._execute_function("Storage.trackCacheStorageForStorageKey", {"storage_key": storage_key})
	
	def _track_indexed_db_for_origin_impl(self, origin: str) -> None:
		return self._execute_function("Storage.trackIndexedDBForOrigin", {"origin": origin})
	
	def _track_indexed_db_for_storage_key_impl(self, storage_key: str) -> None:
		return self._execute_function("Storage.trackIndexedDBForStorageKey", {"storage_key": storage_key})
	
	def _untrack_cache_storage_for_origin_impl(self, origin: str) -> None:
		return self._execute_function("Storage.untrackCacheStorageForOrigin", {"origin": origin})
	
	def _untrack_cache_storage_for_storage_key_impl(self, storage_key: str) -> None:
		return self._execute_function("Storage.untrackCacheStorageForStorageKey", {"storage_key": storage_key})
	
	def _untrack_indexed_db_for_origin_impl(self, origin: str) -> None:
		return self._execute_function("Storage.untrackIndexedDBForOrigin", {"origin": origin})
	
	def _untrack_indexed_db_for_storage_key_impl(self, storage_key: str) -> None:
		return self._execute_function("Storage.untrackIndexedDBForStorageKey", {"storage_key": storage_key})
