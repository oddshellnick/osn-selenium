from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.executors.unified.cdp.audits import (
	UnifiedAuditsCDPExecutor
)
from osn_selenium.abstract.executors.cdp.audits import (
	AbstractAuditsCDPExecutor
)


__all__ = ["AuditsCDPExecutor"]


class AuditsCDPExecutor(UnifiedAuditsCDPExecutor, AbstractAuditsCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedAuditsCDPExecutor.__init__(self, execute_function=execute_function)
	
	def check_contrast(self, report_aaa: Optional[bool] = None) -> None:
		return self._check_contrast_impl(report_aaa=report_aaa)
	
	def check_forms_issues(self) -> List[Dict[str, Any]]:
		return self._check_forms_issues_impl()
	
	def disable(self) -> None:
		return self._disable_impl()
	
	def enable(self) -> None:
		return self._enable_impl()
	
	def get_encoded_response(
			self,
			request_id: str,
			encoding: str,
			quality: Optional[float] = None,
			size_only: Optional[bool] = None
	) -> Tuple[Optional[str], int, int]:
		return self._get_encoded_response_impl(
				request_id=request_id,
				encoding=encoding,
				quality=quality,
				size_only=size_only
		)
