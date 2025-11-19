from abc import ABC, abstractmethod
from typing import (
	Any,
	Dict,
	List,
	Optional,
	Tuple
)


__all__ = ["AbstractNetworkCDPExecutor"]


class AbstractNetworkCDPExecutor(ABC):
	@abstractmethod
	def can_clear_browser_cache(self) -> bool:
		...
	
	@abstractmethod
	def can_clear_browser_cookies(self) -> bool:
		...
	
	@abstractmethod
	def can_emulate_network_conditions(self) -> bool:
		...
	
	@abstractmethod
	def clear_accepted_encodings_override(self) -> None:
		...
	
	@abstractmethod
	def clear_browser_cache(self) -> None:
		...
	
	@abstractmethod
	def clear_browser_cookies(self) -> None:
		...
	
	@abstractmethod
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
		...
	
	@abstractmethod
	def delete_cookies(
			self,
			name: str,
			url: Optional[str] = None,
			domain: Optional[str] = None,
			path: Optional[str] = None,
			partition_key: Optional[Dict[str, Any]] = None
	) -> None:
		...
	
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
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
		...
	
	@abstractmethod
	def emulate_network_conditions_by_rule(self, offline: bool, matched_network_conditions: List[Dict[str, Any]]) -> List[str]:
		...
	
	@abstractmethod
	def enable(
			self,
			max_total_buffer_size: Optional[int] = None,
			max_resource_buffer_size: Optional[int] = None,
			max_post_data_size: Optional[int] = None,
			report_direct_socket_traffic: Optional[bool] = None,
			enable_durable_messages: Optional[bool] = None
	) -> None:
		...
	
	@abstractmethod
	def enable_reporting_api(self, enable: bool) -> None:
		...
	
	@abstractmethod
	def get_all_cookies(self) -> List[Dict[str, Any]]:
		...
	
	@abstractmethod
	def get_certificate(self, origin: str) -> List[str]:
		...
	
	@abstractmethod
	def get_cookies(self, urls: Optional[List[str]] = None) -> List[Dict[str, Any]]:
		...
	
	@abstractmethod
	def get_ip_protection_proxy_status(self) -> str:
		...
	
	@abstractmethod
	def get_request_post_data(self, request_id: str) -> str:
		...
	
	@abstractmethod
	def get_response_body(self, request_id: str) -> Tuple[str, bool]:
		...
	
	@abstractmethod
	def get_response_body_for_interception(self, interception_id: str) -> Tuple[str, bool]:
		...
	
	@abstractmethod
	def get_security_isolation_status(self, frame_id: Optional[str] = None) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def load_network_resource(
			self,
			frame_id: Optional[str] = None,
			url: str = None,
			options: Dict[str, Any] = None
	) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def override_network_state(
			self,
			offline: bool,
			latency: float,
			download_throughput: float,
			upload_throughput: float,
			connection_type: Optional[str] = None
	) -> None:
		...
	
	@abstractmethod
	def replay_xhr(self, request_id: str) -> None:
		...
	
	@abstractmethod
	def search_in_response_body(
			self,
			request_id: str,
			query: str,
			case_sensitive: Optional[bool] = None,
			is_regex: Optional[bool] = None
	) -> List[Dict[str, Any]]:
		...
	
	@abstractmethod
	def set_accepted_encodings(self, encodings: List[str]) -> None:
		...
	
	@abstractmethod
	def set_attach_debug_stack(self, enabled: bool) -> None:
		...
	
	@abstractmethod
	def set_blocked_ur_ls(
			self,
			url_patterns: Optional[List[Dict[str, Any]]] = None,
			urls: Optional[List[str]] = None
	) -> None:
		...
	
	@abstractmethod
	def set_bypass_service_worker(self, bypass: bool) -> None:
		...
	
	@abstractmethod
	def set_cache_disabled(self, cache_disabled: bool) -> None:
		...
	
	@abstractmethod
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
		...
	
	@abstractmethod
	def set_cookie_controls(
			self,
			enable_third_party_cookie_restriction: bool,
			disable_third_party_cookie_metadata: bool,
			disable_third_party_cookie_heuristics: bool
	) -> None:
		...
	
	@abstractmethod
	def set_cookies(self, cookies: List[Dict[str, Any]]) -> None:
		...
	
	@abstractmethod
	def set_extra_http_headers(self, headers: Dict[Any, Any]) -> None:
		...
	
	@abstractmethod
	def set_ip_protection_proxy_bypass_enabled(self, enabled: bool) -> None:
		...
	
	@abstractmethod
	def set_request_interception(self, patterns: List[Dict[str, Any]]) -> None:
		...
	
	@abstractmethod
	def set_user_agent_override(
			self,
			user_agent: str,
			accept_language: Optional[str] = None,
			platform: Optional[str] = None,
			user_agent_metadata: Optional[Dict[str, Any]] = None
	) -> None:
		...
	
	@abstractmethod
	def stream_resource_content(self, request_id: str) -> str:
		...
	
	@abstractmethod
	def take_response_body_for_interception_as_stream(self, interception_id: str) -> str:
		...
