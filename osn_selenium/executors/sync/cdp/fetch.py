from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.abstract.executors.cdp.fetch import (
	AbstractFetchCDPExecutor
)


class FetchCDPExecutor(AbstractFetchCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def continue_request(
			self,
			request_id: str,
			url: Optional[str] = None,
			method: Optional[str] = None,
			post_data: Optional[str] = None,
			headers: Optional[List[Any]] = None,
			intercept_response: Optional[bool] = None
	) -> None:
		return self._execute_function("Fetch.continueRequest", locals())
	
	def continue_response(
			self,
			request_id: str,
			response_code: Optional[int] = None,
			response_phrase: Optional[str] = None,
			response_headers: Optional[List[Any]] = None,
			binary_response_headers: Optional[str] = None
	) -> None:
		return self._execute_function("Fetch.continueResponse", locals())
	
	def continue_with_auth(self, request_id: str, auth_challenge_response: Any) -> None:
		return self._execute_function("Fetch.continueWithAuth", locals())
	
	def disable(self) -> None:
		return self._execute_function("Fetch.disable", locals())
	
	def enable(
			self,
			patterns: Optional[List[Any]] = None,
			handle_auth_requests: Optional[bool] = None
	) -> None:
		return self._execute_function("Fetch.enable", locals())
	
	def fail_request(self, request_id: str, error_reason: str) -> None:
		return self._execute_function("Fetch.failRequest", locals())
	
	def fulfill_request(
			self,
			request_id: str,
			response_code: int,
			response_headers: Optional[List[Any]] = None,
			binary_response_headers: Optional[str] = None,
			body: Optional[str] = None,
			response_phrase: Optional[str] = None
	) -> None:
		return self._execute_function("Fetch.fulfillRequest", locals())
	
	def get_response_body(self, request_id: str) -> Tuple[str]:
		return self._execute_function("Fetch.getResponseBody", locals())
	
	def take_response_body_as_stream(self, request_id: str) -> str:
		return self._execute_function("Fetch.takeResponseBodyAsStream", locals())
