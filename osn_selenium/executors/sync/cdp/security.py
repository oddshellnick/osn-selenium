from typing import Any, Callable, Dict
from osn_selenium.abstract.executors.cdp.security import (
	AbstractSecurityCDPExecutor
)


class SecurityCDPExecutor(AbstractSecurityCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def disable(self) -> None:
		return self._execute_function("Security.disable", locals())
	
	def enable(self) -> None:
		return self._execute_function("Security.enable", locals())
	
	def handle_certificate_error(self, event_id: int, action: str) -> None:
		return self._execute_function("Security.handleCertificateError", locals())
	
	def set_ignore_certificate_errors(self, ignore: bool) -> None:
		return self._execute_function("Security.setIgnoreCertificateErrors", locals())
	
	def set_override_certificate_errors(self, override: bool) -> None:
		return self._execute_function("Security.setOverrideCertificateErrors", locals())
