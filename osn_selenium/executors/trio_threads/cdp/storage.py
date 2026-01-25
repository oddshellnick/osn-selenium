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
from osn_selenium.executors.unified.cdp.storage import (
	UnifiedStorageCDPExecutor
)
from osn_selenium.abstract.executors.cdp.storage import (
	AbstractStorageCDPExecutor
)


__all__ = ["StorageCDPExecutor"]


class StorageCDPExecutor(UnifiedStorageCDPExecutor, TrioThreadMixin, AbstractStorageCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedStorageCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def clear_cookies(self, browser_context_id: Optional[str] = None) -> None:
		return await self.sync_to_trio(sync_function=self._clear_cookies_impl)(browser_context_id=browser_context_id)
	
	async def clear_data_for_origin(self, origin: str, storage_types: str) -> None:
		return await self.sync_to_trio(sync_function=self._clear_data_for_origin_impl)(origin=origin, storage_types=storage_types)
	
	async def clear_data_for_storage_key(self, storage_key: str, storage_types: str) -> None:
		return await self.sync_to_trio(sync_function=self._clear_data_for_storage_key_impl)(storage_key=storage_key, storage_types=storage_types)
	
	async def clear_shared_storage_entries(self, owner_origin: str) -> None:
		return await self.sync_to_trio(sync_function=self._clear_shared_storage_entries_impl)(owner_origin=owner_origin)
	
	async def clear_trust_tokens(self, issuer_origin: str) -> bool:
		return await self.sync_to_trio(sync_function=self._clear_trust_tokens_impl)(issuer_origin=issuer_origin)
	
	async def delete_shared_storage_entry(self, owner_origin: str, key: str) -> None:
		return await self.sync_to_trio(sync_function=self._delete_shared_storage_entry_impl)(owner_origin=owner_origin, key=key)
	
	async def delete_storage_bucket(self, bucket: Dict[str, Any]) -> None:
		return await self.sync_to_trio(sync_function=self._delete_storage_bucket_impl)(bucket=bucket)
	
	async def get_affected_urls_for_third_party_cookie_metadata(self, first_party_url: str, third_party_urls: List[str]) -> List[str]:
		return await self.sync_to_trio(
				sync_function=self._get_affected_urls_for_third_party_cookie_metadata_impl
		)(first_party_url=first_party_url, third_party_urls=third_party_urls)
	
	async def get_cookies(self, browser_context_id: Optional[str] = None) -> List[Dict[str, Any]]:
		return await self.sync_to_trio(sync_function=self._get_cookies_impl)(browser_context_id=browser_context_id)
	
	async def get_interest_group_details(self, owner_origin: str, name: str) -> Any:
		return await self.sync_to_trio(sync_function=self._get_interest_group_details_impl)(owner_origin=owner_origin, name=name)
	
	async def get_related_website_sets(self) -> List[Dict[str, Any]]:
		return await self.sync_to_trio(sync_function=self._get_related_website_sets_impl)()
	
	async def get_shared_storage_entries(self, owner_origin: str) -> List[Dict[str, Any]]:
		return await self.sync_to_trio(sync_function=self._get_shared_storage_entries_impl)(owner_origin=owner_origin)
	
	async def get_shared_storage_metadata(self, owner_origin: str) -> Dict[str, Any]:
		return await self.sync_to_trio(sync_function=self._get_shared_storage_metadata_impl)(owner_origin=owner_origin)
	
	async def get_storage_key(self, frame_id: Optional[str] = None) -> str:
		return await self.sync_to_trio(sync_function=self._get_storage_key_impl)(frame_id=frame_id)
	
	async def get_storage_key_for_frame(self, frame_id: str) -> str:
		return await self.sync_to_trio(sync_function=self._get_storage_key_for_frame_impl)(frame_id=frame_id)
	
	async def get_trust_tokens(self) -> List[Dict[str, Any]]:
		return await self.sync_to_trio(sync_function=self._get_trust_tokens_impl)()
	
	async def get_usage_and_quota(self, origin: str) -> Tuple[float, float, bool, List[Dict[str, Any]]]:
		return await self.sync_to_trio(sync_function=self._get_usage_and_quota_impl)(origin=origin)
	
	async def override_quota_for_origin(self, origin: str, quota_size: Optional[float] = None) -> None:
		return await self.sync_to_trio(sync_function=self._override_quota_for_origin_impl)(origin=origin, quota_size=quota_size)
	
	async def reset_shared_storage_budget(self, owner_origin: str) -> None:
		return await self.sync_to_trio(sync_function=self._reset_shared_storage_budget_impl)(owner_origin=owner_origin)
	
	async def run_bounce_tracking_mitigations(self) -> List[str]:
		return await self.sync_to_trio(sync_function=self._run_bounce_tracking_mitigations_impl)()
	
	async def send_pending_attribution_reports(self) -> int:
		return await self.sync_to_trio(sync_function=self._send_pending_attribution_reports_impl)()
	
	async def set_attribution_reporting_local_testing_mode(self, enabled: bool) -> None:
		return await self.sync_to_trio(sync_function=self._set_attribution_reporting_local_testing_mode_impl)(enabled=enabled)
	
	async def set_attribution_reporting_tracking(self, enable: bool) -> None:
		return await self.sync_to_trio(sync_function=self._set_attribution_reporting_tracking_impl)(enable=enable)
	
	async def set_cookies(
			self,
			cookies: List[Dict[str, Any]],
			browser_context_id: Optional[str] = None
	) -> None:
		return await self.sync_to_trio(sync_function=self._set_cookies_impl)(cookies=cookies, browser_context_id=browser_context_id)
	
	async def set_interest_group_auction_tracking(self, enable: bool) -> None:
		return await self.sync_to_trio(sync_function=self._set_interest_group_auction_tracking_impl)(enable=enable)
	
	async def set_interest_group_tracking(self, enable: bool) -> None:
		return await self.sync_to_trio(sync_function=self._set_interest_group_tracking_impl)(enable=enable)
	
	async def set_protected_audience_k_anonymity(self, owner: str, name: str, hashes: List[str]) -> None:
		return await self.sync_to_trio(sync_function=self._set_protected_audience_k_anonymity_impl)(owner=owner, name=name, hashes=hashes)
	
	async def set_shared_storage_entry(
			self,
			owner_origin: str,
			key: str,
			value: str,
			ignore_if_present: Optional[bool] = None
	) -> None:
		return await self.sync_to_trio(sync_function=self._set_shared_storage_entry_impl)(
				owner_origin=owner_origin,
				key=key,
				value=value,
				ignore_if_present=ignore_if_present
		)
	
	async def set_shared_storage_tracking(self, enable: bool) -> None:
		return await self.sync_to_trio(sync_function=self._set_shared_storage_tracking_impl)(enable=enable)
	
	async def set_storage_bucket_tracking(self, storage_key: str, enable: bool) -> None:
		return await self.sync_to_trio(sync_function=self._set_storage_bucket_tracking_impl)(storage_key=storage_key, enable=enable)
	
	async def track_cache_storage_for_origin(self, origin: str) -> None:
		return await self.sync_to_trio(sync_function=self._track_cache_storage_for_origin_impl)(origin=origin)
	
	async def track_cache_storage_for_storage_key(self, storage_key: str) -> None:
		return await self.sync_to_trio(sync_function=self._track_cache_storage_for_storage_key_impl)(storage_key=storage_key)
	
	async def track_indexed_db_for_origin(self, origin: str) -> None:
		return await self.sync_to_trio(sync_function=self._track_indexed_db_for_origin_impl)(origin=origin)
	
	async def track_indexed_db_for_storage_key(self, storage_key: str) -> None:
		return await self.sync_to_trio(sync_function=self._track_indexed_db_for_storage_key_impl)(storage_key=storage_key)
	
	async def untrack_cache_storage_for_origin(self, origin: str) -> None:
		return await self.sync_to_trio(sync_function=self._untrack_cache_storage_for_origin_impl)(origin=origin)
	
	async def untrack_cache_storage_for_storage_key(self, storage_key: str) -> None:
		return await self.sync_to_trio(sync_function=self._untrack_cache_storage_for_storage_key_impl)(storage_key=storage_key)
	
	async def untrack_indexed_db_for_origin(self, origin: str) -> None:
		return await self.sync_to_trio(sync_function=self._untrack_indexed_db_for_origin_impl)(origin=origin)
	
	async def untrack_indexed_db_for_storage_key(self, storage_key: str) -> None:
		return await self.sync_to_trio(sync_function=self._untrack_indexed_db_for_storage_key_impl)(storage_key=storage_key)
