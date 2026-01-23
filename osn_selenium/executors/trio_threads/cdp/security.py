import trio
from typing import Any, Callable, Dict
from osn_selenium.base_mixin import TrioThreadMixin
from osn_selenium.executors.unified.cdp.security import (
	UnifiedSecurityCDPExecutor
)
from osn_selenium.abstract.executors.cdp.security import (
	AbstractSecurityCDPExecutor
)


__all__ = ["SecurityCDPExecutor"]


class SecurityCDPExecutor(
		UnifiedSecurityCDPExecutor,
		TrioThreadMixin,
		AbstractSecurityCDPExecutor
):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedSecurityCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def disable(self) -> None:
		return await self.sync_to_trio(sync_function=self._disable_impl)()
	
	async def enable(self) -> None:
		return await self.sync_to_trio(sync_function=self._enable_impl)()
	
	async def handle_certificate_error(self, event_id: int, action: str) -> None:
		return await self.sync_to_trio(sync_function=self._handle_certificate_error_impl)(event_id=event_id, action=action)
	
	async def set_ignore_certificate_errors(self, ignore: bool) -> None:
		return await self.sync_to_trio(sync_function=self._set_ignore_certificate_errors_impl)(ignore=ignore)
	
	async def set_override_certificate_errors(self, override: bool) -> None:
		return await self.sync_to_trio(sync_function=self._set_override_certificate_errors_impl)(override=override)
