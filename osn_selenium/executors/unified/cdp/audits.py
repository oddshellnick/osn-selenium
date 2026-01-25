from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)


__all__ = ["UnifiedAuditsCDPExecutor"]


class UnifiedAuditsCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _check_contrast_impl(self, report_aaa: Optional[bool] = None) -> None:
		return self._execute_function("Audits.checkContrast", {"report_aaa": report_aaa})
	
	def _check_forms_issues_impl(self) -> List[Dict[str, Any]]:
		return self._execute_function("Audits.checkFormsIssues", {})
	
	def _disable_impl(self) -> None:
		return self._execute_function("Audits.disable", {})
	
	def _enable_impl(self) -> None:
		return self._execute_function("Audits.enable", {})
	
	def _get_encoded_response_impl(
			self,
			request_id: str,
			encoding: str,
			quality: Optional[float] = None,
			size_only: Optional[bool] = None
	) -> Tuple[Optional[str], int, int]:
		return self._execute_function(
				"Audits.getEncodedResponse",
				{
					"request_id": request_id,
					"encoding": encoding,
					"quality": quality,
					"size_only": size_only
				}
		)
