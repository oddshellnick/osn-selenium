from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)


__all__ = ["UnifiedFetchCDPExecutor"]


class UnifiedFetchCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _continue_request_impl(
			self,
			request_id: str,
			url: Optional[str] = None,
			method: Optional[str] = None,
			post_data: Optional[str] = None,
			headers: Optional[List[Dict[str, Any]]] = None,
			intercept_response: Optional[bool] = None
	) -> None:
		return self._execute_function(
				"Fetch.continueRequest",
				{
					"request_id": request_id,
					"url": url,
					"method": method,
					"post_data": post_data,
					"headers": headers,
					"intercept_response": intercept_response
				}
		)
	
	def _continue_response_impl(
			self,
			request_id: str,
			response_code: Optional[int] = None,
			response_phrase: Optional[str] = None,
			response_headers: Optional[List[Dict[str, Any]]] = None,
			binary_response_headers: Optional[str] = None
	) -> None:
		return self._execute_function(
				"Fetch.continueResponse",
				{
					"request_id": request_id,
					"response_code": response_code,
					"response_phrase": response_phrase,
					"response_headers": response_headers,
					"binary_response_headers": binary_response_headers
				}
		)
	
	def _continue_with_auth_impl(self, request_id: str, auth_challenge_response: Dict[str, Any]) -> None:
		return self._execute_function(
				"Fetch.continueWithAuth",
				{
					"request_id": request_id,
					"auth_challenge_response": auth_challenge_response
				}
		)
	
	def _disable_impl(self) -> None:
		return self._execute_function("Fetch.disable", {})
	
	def _enable_impl(
			self,
			patterns: Optional[List[Dict[str, Any]]] = None,
			handle_auth_requests: Optional[bool] = None
	) -> None:
		return self._execute_function(
				"Fetch.enable",
				{"patterns": patterns, "handle_auth_requests": handle_auth_requests}
		)
	
	def _fail_request_impl(self, request_id: str, error_reason: str) -> None:
		return self._execute_function(
				"Fetch.failRequest",
				{"request_id": request_id, "error_reason": error_reason}
		)
	
	def _fulfill_request_impl(
			self,
			request_id: str,
			response_code: int,
			response_headers: Optional[List[Dict[str, Any]]] = None,
			binary_response_headers: Optional[str] = None,
			body: Optional[str] = None,
			response_phrase: Optional[str] = None
	) -> None:
		return self._execute_function(
				"Fetch.fulfillRequest",
				{
					"request_id": request_id,
					"response_code": response_code,
					"response_headers": response_headers,
					"binary_response_headers": binary_response_headers,
					"body": body,
					"response_phrase": response_phrase
				}
		)
	
	def _get_response_body_impl(self, request_id: str) -> Tuple[str, bool]:
		return self._execute_function("Fetch.getResponseBody", {"request_id": request_id})
	
	def _take_response_body_as_stream_impl(self, request_id: str) -> str:
		return self._execute_function("Fetch.takeResponseBodyAsStream", {"request_id": request_id})
