from typing import List, Optional, Self
from selenium.webdriver.common.fedcm.account import Account
from osn_selenium.abstract.instances.dialog import AbstractDialog
from selenium.webdriver.common.fedcm.dialog import (
	Dialog as legacyDialog
)


class Dialog(AbstractDialog):
	def __init__(self, selenium_dialog: legacyDialog,) -> None:
		self._selenium_dialog = selenium_dialog
	
	def accept(self) -> None:
		self.legacy.accept()
	
	def dismiss(self) -> None:
		self.legacy.dismiss()
	
	@classmethod
	def from_legacy(cls, selenium_dialog: legacyDialog,) -> Self:
		"""
		Creates an instance from a legacy Selenium Dialog object.

		This factory method is used to wrap an existing Selenium Dialog
		instance into the new interface.

		Args:
			selenium_dialog (legacyDialog): The legacy Selenium Dialog instance.

		Returns:
			Self: A new instance of a class implementing Dialog.
		"""
		
		return cls(selenium_dialog=selenium_dialog)
	
	def get_accounts(self) -> List[Account]:
		return self.legacy.get_accounts()
	
	@property
	def legacy(self) -> legacyDialog:
		return self._selenium_dialog
	
	def select_account(self, index: int) -> None:
		self.legacy.select_account(index=index)
	
	def subtitle(self) -> Optional[str]:
		return self.legacy.subtitle
	
	def title(self) -> str:
		return self.legacy.title
	
	def type(self) -> Optional[str]:
		return self.legacy.type
