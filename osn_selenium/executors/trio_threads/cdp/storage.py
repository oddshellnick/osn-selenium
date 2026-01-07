from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.abstract.executors.cdp.storage import (
	AbstractStorageCDPExecutor
)


class StorageCDPExecutor(AbstractStorageCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def clear_cookies(self, browser_context_id: Optional[str] = None) -> None:
		return await self._execute_function("Storage.clearCookies", locals())
	
	async def clear_data_for_origin(self, origin: str, storage_types: str) -> None:
		return await self._execute_function("Storage.clearDataForOrigin", locals())
	
	async def clear_data_for_storage_key(self, storage_key: str, storage_types: str) -> None:
		return await self._execute_function("Storage.clearDataForStorageKey", locals())
	
	async def clear_shared_storage_entries(self, owner_origin: str) -> None:
		return await self._execute_function("Storage.clearSharedStorageEntries", locals())
	
	async def clear_trust_tokens(self, issuer_origin: str) -> bool:
		return await self._execute_function("Storage.clearTrustTokens", locals())
	
	async def delete_shared_storage_entry(self, owner_origin: str, key: str) -> None:
		return await self._execute_function("Storage.deleteSharedStorageEntry", locals())
	
	async def delete_storage_bucket(self, bucket: Any) -> None:
		return await self._execute_function("Storage.deleteStorageBucket", locals())
	
	async def get_affected_urls_for_third_party_cookie_metadata(self, first_party_url: str, third_party_urls: List[str]) -> List[str]:
		return await self._execute_function("Storage.getAffectedUrlsForThirdPartyCookieMetadata", locals())
	
	async def get_cookies(self, browser_context_id: Optional[str] = None) -> List[Any]:
		return await self._execute_function("Storage.getCookies", locals())
	
	async def get_interest_group_details(self, owner_origin: str, name: str) -> dict:
		return await self._execute_function("Storage.getInterestGroupDetails", locals())
	
	async def get_related_website_sets(self) -> List[Any]:
		return await self._execute_function("Storage.getRelatedWebsiteSets", locals())
	
	async def get_shared_storage_entries(self, owner_origin: str) -> List[Any]:
		return await self._execute_function("Storage.getSharedStorageEntries", locals())
	
	async def get_shared_storage_metadata(self, owner_origin: str) -> Any:
		return await self._execute_function("Storage.getSharedStorageMetadata", locals())
	
	async def get_storage_key(self, frame_id: Optional[str] = None) -> str:
		return await self._execute_function("Storage.getStorageKey", locals())
	
	async def get_storage_key_for_frame(self, frame_id: str) -> str:
		return await self._execute_function("Storage.getStorageKeyForFrame", locals())
	
	async def get_trust_tokens(self) -> List[Any]:
		return await self._execute_function("Storage.getTrustTokens", locals())
	
	async def get_usage_and_quota(self, origin: str) -> Tuple[float, float, bool, List[Any]]:
		return await self._execute_function("Storage.getUsageAndQuota", locals())
	
	async def override_quota_for_origin(self, origin: str, quota_size: Optional[float] = None) -> None:
		return await self._execute_function("Storage.overrideQuotaForOrigin", locals())
	
	async def reset_shared_storage_budget(self, owner_origin: str) -> None:
		return await self._execute_function("Storage.resetSharedStorageBudget", locals())
	
	async def run_bounce_tracking_mitigations(self) -> List[str]:
		return await self._execute_function("Storage.runBounceTrackingMitigations", locals())
	
	async def send_pending_attribution_reports(self) -> int:
		return await self._execute_function("Storage.sendPendingAttributionReports", locals())
	
	async def set_attribution_reporting_local_testing_mode(self, enabled: bool) -> None:
		return await self._execute_function("Storage.setAttributionReportingLocalTestingMode", locals())
	
	async def set_attribution_reporting_tracking(self, enable: bool) -> None:
		return await self._execute_function("Storage.setAttributionReportingTracking", locals())
	
	async def set_cookies(self, cookies: List[Any], browser_context_id: Optional[str] = None) -> None:
		return await self._execute_function("Storage.setCookies", locals())
	
	async def set_interest_group_auction_tracking(self, enable: bool) -> None:
		return await self._execute_function("Storage.setInterestGroupAuctionTracking", locals())
	
	async def set_interest_group_tracking(self, enable: bool) -> None:
		return await self._execute_function("Storage.setInterestGroupTracking", locals())
	
	async def set_protected_audience_k_anonymity(self, owner: str, name: str, hashes: List[str]) -> None:
		return await self._execute_function("Storage.setProtectedAudienceKAnonymity", locals())
	
	async def set_shared_storage_entry(
			self,
			owner_origin: str,
			key: str,
			value: str,
			ignore_if_present: Optional[bool] = None
	) -> None:
		return await self._execute_function("Storage.setSharedStorageEntry", locals())
	
	async def set_shared_storage_tracking(self, enable: bool) -> None:
		return await self._execute_function("Storage.setSharedStorageTracking", locals())
	
	async def set_storage_bucket_tracking(self, storage_key: str, enable: bool) -> None:
		return await self._execute_function("Storage.setStorageBucketTracking", locals())
	
	async def track_cache_storage_for_origin(self, origin: str) -> None:
		return await self._execute_function("Storage.trackCacheStorageForOrigin", locals())
	
	async def track_cache_storage_for_storage_key(self, storage_key: str) -> None:
		return await self._execute_function("Storage.trackCacheStorageForStorageKey", locals())
	
	async def track_indexed_db_for_origin(self, origin: str) -> None:
		return await self._execute_function("Storage.trackIndexedDBForOrigin", locals())
	
	async def track_indexed_db_for_storage_key(self, storage_key: str) -> None:
		return await self._execute_function("Storage.trackIndexedDBForStorageKey", locals())
	
	async def untrack_cache_storage_for_origin(self, origin: str) -> None:
		return await self._execute_function("Storage.untrackCacheStorageForOrigin", locals())
	
	async def untrack_cache_storage_for_storage_key(self, storage_key: str) -> None:
		return await self._execute_function("Storage.untrackCacheStorageForStorageKey", locals())
	
	async def untrack_indexed_db_for_origin(self, origin: str) -> None:
		return await self._execute_function("Storage.untrackIndexedDBForOrigin", locals())
	
	async def untrack_indexed_db_for_storage_key(self, storage_key: str) -> None:
		return await self._execute_function("Storage.untrackIndexedDBForStorageKey", locals())
