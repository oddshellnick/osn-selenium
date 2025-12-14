from typing import (
	Any,
	Callable,
	Dict,
	Optional
)
from osn_selenium.abstract.executors.cdp.fedcm import (
	AbstractFedCmCDPExecutor
)


class FedCmCDPExecutor(AbstractFedCmCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def click_dialog_button(self, dialog_id: str, dialog_button: str) -> None:
		return self._execute_function("FedCm.clickDialogButton", locals())
	
	def disable(self) -> None:
		return self._execute_function("FedCm.disable", locals())
	
	def dismiss_dialog(self, dialog_id: str, trigger_cooldown: Optional[bool] = None) -> None:
		return self._execute_function("FedCm.dismissDialog", locals())
	
	def enable(self, disable_rejection_delay: Optional[bool] = None) -> None:
		return self._execute_function("FedCm.enable", locals())
	
	def open_url(self, dialog_id: str, account_index: int, account_url_type: str) -> None:
		return self._execute_function("FedCm.openUrl", locals())
	
	def reset_cooldown(self) -> None:
		return self._execute_function("FedCm.resetCooldown", locals())
	
	def select_account(self, dialog_id: str, account_index: int) -> None:
		return self._execute_function("FedCm.selectAccount", locals())
