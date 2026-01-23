from typing import (
	Any,
	Callable,
	Dict,
	Optional
)


__all__ = ["UnifiedFedCmCDPExecutor"]


class UnifiedFedCmCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _click_dialog_button_impl(self, dialog_id: str, dialog_button: str) -> None:
		return self._execute_function(
				"FedCm.clickDialogButton",
				{"dialog_id": dialog_id, "dialog_button": dialog_button}
		)
	
	def _disable_impl(self) -> None:
		return self._execute_function("FedCm.disable", {})
	
	def _dismiss_dialog_impl(self, dialog_id: str, trigger_cooldown: Optional[bool] = None) -> None:
		return self._execute_function(
				"FedCm.dismissDialog",
				{"dialog_id": dialog_id, "trigger_cooldown": trigger_cooldown}
		)
	
	def _enable_impl(self, disable_rejection_delay: Optional[bool] = None) -> None:
		return self._execute_function("FedCm.enable", {"disable_rejection_delay": disable_rejection_delay})
	
	def _open_url_impl(self, dialog_id: str, account_index: int, account_url_type: str) -> None:
		return self._execute_function(
				"FedCm.openUrl",
				{
					"dialog_id": dialog_id,
					"account_index": account_index,
					"account_url_type": account_url_type
				}
		)
	
	def _reset_cooldown_impl(self) -> None:
		return self._execute_function("FedCm.resetCooldown", {})
	
	def _select_account_impl(self, dialog_id: str, account_index: int) -> None:
		return self._execute_function(
				"FedCm.selectAccount",
				{"dialog_id": dialog_id, "account_index": account_index}
		)
