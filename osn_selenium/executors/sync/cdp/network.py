from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.abstract.executors.cdp.network import (
	AbstractNetworkCDPExecutor
)


class NetworkCDPExecutor(AbstractNetworkCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def can_clear_browser_cache(self) -> bool:
		return self._execute_function("Network.canClearBrowserCache", locals())
	
	def can_clear_browser_cookies(self) -> bool:
		return self._execute_function("Network.canClearBrowserCookies", locals())
	
	def can_emulate_network_conditions(self) -> bool:
		return self._execute_function("Network.canEmulateNetworkConditions", locals())
	
	def clear_accepted_encodings_override(self) -> None:
		return self._execute_function("Network.clearAcceptedEncodingsOverride", locals())
	
	def clear_browser_cache(self) -> None:
		return self._execute_function("Network.clearBrowserCache", locals())
	
	def clear_browser_cookies(self) -> None:
		return self._execute_function("Network.clearBrowserCookies", locals())
	
	def continue_intercepted_request(
			self,
			interception_id: str,
			error_reason: Optional[str] = None,
			raw_response: Optional[str] = None,
			url: Optional[str] = None,
			method: Optional[str] = None,
			post_data: Optional[str] = None,
			headers: Optional[Dict[Any, Any]] = None,
			auth_challenge_response: Optional[Any] = None
	) -> None:
		return self._execute_function("Network.continueInterceptedRequest", locals())
	
	def delete_cookies(
			self,
			name: str,
			url: Optional[str] = None,
			domain: Optional[str] = None,
			path: Optional[str] = None,
			partition_key: Optional[Any] = None
	) -> None:
		return self._execute_function("Network.deleteCookies", locals())
	
	def disable(self) -> None:
		return self._execute_function("Network.disable", locals())
	
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
		return self._execute_function("Network.emulateNetworkConditions", locals())
	
	def emulate_network_conditions_by_rule(self, offline: bool, matched_network_conditions: List[Any]) -> List[str]:
		return self._execute_function("Network.emulateNetworkConditionsByRule", locals())
	
	def enable(
			self,
			max_total_buffer_size: Optional[int] = None,
			max_resource_buffer_size: Optional[int] = None,
			max_post_data_size: Optional[int] = None,
			report_direct_socket_traffic: Optional[bool] = None,
			enable_durable_messages: Optional[bool] = None
	) -> None:
		return self._execute_function("Network.enable", locals())
	
	def enable_reporting_api(self, enable: bool) -> None:
		return self._execute_function("Network.enableReportingApi", locals())
	
	def get_all_cookies(self) -> List[Any]:
		return self._execute_function("Network.getAllCookies", locals())
	
	def get_certificate(self, origin: str) -> List[str]:
		return self._execute_function("Network.getCertificate", locals())
	
	def get_cookies(self, urls: Optional[List[str]] = None) -> List[Any]:
		return self._execute_function("Network.getCookies", locals())
	
	def get_ip_protection_proxy_status(self) -> str:
		return self._execute_function("Network.getIPProtectionProxyStatus", locals())
	
	def get_request_post_data(self, request_id: str) -> str:
		return self._execute_function("Network.getRequestPostData", locals())
	
	def get_response_body(self, request_id: str) -> Tuple[str]:
		return self._execute_function("Network.getResponseBody", locals())
	
	def get_response_body_for_interception(self, interception_id: str) -> Tuple[str]:
		return self._execute_function("Network.getResponseBodyForInterception", locals())
	
	def get_security_isolation_status(self, frame_id: Optional[str] = None) -> Any:
		return self._execute_function("Network.getSecurityIsolationStatus", locals())
	
	def load_network_resource(
			self,
			frame_id: Optional[str] = None,
			url: str = None,
			options: Any = None
	) -> Any:
		return self._execute_function("Network.loadNetworkResource", locals())
	
	def override_network_state(
			self,
			offline: bool,
			latency: float,
			download_throughput: float,
			upload_throughput: float,
			connection_type: Optional[str] = None
	) -> None:
		return self._execute_function("Network.overrideNetworkState", locals())
	
	def replay_xhr(self, request_id: str) -> None:
		return self._execute_function("Network.replayXHR", locals())
	
	def search_in_response_body(
			self,
			request_id: str,
			query: str,
			case_sensitive: Optional[bool] = None,
			is_regex: Optional[bool] = None
	) -> List[Any]:
		return self._execute_function("Network.searchInResponseBody", locals())
	
	def set_accepted_encodings(self, encodings: List[str]) -> None:
		return self._execute_function("Network.setAcceptedEncodings", locals())
	
	def set_attach_debug_stack(self, enabled: bool) -> None:
		return self._execute_function("Network.setAttachDebugStack", locals())
	
	def set_blocked_ur_ls(
			self,
			url_patterns: Optional[List[Any]] = None,
			urls: Optional[List[str]] = None
	) -> None:
		return self._execute_function("Network.setBlockedURLs", locals())
	
	def set_bypass_service_worker(self, bypass: bool) -> None:
		return self._execute_function("Network.setBypassServiceWorker", locals())
	
	def set_cache_disabled(self, cache_disabled: bool) -> None:
		return self._execute_function("Network.setCacheDisabled", locals())
	
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
			partition_key: Optional[Any] = None
	) -> bool:
		return self._execute_function("Network.setCookie", locals())
	
	def set_cookie_controls(
			self,
			enable_third_party_cookie_restriction: bool,
			disable_third_party_cookie_metadata: bool,
			disable_third_party_cookie_heuristics: bool
	) -> None:
		return self._execute_function("Network.setCookieControls", locals())
	
	def set_cookies(self, cookies: List[Any]) -> None:
		return self._execute_function("Network.setCookies", locals())
	
	def set_extra_http_headers(self, headers: Dict[Any, Any]) -> None:
		return self._execute_function("Network.setExtraHTTPHeaders", locals())
	
	def set_ip_protection_proxy_bypass_enabled(self, enabled: bool) -> None:
		return self._execute_function("Network.setIPProtectionProxyBypassEnabled", locals())
	
	def set_request_interception(self, patterns: List[Any]) -> None:
		return self._execute_function("Network.setRequestInterception", locals())
	
	def set_user_agent_override(
			self,
			user_agent: str,
			accept_language: Optional[str] = None,
			platform: Optional[str] = None,
			user_agent_metadata: Optional[Any] = None
	) -> None:
		return self._execute_function("Network.setUserAgentOverride", locals())
	
	def stream_resource_content(self, request_id: str) -> str:
		return self._execute_function("Network.streamResourceContent", locals())
	
	def take_response_body_for_interception_as_stream(self, interception_id: str) -> str:
		return self._execute_function("Network.takeResponseBodyForInterceptionAsStream", locals())
