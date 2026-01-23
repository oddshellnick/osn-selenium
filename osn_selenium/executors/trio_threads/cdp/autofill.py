import trio
from osn_selenium.base_mixin import TrioThreadMixin
from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional
)
from osn_selenium.executors.unified.cdp.autofill import (
	UnifiedAutofillCDPExecutor
)
from osn_selenium.abstract.executors.cdp.autofill import (
	AbstractAutofillCDPExecutor
)


__all__ = ["AutofillCDPExecutor"]


class AutofillCDPExecutor(
		UnifiedAutofillCDPExecutor,
		TrioThreadMixin,
		AbstractAutofillCDPExecutor
):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedAutofillCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def disable(self) -> None:
		return await self.sync_to_trio(sync_function=self._disable_impl)()
	
	async def enable(self) -> None:
		return await self.sync_to_trio(sync_function=self._enable_impl)()
	
	async def set_addresses(self, addresses: List[Dict[str, Any]]) -> None:
		return await self.sync_to_trio(sync_function=self._set_addresses_impl)(addresses=addresses)
	
	async def trigger(
			self,
			field_id: int,
			frame_id: Optional[str] = None,
			card: Optional[Dict[str, Any]] = None,
			address: Optional[Dict[str, Any]] = None
	) -> None:
		return await self.sync_to_trio(sync_function=self._trigger_impl)(field_id=field_id, frame_id=frame_id, card=card, address=address)
