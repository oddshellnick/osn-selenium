import trio
from osn_selenium.base_mixin import TrioThreadMixin
from typing import (
	Any,
	Callable,
	Dict,
	List
)
from osn_selenium.executors.unified.cdp.schema import (
	UnifiedSchemaCDPExecutor
)
from osn_selenium.abstract.executors.cdp.schema import (
	AbstractSchemaCDPExecutor
)


__all__ = ["SchemaCDPExecutor"]


class SchemaCDPExecutor(UnifiedSchemaCDPExecutor, TrioThreadMixin, AbstractSchemaCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedSchemaCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def get_domains(self) -> List[Dict[str, Any]]:
		return await self.sync_to_trio(sync_function=self._get_domains_impl)()
