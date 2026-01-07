from osn_selenium.abstract.executors.cdp.fetch import (
	AbstractFetchCDPExecutor
)
from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	List,
	Optional,
	Tuple
)


class FetchCDPExecutor(AbstractFetchCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def continue_request(
			self,
			request_id: str,
			url: Optional[str] = None,
			method: Optional[str] = None,
			post_data: Optional[str] = None,
			headers: Optional[List[Any]] = None,
			intercept_response: Optional[bool] = None
	) -> None:
		return await self._execute_function("Fetch.continueRequest", locals())
	
	async def continue_response(
			self,
			request_id: str,
			response_code: Optional[int] = None,
			response_phrase: Optional[str] = None,
			response_headers: Optional[List[Any]] = None,
			binary_response_headers: Optional[str] = None
	) -> None:
		return await self._execute_function("Fetch.continueResponse", locals())
	
	async def continue_with_auth(self, request_id: str, auth_challenge_response: Any) -> None:
		return await self._execute_function("Fetch.continueWithAuth", locals())
	
	async def disable(self) -> None:
		return await self._execute_function("Fetch.disable", locals())
	
	async def enable(
			self,
			patterns: Optional[List[Any]] = None,
			handle_auth_requests: Optional[bool] = None
	) -> None:
		return await self._execute_function("Fetch.enable", locals())
	
	async def fail_request(self, request_id: str, error_reason: str) -> None:
		return await self._execute_function("Fetch.failRequest", locals())
	
	async def fulfill_request(
			self,
			request_id: str,
			response_code: int,
			response_headers: Optional[List[Any]] = None,
			binary_response_headers: Optional[str] = None,
			body: Optional[str] = None,
			response_phrase: Optional[str] = None
	) -> None:
		return await self._execute_function("Fetch.fulfillRequest", locals())
	
	async def get_response_body(self, request_id: str) -> Tuple[str, bool]:
		return await self._execute_function("Fetch.getResponseBody", locals())
	
	async def take_response_body_as_stream(self, request_id: str) -> str:
		return await self._execute_function("Fetch.takeResponseBodyAsStream", locals())
