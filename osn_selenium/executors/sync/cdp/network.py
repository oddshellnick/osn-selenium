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


class NetworkCDPExecutor(UnifiedNetworkCDPExecutor, AbstractNetworkCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedNetworkCDPExecutor.__init__(self, execute_function=execute_function)
	
	def can_clear_browser_cache(self) -> bool:
		return self._can_clear_browser_cache_impl()
	
	def can_clear_browser_cookies(self) -> bool:
		return self._can_clear_browser_cookies_impl()
	
	def can_emulate_network_conditions(self) -> bool:
		return self._can_emulate_network_conditions_impl()
	
	def clear_accepted_encodings_override(self) -> None:
		return self._clear_accepted_encodings_override_impl()
	
	def clear_browser_cache(self) -> None:
		return self._clear_browser_cache_impl()
	
	def clear_browser_cookies(self) -> None:
		return self._clear_browser_cookies_impl()
	
	def continue_intercepted_request(
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
		return self._continue_intercepted_request_impl(
				interception_id=interception_id,
				error_reason=error_reason,
				raw_response=raw_response,
				url=url,
				method=method,
				post_data=post_data,
				headers=headers,
				auth_challenge_response=auth_challenge_response
		)
	
	def delete_cookies(
			self,
			name: str,
			url: Optional[str] = None,
			domain: Optional[str] = None,
			path: Optional[str] = None,
			partition_key: Optional[Dict[str, Any]] = None
	) -> None:
		return self._delete_cookies_impl(
				name=name,
				url=url,
				domain=domain,
				path=path,
				partition_key=partition_key
		)
	
	def disable(self) -> None:
		return self._disable_impl()
	
	def emulate_network_conditions(
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
		return self._emulate_network_conditions_impl(
				offline=offline,
				latency=latency,
				download_throughput=download_throughput,
				upload_throughput=upload_throughput,
				connection_type=connection_type,
				packet_loss=packet_loss,
				packet_queue_length=packet_queue_length,
				packet_reordering=packet_reordering
		)
	
	def emulate_network_conditions_by_rule(self, offline: bool, matched_network_conditions: List[Dict[str, Any]]) -> List[str]:
		return self._emulate_network_conditions_by_rule_impl(offline=offline, matched_network_conditions=matched_network_conditions)
	
	def enable(
			self,
			max_total_buffer_size: Optional[int] = None,
			max_resource_buffer_size: Optional[int] = None,
			max_post_data_size: Optional[int] = None,
			report_direct_socket_traffic: Optional[bool] = None,
			enable_durable_messages: Optional[bool] = None
	) -> None:
		return self._enable_impl(
				max_total_buffer_size=max_total_buffer_size,
				max_resource_buffer_size=max_resource_buffer_size,
				max_post_data_size=max_post_data_size,
				report_direct_socket_traffic=report_direct_socket_traffic,
				enable_durable_messages=enable_durable_messages
		)
	
	def enable_reporting_api(self, enable: bool) -> None:
		return self._enable_reporting_api_impl(enable=enable)
	
	def get_all_cookies(self) -> List[Dict[str, Any]]:
		return self._get_all_cookies_impl()
	
	def get_certificate(self, origin: str) -> List[str]:
		return self._get_certificate_impl(origin=origin)
	
	def get_cookies(self, urls: Optional[List[str]] = None) -> List[Dict[str, Any]]:
		return self._get_cookies_impl(urls=urls)
	
	def get_ip_protection_proxy_status(self) -> str:
		return self._get_ip_protection_proxy_status_impl()
	
	def get_request_post_data(self, request_id: str) -> str:
		return self._get_request_post_data_impl(request_id=request_id)
	
	def get_response_body(self, request_id: str) -> Tuple[str, bool]:
		return self._get_response_body_impl(request_id=request_id)
	
	def get_response_body_for_interception(self, interception_id: str) -> Tuple[str, bool]:
		return self._get_response_body_for_interception_impl(interception_id=interception_id)
	
	def get_security_isolation_status(self, frame_id: Optional[str] = None) -> Dict[str, Any]:
		return self._get_security_isolation_status_impl(frame_id=frame_id)
	
	def load_network_resource(
			self,
			frame_id: Optional[str] = None,
			url: str = None,
			options: Dict[str, Any] = None
	) -> Dict[str, Any]:
		return self._load_network_resource_impl(frame_id=frame_id, url=url, options=options)
	
	def override_network_state(
			self,
			offline: bool,
			latency: float,
			download_throughput: float,
			upload_throughput: float,
			connection_type: Optional[str] = None
	) -> None:
		return self._override_network_state_impl(
				offline=offline,
				latency=latency,
				download_throughput=download_throughput,
				upload_throughput=upload_throughput,
				connection_type=connection_type
		)
	
	def replay_xhr(self, request_id: str) -> None:
		return self._replay_xhr_impl(request_id=request_id)
	
	def search_in_response_body(
			self,
			request_id: str,
			query: str,
			case_sensitive: Optional[bool] = None,
			is_regex: Optional[bool] = None
	) -> List[Dict[str, Any]]:
		return self._search_in_response_body_impl(
				request_id=request_id,
				query=query,
				case_sensitive=case_sensitive,
				is_regex=is_regex
		)
	
	def set_accepted_encodings(self, encodings: List[str]) -> None:
		return self._set_accepted_encodings_impl(encodings=encodings)
	
	def set_attach_debug_stack(self, enabled: bool) -> None:
		return self._set_attach_debug_stack_impl(enabled=enabled)
	
	def set_blocked_ur_ls(
			self,
			url_patterns: Optional[List[Dict[str, Any]]] = None,
			urls: Optional[List[str]] = None
	) -> None:
		return self._set_blocked_ur_ls_impl(url_patterns=url_patterns, urls=urls)
	
	def set_bypass_service_worker(self, bypass: bool) -> None:
		return self._set_bypass_service_worker_impl(bypass=bypass)
	
	def set_cache_disabled(self, cache_disabled: bool) -> None:
		return self._set_cache_disabled_impl(cache_disabled=cache_disabled)
	
	def set_cookie(
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
		return self._set_cookie_impl(
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
	
	def set_cookie_controls(
			self,
			enable_third_party_cookie_restriction: bool,
			disable_third_party_cookie_metadata: bool,
			disable_third_party_cookie_heuristics: bool
	) -> None:
		return self._set_cookie_controls_impl(
				enable_third_party_cookie_restriction=enable_third_party_cookie_restriction,
				disable_third_party_cookie_metadata=disable_third_party_cookie_metadata,
				disable_third_party_cookie_heuristics=disable_third_party_cookie_heuristics
		)
	
	def set_cookies(self, cookies: List[Dict[str, Any]]) -> None:
		return self._set_cookies_impl(cookies=cookies)
	
	def set_extra_http_headers(self, headers: Dict[Any, Any]) -> None:
		return self._set_extra_http_headers_impl(headers=headers)
	
	def set_ip_protection_proxy_bypass_enabled(self, enabled: bool) -> None:
		return self._set_ip_protection_proxy_bypass_enabled_impl(enabled=enabled)
	
	def set_request_interception(self, patterns: List[Dict[str, Any]]) -> None:
		return self._set_request_interception_impl(patterns=patterns)
	
	def set_user_agent_override(
			self,
			user_agent: str,
			accept_language: Optional[str] = None,
			platform: Optional[str] = None,
			user_agent_metadata: Optional[Dict[str, Any]] = None
	) -> None:
		return self._set_user_agent_override_impl(
				user_agent=user_agent,
				accept_language=accept_language,
				platform=platform,
				user_agent_metadata=user_agent_metadata
		)
	
	def stream_resource_content(self, request_id: str) -> str:
		return self._stream_resource_content_impl(request_id=request_id)
	
	def take_response_body_for_interception_as_stream(self, interception_id: str) -> str:
		return self._take_response_body_for_interception_as_stream_impl(interception_id=interception_id)
