from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.abstract.executors.cdp.audits import (
	AbstractAuditsCDPExecutor
)


class AuditsCDPExecutor(AbstractAuditsCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def check_contrast(self, report_aaa: Optional[bool] = None) -> None:
		return self._execute_function("Audits.checkContrast", locals())
	
	def check_forms_issues(self) -> List[Any]:
		return self._execute_function("Audits.checkFormsIssues", locals())
	
	def disable(self) -> None:
		return self._execute_function("Audits.disable", locals())
	
	def enable(self) -> None:
		return self._execute_function("Audits.enable", locals())
	
	def get_encoded_response(
			self,
			request_id: str,
			encoding: str,
			quality: Optional[float] = None,
			size_only: Optional[bool] = None
	) -> Tuple[Optional[str], int, int]:
		return self._execute_function("Audits.getEncodedResponse", locals())
