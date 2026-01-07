from typing import (
	Any,
	Callable,
	Coroutine,
	Dict
)
from osn_selenium.abstract.executors.cdp.security import (
	AbstractSecurityCDPExecutor
)


class SecurityCDPExecutor(AbstractSecurityCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def disable(self) -> None:
		return await self._execute_function("Security.disable", locals())
	
	async def enable(self) -> None:
		return await self._execute_function("Security.enable", locals())
	
	async def handle_certificate_error(self, event_id: int, action: str) -> None:
		return await self._execute_function("Security.handleCertificateError", locals())
	
	async def set_ignore_certificate_errors(self, ignore: bool) -> None:
		return await self._execute_function("Security.setIgnoreCertificateErrors", locals())
	
	async def set_override_certificate_errors(self, override: bool) -> None:
		return await self._execute_function("Security.setOverrideCertificateErrors", locals())
