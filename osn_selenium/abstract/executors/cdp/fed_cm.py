from typing import Optional
from abc import ABC, abstractmethod


__all__ = ["AbstractFedCmCDPExecutor"]


class AbstractFedCmCDPExecutor(ABC):
	@abstractmethod
	def click_dialog_button(self, dialog_id: str, dialog_button: str) -> None:
		...
	
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def dismiss_dialog(self, dialog_id: str, trigger_cooldown: Optional[bool] = None) -> None:
		...
	
	@abstractmethod
	def enable(self, disable_rejection_delay: Optional[bool] = None) -> None:
		...
	
	@abstractmethod
	def open_url(self, dialog_id: str, account_index: int, account_url_type: str) -> None:
		...
	
	@abstractmethod
	def reset_cooldown(self) -> None:
		...
	
	@abstractmethod
	def select_account(self, dialog_id: str, account_index: int) -> None:
		...
