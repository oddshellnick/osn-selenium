from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.executors.unified.cdp.fetch import (
	UnifiedFetchCDPExecutor
)
from osn_selenium.abstract.executors.cdp.fetch import (
	AbstractFetchCDPExecutor
)


__all__ = ["FetchCDPExecutor"]


class FetchCDPExecutor(UnifiedFetchCDPExecutor, AbstractFetchCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedFetchCDPExecutor.__init__(self, execute_function=execute_function)
	
	def continue_request(
			self,
			request_id: str,
			url: Optional[str] = None,
			method: Optional[str] = None,
			post_data: Optional[str] = None,
			headers: Optional[List[Dict[str, Any]]] = None,
			intercept_response: Optional[bool] = None
	) -> None:
		return self._continue_request_impl(
				request_id=request_id,
				url=url,
				method=method,
				post_data=post_data,
				headers=headers,
				intercept_response=intercept_response
		)
	
	def continue_response(
			self,
			request_id: str,
			response_code: Optional[int] = None,
			response_phrase: Optional[str] = None,
			response_headers: Optional[List[Dict[str, Any]]] = None,
			binary_response_headers: Optional[str] = None
	) -> None:
		return self._continue_response_impl(
				request_id=request_id,
				response_code=response_code,
				response_phrase=response_phrase,
				response_headers=response_headers,
				binary_response_headers=binary_response_headers
		)
	
	def continue_with_auth(self, request_id: str, auth_challenge_response: Dict[str, Any]) -> None:
		return self._continue_with_auth_impl(request_id=request_id, auth_challenge_response=auth_challenge_response)
	
	def disable(self) -> None:
		return self._disable_impl()
	
	def enable(
			self,
			patterns: Optional[List[Dict[str, Any]]] = None,
			handle_auth_requests: Optional[bool] = None
	) -> None:
		return self._enable_impl(patterns=patterns, handle_auth_requests=handle_auth_requests)
	
	def fail_request(self, request_id: str, error_reason: str) -> None:
		return self._fail_request_impl(request_id=request_id, error_reason=error_reason)
	
	def fulfill_request(
			self,
			request_id: str,
			response_code: int,
			response_headers: Optional[List[Dict[str, Any]]] = None,
			binary_response_headers: Optional[str] = None,
			body: Optional[str] = None,
			response_phrase: Optional[str] = None
	) -> None:
		return self._fulfill_request_impl(
				request_id=request_id,
				response_code=response_code,
				response_headers=response_headers,
				binary_response_headers=binary_response_headers,
				body=body,
				response_phrase=response_phrase
		)
	
	def get_response_body(self, request_id: str) -> Tuple[str, bool]:
		return self._get_response_body_impl(request_id=request_id)
	
	def take_response_body_as_stream(self, request_id: str) -> str:
		return self._take_response_body_as_stream_impl(request_id=request_id)
