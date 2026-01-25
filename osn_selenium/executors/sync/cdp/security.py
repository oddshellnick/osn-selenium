from typing import Any, Callable, Dict
from osn_selenium.executors.unified.cdp.security import (
	UnifiedSecurityCDPExecutor
)
from osn_selenium.abstract.executors.cdp.security import (
	AbstractSecurityCDPExecutor
)


__all__ = ["SecurityCDPExecutor"]


class SecurityCDPExecutor(UnifiedSecurityCDPExecutor, AbstractSecurityCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedSecurityCDPExecutor.__init__(self, execute_function=execute_function)
	
	def disable(self) -> None:
		return self._disable_impl()
	
	def enable(self) -> None:
		return self._enable_impl()
	
	def handle_certificate_error(self, event_id: int, action: str) -> None:
		return self._handle_certificate_error_impl(event_id=event_id, action=action)
	
	def set_ignore_certificate_errors(self, ignore: bool) -> None:
		return self._set_ignore_certificate_errors_impl(ignore=ignore)
	
	def set_override_certificate_errors(self, override: bool) -> None:
		return self._set_override_certificate_errors_impl(override=override)
