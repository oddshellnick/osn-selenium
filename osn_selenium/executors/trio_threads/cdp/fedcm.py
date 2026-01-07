from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	Optional
)
from osn_selenium.abstract.executors.cdp.fedcm import (
	AbstractFedCmCDPExecutor
)


class AsyncFedCmCDPExecutor(AbstractFedCmCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def click_dialog_button(self, dialog_id: str, dialog_button: str) -> None:
		return await self._execute_function("FedCm.clickDialogButton", locals())
	
	async def disable(self) -> None:
		return await self._execute_function("FedCm.disable", locals())
	
	async def dismiss_dialog(self, dialog_id: str, trigger_cooldown: Optional[bool] = None) -> None:
		return await self._execute_function("FedCm.dismissDialog", locals())
	
	async def enable(self, disable_rejection_delay: Optional[bool] = None) -> None:
		return await self._execute_function("FedCm.enable", locals())
	
	async def open_url(self, dialog_id: str, account_index: int, account_url_type: str) -> None:
		return await self._execute_function("FedCm.openUrl", locals())
	
	async def reset_cooldown(self) -> None:
		return await self._execute_function("FedCm.resetCooldown", locals())
	
	async def select_account(self, dialog_id: str, account_index: int) -> None:
		return await self._execute_function("FedCm.selectAccount", locals())
