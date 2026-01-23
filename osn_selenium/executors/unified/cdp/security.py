from typing import Any, Callable, Dict


__all__ = ["UnifiedSecurityCDPExecutor"]


class UnifiedSecurityCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _disable_impl(self) -> None:
		return self._execute_function("Security.disable", {})
	
	def _enable_impl(self) -> None:
		return self._execute_function("Security.enable", {})
	
	def _handle_certificate_error_impl(self, event_id: int, action: str) -> None:
		return self._execute_function(
				"Security.handleCertificateError",
				{"event_id": event_id, "action": action}
		)
	
	def _set_ignore_certificate_errors_impl(self, ignore: bool) -> None:
		return self._execute_function("Security.setIgnoreCertificateErrors", {"ignore": ignore})
	
	def _set_override_certificate_errors_impl(self, override: bool) -> None:
		return self._execute_function("Security.setOverrideCertificateErrors", {"override": override})
