from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.abstract.executors.cdp.audits import (
	AbstractAuditsCDPExecutor
)


class AuditsCDPExecutor(AbstractAuditsCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def check_contrast(self, report_aaa: Optional[bool] = None) -> None:
		return await self._execute_function("Audits.checkContrast", locals())
	
	async def check_forms_issues(self) -> List[Any]:
		return await self._execute_function("Audits.checkFormsIssues", locals())
	
	async def disable(self) -> None:
		return await self._execute_function("Audits.disable", locals())
	
	async def enable(self) -> None:
		return await self._execute_function("Audits.enable", locals())
	
	async def get_encoded_response(
			self,
			request_id: str,
			encoding: str,
			quality: Optional[float] = None,
			size_only: Optional[bool] = None
	) -> Tuple[Optional[str], int, int]:
		return await self._execute_function("Audits.getEncodedResponse", locals())
