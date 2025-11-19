import trio
from osn_selenium.base_mixin import TrioThreadMixin
from typing import (
	Any,
	Callable,
	Dict,
	List,
	Tuple
)
from osn_selenium.executors.unified.cdp.system_info import (
	UnifiedSystemInfoCDPExecutor
)
from osn_selenium.abstract.executors.cdp.system_info import (
	AbstractSystemInfoCDPExecutor
)


__all__ = ["SystemInfoCDPExecutor"]


class SystemInfoCDPExecutor(
		UnifiedSystemInfoCDPExecutor,
		TrioThreadMixin,
		AbstractSystemInfoCDPExecutor
):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedSystemInfoCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def get_feature_state(self, feature_state: str) -> bool:
		return await self.sync_to_trio(sync_function=self._get_feature_state_impl)(feature_state=feature_state)
	
	async def get_info(self) -> Tuple[Dict[str, Any], str, str, str]:
		return await self.sync_to_trio(sync_function=self._get_info_impl)()
	
	async def get_process_info(self) -> List[Dict[str, Any]]:
		return await self.sync_to_trio(sync_function=self._get_process_info_impl)()
