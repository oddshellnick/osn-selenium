import trio
from osn_selenium.base_mixin import TrioThreadMixin
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


class AuditsCDPExecutor(UnifiedAuditsCDPExecutor, TrioThreadMixin, AbstractAuditsCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedAuditsCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def check_contrast(self, report_aaa: Optional[bool] = None) -> None:
		return await self.sync_to_trio(sync_function=self._check_contrast_impl)(report_aaa=report_aaa)
	
	async def check_forms_issues(self) -> List[Dict[str, Any]]:
		return await self.sync_to_trio(sync_function=self._check_forms_issues_impl)()
	
	async def disable(self) -> None:
		return await self.sync_to_trio(sync_function=self._disable_impl)()
	
	async def enable(self) -> None:
		return await self.sync_to_trio(sync_function=self._enable_impl)()
	
	async def get_encoded_response(
			self,
			request_id: str,
			encoding: str,
			quality: Optional[float] = None,
			size_only: Optional[bool] = None
	) -> Tuple[Optional[str], int, int]:
		return await self.sync_to_trio(sync_function=self._get_encoded_response_impl)(
				request_id=request_id,
				encoding=encoding,
				quality=quality,
				size_only=size_only
		)
