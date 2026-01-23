import trio
from osn_selenium.base_mixin import TrioThreadMixin
from typing import (
	Any,
	Callable,
	Dict,
	Optional
)
from osn_selenium.executors.unified.cdp.fed_cm import (
	UnifiedFedCmCDPExecutor
)
from osn_selenium.abstract.executors.cdp.fed_cm import (
	AbstractFedCmCDPExecutor
)


__all__ = ["FedCmCDPExecutor"]


class FedCmCDPExecutor(UnifiedFedCmCDPExecutor, TrioThreadMixin, AbstractFedCmCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedFedCmCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def click_dialog_button(self, dialog_id: str, dialog_button: str) -> None:
		return await self.sync_to_trio(sync_function=self._click_dialog_button_impl)(dialog_id=dialog_id, dialog_button=dialog_button)
	
	async def disable(self) -> None:
		return await self.sync_to_trio(sync_function=self._disable_impl)()
	
	async def dismiss_dialog(self, dialog_id: str, trigger_cooldown: Optional[bool] = None) -> None:
		return await self.sync_to_trio(sync_function=self._dismiss_dialog_impl)(dialog_id=dialog_id, trigger_cooldown=trigger_cooldown)
	
	async def enable(self, disable_rejection_delay: Optional[bool] = None) -> None:
		return await self.sync_to_trio(sync_function=self._enable_impl)(disable_rejection_delay=disable_rejection_delay)
	
	async def open_url(self, dialog_id: str, account_index: int, account_url_type: str) -> None:
		return await self.sync_to_trio(sync_function=self._open_url_impl)(
				dialog_id=dialog_id,
				account_index=account_index,
				account_url_type=account_url_type
		)
	
	async def reset_cooldown(self) -> None:
		return await self.sync_to_trio(sync_function=self._reset_cooldown_impl)()
	
	async def select_account(self, dialog_id: str, account_index: int) -> None:
		return await self.sync_to_trio(sync_function=self._select_account_impl)(dialog_id=dialog_id, account_index=account_index)
