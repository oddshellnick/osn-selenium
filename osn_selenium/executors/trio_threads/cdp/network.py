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
from osn_selenium.executors.unified.cdp.network import (
	UnifiedNetworkCDPExecutor
)
from osn_selenium.abstract.executors.cdp.network import (
	AbstractNetworkCDPExecutor
)


__all__ = ["NetworkCDPExecutor"]


class NetworkCDPExecutor(UnifiedNetworkCDPExecutor, TrioThreadMixin, AbstractNetworkCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedNetworkCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def can_clear_browser_cache(self) -> bool:
		return await self.sync_to_trio(sync_function=self._can_clear_browser_cache_impl)()
	
	async def can_clear_browser_cookies(self) -> bool:
		return await self.sync_to_trio(sync_function=self._can_clear_browser_cookies_impl)()
	
	async def can_emulate_network_conditions(self) -> bool:
		return await self.sync_to_trio(sync_function=self._can_emulate_network_conditions_impl)()
	
	async def clear_accepted_encodings_override(self) -> None:
		return await self.sync_to_trio(sync_function=self._clear_accepted_encodings_override_impl)()
	
	async def clear_browser_cache(self) -> None:
		return await self.sync_to_trio(sync_function=self._clear_browser_cache_impl)()
	
	async def clear_browser_cookies(self) -> None:
		return await self.sync_to_trio(sync_function=self._clear_browser_cookies_impl)()
	
	async def continue_intercepted_request(
			self,
			interception_id: str,
			error_reason: Optional[str] = None,
			raw_response: Optional[str] = None,
			url: Optional[str] = None,
			method: Optional[str] = None,
			post_data: Optional[str] = None,
			headers: Optional[Dict[Any, Any]] = None,
			auth_challenge_response: Optional[Dict[str, Any]] = None
	) -> None:
		return await self.sync_to_trio(sync_function=self._continue_intercepted_request_impl)(
				interception_id=interception_id,
				error_reason=error_reason,
				raw_response=raw_response,
				url=url,
				method=method,
				post_data=post_data,
				headers=headers,
				auth_challenge_response=auth_challenge_response
		)
	
	async def delete_cookies(
			self,
			name: str,
			url: Optional[str] = None,
			domain: Optional[str] = None,
			path: Optional[str] = None,
			partition_key: Optional[Dict[str, Any]] = None
	) -> None:
		return await self.sync_to_trio(sync_function=self._delete_cookies_impl)(
				name=name,
				url=url,
				domain=domain,
				path=path,
				partition_key=partition_key
		)
	
	async def disable(self) -> None:
		return await self.sync_to_trio(sync_function=self._disable_impl)()
	
	async def emulate_network_conditions(
			self,
			offline: bool,
			latency: float,
			download_throughput: float,
			upload_throughput: float,
			connection_type: Optional[str] = None,
			packet_loss: Optional[float] = None,
			packet_queue_length: Optional[int] = None,
			packet_reordering: Optional[bool] = None
	) -> None:
		return await self.sync_to_trio(sync_function=self._emulate_network_conditions_impl)(
				offline=offline,
				latency=latency,
				download_throughput=download_throughput,
				upload_throughput=upload_throughput,
				connection_type=connection_type,
				packet_loss=packet_loss,
				packet_queue_length=packet_queue_length,
				packet_reordering=packet_reordering
		)
	
	async def emulate_network_conditions_by_rule(self, offline: bool, matched_network_conditions: List[Dict[str, Any]]) -> List[str]:
		return await self.sync_to_trio(sync_function=self._emulate_network_conditions_by_rule_impl)(offline=offline, matched_network_conditions=matched_network_conditions)
	
	async def enable(
			self,
			max_total_buffer_size: Optional[int] = None,
			max_resource_buffer_size: Optional[int] = None,
			max_post_data_size: Optional[int] = None,
			report_direct_socket_traffic: Optional[bool] = None,
			enable_durable_messages: Optional[bool] = None
	) -> None:
		return await self.sync_to_trio(sync_function=self._enable_impl)(
				max_total_buffer_size=max_total_buffer_size,
				max_resource_buffer_size=max_resource_buffer_size,
				max_post_data_size=max_post_data_size,
				report_direct_socket_traffic=report_direct_socket_traffic,
				enable_durable_messages=enable_durable_messages
		)
	
	async def enable_reporting_api(self, enable: bool) -> None:
		return await self.sync_to_trio(sync_function=self._enable_reporting_api_impl)(enable=enable)
	
	async def get_all_cookies(self) -> List[Dict[str, Any]]:
		return await self.sync_to_trio(sync_function=self._get_all_cookies_impl)()
	
	async def get_certificate(self, origin: str) -> List[str]:
		return await self.sync_to_trio(sync_function=self._get_certificate_impl)(origin=origin)
	
	async def get_cookies(self, urls: Optional[List[str]] = None) -> List[Dict[str, Any]]:
		return await self.sync_to_trio(sync_function=self._get_cookies_impl)(urls=urls)
	
	async def get_ip_protection_proxy_status(self) -> str:
		return await self.sync_to_trio(sync_function=self._get_ip_protection_proxy_status_impl)()
	
	async def get_request_post_data(self, request_id: str) -> str:
		return await self.sync_to_trio(sync_function=self._get_request_post_data_impl)(request_id=request_id)
	
	async def get_response_body(self, request_id: str) -> Tuple[str, bool]:
		return await self.sync_to_trio(sync_function=self._get_response_body_impl)(request_id=request_id)
	
	async def get_response_body_for_interception(self, interception_id: str) -> Tuple[str, bool]:
		return await self.sync_to_trio(sync_function=self._get_response_body_for_interception_impl)(interception_id=interception_id)
	
	async def get_security_isolation_status(self, frame_id: Optional[str] = None) -> Dict[str, Any]:
		return await self.sync_to_trio(sync_function=self._get_security_isolation_status_impl)(frame_id=frame_id)
	
	async def load_network_resource(
			self,
			frame_id: Optional[str] = None,
			url: str = None,
			options: Dict[str, Any] = None
	) -> Dict[str, Any]:
		return await self.sync_to_trio(sync_function=self._load_network_resource_impl)(frame_id=frame_id, url=url, options=options)
	
	async def override_network_state(
			self,
			offline: bool,
			latency: float,
			download_throughput: float,
			upload_throughput: float,
			connection_type: Optional[str] = None
	) -> None:
		return await self.sync_to_trio(sync_function=self._override_network_state_impl)(
				offline=offline,
				latency=latency,
				download_throughput=download_throughput,
				upload_throughput=upload_throughput,
				connection_type=connection_type
		)
	
	async def replay_xhr(self, request_id: str) -> None:
		return await self.sync_to_trio(sync_function=self._replay_xhr_impl)(request_id=request_id)
	
	async def search_in_response_body(
			self,
			request_id: str,
			query: str,
			case_sensitive: Optional[bool] = None,
			is_regex: Optional[bool] = None
	) -> List[Dict[str, Any]]:
		return await self.sync_to_trio(sync_function=self._search_in_response_body_impl)(
				request_id=request_id,
				query=query,
				case_sensitive=case_sensitive,
				is_regex=is_regex
		)
	
	async def set_accepted_encodings(self, encodings: List[str]) -> None:
		return await self.sync_to_trio(sync_function=self._set_accepted_encodings_impl)(encodings=encodings)
	
	async def set_attach_debug_stack(self, enabled: bool) -> None:
		return await self.sync_to_trio(sync_function=self._set_attach_debug_stack_impl)(enabled=enabled)
	
	async def set_blocked_ur_ls(
			self,
			url_patterns: Optional[List[Dict[str, Any]]] = None,
			urls: Optional[List[str]] = None
	) -> None:
		return await self.sync_to_trio(sync_function=self._set_blocked_ur_ls_impl)(url_patterns=url_patterns, urls=urls)
	
	async def set_bypass_service_worker(self, bypass: bool) -> None:
		return await self.sync_to_trio(sync_function=self._set_bypass_service_worker_impl)(bypass=bypass)
	
	async def set_cache_disabled(self, cache_disabled: bool) -> None:
		return await self.sync_to_trio(sync_function=self._set_cache_disabled_impl)(cache_disabled=cache_disabled)
	
	async def set_cookie(
			self,
			name: str,
			value: str,
			url: Optional[str] = None,
			domain: Optional[str] = None,
			path: Optional[str] = None,
			secure: Optional[bool] = None,
			http_only: Optional[bool] = None,
			same_site: Optional[str] = None,
			expires: Optional[float] = None,
			priority: Optional[str] = None,
			same_party: Optional[bool] = None,
			source_scheme: Optional[str] = None,
			source_port: Optional[int] = None,
			partition_key: Optional[Dict[str, Any]] = None
	) -> bool:
		return await self.sync_to_trio(sync_function=self._set_cookie_impl)(
				name=name,
				value=value,
				url=url,
				domain=domain,
				path=path,
				secure=secure,
				http_only=http_only,
				same_site=same_site,
				expires=expires,
				priority=priority,
				same_party=same_party,
				source_scheme=source_scheme,
				source_port=source_port,
				partition_key=partition_key
		)
	
	async def set_cookie_controls(
			self,
			enable_third_party_cookie_restriction: bool,
			disable_third_party_cookie_metadata: bool,
			disable_third_party_cookie_heuristics: bool
	) -> None:
		return await self.sync_to_trio(sync_function=self._set_cookie_controls_impl)(
				enable_third_party_cookie_restriction=enable_third_party_cookie_restriction,
				disable_third_party_cookie_metadata=disable_third_party_cookie_metadata,
				disable_third_party_cookie_heuristics=disable_third_party_cookie_heuristics
		)
	
	async def set_cookies(self, cookies: List[Dict[str, Any]]) -> None:
		return await self.sync_to_trio(sync_function=self._set_cookies_impl)(cookies=cookies)
	
	async def set_extra_http_headers(self, headers: Dict[Any, Any]) -> None:
		return await self.sync_to_trio(sync_function=self._set_extra_http_headers_impl)(headers=headers)
	
	async def set_ip_protection_proxy_bypass_enabled(self, enabled: bool) -> None:
		return await self.sync_to_trio(sync_function=self._set_ip_protection_proxy_bypass_enabled_impl)(enabled=enabled)
	
	async def set_request_interception(self, patterns: List[Dict[str, Any]]) -> None:
		return await self.sync_to_trio(sync_function=self._set_request_interception_impl)(patterns=patterns)
	
	async def set_user_agent_override(
			self,
			user_agent: str,
			accept_language: Optional[str] = None,
			platform: Optional[str] = None,
			user_agent_metadata: Optional[Dict[str, Any]] = None
	) -> None:
		return await self.sync_to_trio(sync_function=self._set_user_agent_override_impl)(
				user_agent=user_agent,
				accept_language=accept_language,
				platform=platform,
				user_agent_metadata=user_agent_metadata
		)
	
	async def stream_resource_content(self, request_id: str) -> str:
		return await self.sync_to_trio(sync_function=self._stream_resource_content_impl)(request_id=request_id)
	
	async def take_response_body_for_interception_as_stream(self, interception_id: str) -> str:
		return await self.sync_to_trio(sync_function=self._take_response_body_for_interception_as_stream_impl)(interception_id=interception_id)
