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


class FedCmCDPExecutor(UnifiedFedCmCDPExecutor, AbstractFedCmCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedFedCmCDPExecutor.__init__(self, execute_function=execute_function)
	
	def click_dialog_button(self, dialog_id: str, dialog_button: str) -> None:
		return self._click_dialog_button_impl(dialog_id=dialog_id, dialog_button=dialog_button)
	
	def disable(self) -> None:
		return self._disable_impl()
	
	def dismiss_dialog(self, dialog_id: str, trigger_cooldown: Optional[bool] = None) -> None:
		return self._dismiss_dialog_impl(dialog_id=dialog_id, trigger_cooldown=trigger_cooldown)
	
	def enable(self, disable_rejection_delay: Optional[bool] = None) -> None:
		return self._enable_impl(disable_rejection_delay=disable_rejection_delay)
	
	def open_url(self, dialog_id: str, account_index: int, account_url_type: str) -> None:
		return self._open_url_impl(
				dialog_id=dialog_id,
				account_index=account_index,
				account_url_type=account_url_type
		)
	
	def reset_cooldown(self) -> None:
		return self._reset_cooldown_impl()
	
	def select_account(self, dialog_id: str, account_index: int) -> None:
		return self._select_account_impl(dialog_id=dialog_id, account_index=account_index)
