from abc import ABC, abstractmethod
from typing import (
	Any,
	Dict,
	List,
	Optional,
	Tuple
)


__all__ = ["AbstractFetchCDPExecutor"]


class AbstractFetchCDPExecutor(ABC):
	@abstractmethod
	def continue_request(
			self,
			request_id: str,
			url: Optional[str] = None,
			method: Optional[str] = None,
			post_data: Optional[str] = None,
			headers: Optional[List[Dict[str, Any]]] = None,
			intercept_response: Optional[bool] = None
	) -> None:
		...
	
	@abstractmethod
	def continue_response(
			self,
			request_id: str,
			response_code: Optional[int] = None,
			response_phrase: Optional[str] = None,
			response_headers: Optional[List[Dict[str, Any]]] = None,
			binary_response_headers: Optional[str] = None
	) -> None:
		...
	
	@abstractmethod
	def continue_with_auth(self, request_id: str, auth_challenge_response: Dict[str, Any]) -> None:
		...
	
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def enable(
			self,
			patterns: Optional[List[Dict[str, Any]]] = None,
			handle_auth_requests: Optional[bool] = None
	) -> None:
		...
	
	@abstractmethod
	def fail_request(self, request_id: str, error_reason: str) -> None:
		...
	
	@abstractmethod
	def fulfill_request(
			self,
			request_id: str,
			response_code: int,
			response_headers: Optional[List[Dict[str, Any]]] = None,
			binary_response_headers: Optional[str] = None,
			body: Optional[str] = None,
			response_phrase: Optional[str] = None
	) -> None:
		...
	
	@abstractmethod
	def get_response_body(self, request_id: str) -> Tuple[str, bool]:
		...
	
	@abstractmethod
	def take_response_body_as_stream(self, request_id: str) -> str:
		...
