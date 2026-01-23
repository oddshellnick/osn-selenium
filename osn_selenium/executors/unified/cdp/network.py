from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)


__all__ = ["UnifiedNetworkCDPExecutor"]


class UnifiedNetworkCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _can_clear_browser_cache_impl(self) -> bool:
		return self._execute_function("Network.canClearBrowserCache", {})
	
	def _can_clear_browser_cookies_impl(self) -> bool:
		return self._execute_function("Network.canClearBrowserCookies", {})
	
	def _can_emulate_network_conditions_impl(self) -> bool:
		return self._execute_function("Network.canEmulateNetworkConditions", {})
	
	def _clear_accepted_encodings_override_impl(self) -> None:
		return self._execute_function("Network.clearAcceptedEncodingsOverride", {})
	
	def _clear_browser_cache_impl(self) -> None:
		return self._execute_function("Network.clearBrowserCache", {})
	
	def _clear_browser_cookies_impl(self) -> None:
		return self._execute_function("Network.clearBrowserCookies", {})
	
	def _continue_intercepted_request_impl(
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
		return self._execute_function(
				"Network.continueInterceptedRequest",
				{
					"interception_id": interception_id,
					"error_reason": error_reason,
					"raw_response": raw_response,
					"url": url,
					"method": method,
					"post_data": post_data,
					"headers": headers,
					"auth_challenge_response": auth_challenge_response
				}
		)
	
	def _delete_cookies_impl(
			self,
			name: str,
			url: Optional[str] = None,
			domain: Optional[str] = None,
			path: Optional[str] = None,
			partition_key: Optional[Dict[str, Any]] = None
	) -> None:
		return self._execute_function(
				"Network.deleteCookies",
				{
					"name": name,
					"url": url,
					"domain": domain,
					"path": path,
					"partition_key": partition_key
				}
		)
	
	def _disable_impl(self) -> None:
		return self._execute_function("Network.disable", {})
	
	def _emulate_network_conditions_by_rule_impl(self, offline: bool, matched_network_conditions: List[Dict[str, Any]]) -> List[str]:
		return self._execute_function(
				"Network.emulateNetworkConditionsByRule",
				{
					"offline": offline,
					"matched_network_conditions": matched_network_conditions
				}
		)
	
	def _emulate_network_conditions_impl(
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
		return self._execute_function(
				"Network.emulateNetworkConditions",
				{
					"offline": offline,
					"latency": latency,
					"download_throughput": download_throughput,
					"upload_throughput": upload_throughput,
					"connection_type": connection_type,
					"packet_loss": packet_loss,
					"packet_queue_length": packet_queue_length,
					"packet_reordering": packet_reordering
				}
		)
	
	def _enable_impl(
			self,
			max_total_buffer_size: Optional[int] = None,
			max_resource_buffer_size: Optional[int] = None,
			max_post_data_size: Optional[int] = None,
			report_direct_socket_traffic: Optional[bool] = None,
			enable_durable_messages: Optional[bool] = None
	) -> None:
		return self._execute_function(
				"Network.enable",
				{
					"max_total_buffer_size": max_total_buffer_size,
					"max_resource_buffer_size": max_resource_buffer_size,
					"max_post_data_size": max_post_data_size,
					"report_direct_socket_traffic": report_direct_socket_traffic,
					"enable_durable_messages": enable_durable_messages
				}
		)
	
	def _enable_reporting_api_impl(self, enable: bool) -> None:
		return self._execute_function("Network.enableReportingApi", {"enable": enable})
	
	def _get_all_cookies_impl(self) -> List[Dict[str, Any]]:
		return self._execute_function("Network.getAllCookies", {})
	
	def _get_certificate_impl(self, origin: str) -> List[str]:
		return self._execute_function("Network.getCertificate", {"origin": origin})
	
	def _get_cookies_impl(self, urls: Optional[List[str]] = None) -> List[Dict[str, Any]]:
		return self._execute_function("Network.getCookies", {"urls": urls})
	
	def _get_ip_protection_proxy_status_impl(self) -> str:
		return self._execute_function("Network.getIPProtectionProxyStatus", {})
	
	def _get_request_post_data_impl(self, request_id: str) -> str:
		return self._execute_function("Network.getRequestPostData", {"request_id": request_id})
	
	def _get_response_body_for_interception_impl(self, interception_id: str) -> Tuple[str, bool]:
		return self._execute_function(
				"Network.getResponseBodyForInterception",
				{"interception_id": interception_id}
		)
	
	def _get_response_body_impl(self, request_id: str) -> Tuple[str, bool]:
		return self._execute_function("Network.getResponseBody", {"request_id": request_id})
	
	def _get_security_isolation_status_impl(self, frame_id: Optional[str] = None) -> Dict[str, Any]:
		return self._execute_function("Network.getSecurityIsolationStatus", {"frame_id": frame_id})
	
	def _load_network_resource_impl(
			self,
			frame_id: Optional[str] = None,
			url: str = None,
			options: Dict[str, Any] = None
	) -> Dict[str, Any]:
		return self._execute_function(
				"Network.loadNetworkResource",
				{"frame_id": frame_id, "url": url, "options": options}
		)
	
	def _override_network_state_impl(
			self,
			offline: bool,
			latency: float,
			download_throughput: float,
			upload_throughput: float,
			connection_type: Optional[str] = None
	) -> None:
		return self._execute_function(
				"Network.overrideNetworkState",
				{
					"offline": offline,
					"latency": latency,
					"download_throughput": download_throughput,
					"upload_throughput": upload_throughput,
					"connection_type": connection_type
				}
		)
	
	def _replay_xhr_impl(self, request_id: str) -> None:
		return self._execute_function("Network.replayXHR", {"request_id": request_id})
	
	def _search_in_response_body_impl(
			self,
			request_id: str,
			query: str,
			case_sensitive: Optional[bool] = None,
			is_regex: Optional[bool] = None
	) -> List[Dict[str, Any]]:
		return self._execute_function(
				"Network.searchInResponseBody",
				{
					"request_id": request_id,
					"query": query,
					"case_sensitive": case_sensitive,
					"is_regex": is_regex
				}
		)
	
	def _set_accepted_encodings_impl(self, encodings: List[str]) -> None:
		return self._execute_function("Network.setAcceptedEncodings", {"encodings": encodings})
	
	def _set_attach_debug_stack_impl(self, enabled: bool) -> None:
		return self._execute_function("Network.setAttachDebugStack", {"enabled": enabled})
	
	def _set_blocked_ur_ls_impl(
			self,
			url_patterns: Optional[List[Dict[str, Any]]] = None,
			urls: Optional[List[str]] = None
	) -> None:
		return self._execute_function("Network.setBlockedURLs", {"url_patterns": url_patterns, "urls": urls})
	
	def _set_bypass_service_worker_impl(self, bypass: bool) -> None:
		return self._execute_function("Network.setBypassServiceWorker", {"bypass": bypass})
	
	def _set_cache_disabled_impl(self, cache_disabled: bool) -> None:
		return self._execute_function("Network.setCacheDisabled", {"cache_disabled": cache_disabled})
	
	def _set_cookie_controls_impl(
			self,
			enable_third_party_cookie_restriction: bool,
			disable_third_party_cookie_metadata: bool,
			disable_third_party_cookie_heuristics: bool
	) -> None:
		return self._execute_function(
				"Network.setCookieControls",
				{
					"enable_third_party_cookie_restriction": enable_third_party_cookie_restriction,
					"disable_third_party_cookie_metadata": disable_third_party_cookie_metadata,
					"disable_third_party_cookie_heuristics": disable_third_party_cookie_heuristics
				}
		)
	
	def _set_cookie_impl(
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
		return self._execute_function(
				"Network.setCookie",
				{
					"name": name,
					"value": value,
					"url": url,
					"domain": domain,
					"path": path,
					"secure": secure,
					"http_only": http_only,
					"same_site": same_site,
					"expires": expires,
					"priority": priority,
					"same_party": same_party,
					"source_scheme": source_scheme,
					"source_port": source_port,
					"partition_key": partition_key
				}
		)
	
	def _set_cookies_impl(self, cookies: List[Dict[str, Any]]) -> None:
		return self._execute_function("Network.setCookies", {"cookies": cookies})
	
	def _set_extra_http_headers_impl(self, headers: Dict[Any, Any]) -> None:
		return self._execute_function("Network.setExtraHTTPHeaders", {"headers": headers})
	
	def _set_ip_protection_proxy_bypass_enabled_impl(self, enabled: bool) -> None:
		return self._execute_function("Network.setIPProtectionProxyBypassEnabled", {"enabled": enabled})
	
	def _set_request_interception_impl(self, patterns: List[Dict[str, Any]]) -> None:
		return self._execute_function("Network.setRequestInterception", {"patterns": patterns})
	
	def _set_user_agent_override_impl(
			self,
			user_agent: str,
			accept_language: Optional[str] = None,
			platform: Optional[str] = None,
			user_agent_metadata: Optional[Dict[str, Any]] = None
	) -> None:
		return self._execute_function(
				"Network.setUserAgentOverride",
				{
					"user_agent": user_agent,
					"accept_language": accept_language,
					"platform": platform,
					"user_agent_metadata": user_agent_metadata
				}
		)
	
	def _stream_resource_content_impl(self, request_id: str) -> str:
		return self._execute_function("Network.streamResourceContent", {"request_id": request_id})
	
	def _take_response_body_for_interception_as_stream_impl(self, interception_id: str) -> str:
		return self._execute_function(
				"Network.takeResponseBodyForInterceptionAsStream",
				{"interception_id": interception_id}
		)
