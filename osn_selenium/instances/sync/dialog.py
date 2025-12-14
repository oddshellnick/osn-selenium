from typing import List, Optional, Self
from osn_selenium.instances.types import DIALOG_TYPEHINT
from selenium.webdriver.common.fedcm.account import Account
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.abstract.instances.dialog import AbstractDialog
from selenium.webdriver.common.fedcm.dialog import (
	Dialog as legacyDialog
)


class Dialog(AbstractDialog):
	def __init__(self, selenium_dialog: legacyDialog) -> None:
		if not isinstance(selenium_dialog, legacyDialog):
			raise TypeError(f"Expected {type(legacyDialog)}, got {type(selenium_dialog)}")
		
		self._selenium_dialog = selenium_dialog
	
	def accept(self) -> None:
		self.legacy.accept()
	
	def dismiss(self) -> None:
		self.legacy.dismiss()
	
	@classmethod
	def from_legacy(cls, selenium_dialog: DIALOG_TYPEHINT) -> Self:
		"""
		Creates an instance from a legacy Selenium Dialog object.

		This factory method is used to wrap an existing Selenium Dialog
		instance into the new interface.

		Args:
			selenium_dialog (DIALOG_TYPEHINT): The legacy Selenium Dialog instance or its wrapper.

		Returns:
			Self: A new instance of a class implementing Dialog.
		"""

		legacy_dialog_obj = get_legacy_instance(selenium_dialog)
		
		if not isinstance(legacy_dialog_obj, legacyDialog):
			raise TypeError(
					f"Could not convert input to {type(legacyDialog)}: {type(selenium_dialog)}"
			)
		
		return cls(selenium_dialog=legacy_dialog_obj)
	
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
