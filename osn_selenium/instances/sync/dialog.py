from typing import List, Optional, Self
from selenium.webdriver.common.fedcm.account import Account
from osn_selenium.instances._typehints import DIALOG_TYPEHINT
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.instances.unified.dialog import UnifiedDialog
from osn_selenium.abstract.instances.dialog import AbstractDialog
from osn_selenium.exceptions.instance import (
	CannotConvertTypeError
)
from selenium.webdriver.common.fedcm.dialog import (
	Dialog as legacyDialog
)


__all__ = ["Dialog"]


class Dialog(UnifiedDialog, AbstractDialog):
	"""
	Wrapper for the legacy Selenium FedCM Dialog instance (Synchronous).

	Handles Federated Credential Management dialogs, including account selection
	and dismissal.
	"""
	
	def __init__(self, selenium_dialog: legacyDialog) -> None:
		"""
		Initializes the Dialog wrapper.

		Args:
			selenium_dialog (legacyDialog): The legacy Selenium Dialog instance to wrap.
		"""
		
		UnifiedDialog.__init__(self, selenium_dialog=selenium_dialog)
	
	def accept(self) -> None:
		self._accept_impl()
	
	def dismiss(self) -> None:
		self._dismiss_impl()
	
	@classmethod
	def from_legacy(cls, legacy_object: DIALOG_TYPEHINT) -> Self:
		"""
		Creates an instance from a legacy Selenium Dialog object.

		This factory method is used to wrap an existing Selenium Dialog
		instance into the new interface.

		Args:
			selenium_dialog (DIALOG_TYPEHINT): The legacy Selenium Dialog instance or its wrapper.

		Returns:
			Self: A new instance of a class implementing Dialog.
		"""
		
		legacy_dialog_obj = get_legacy_instance(instance=legacy_object)
		
		if not isinstance(legacy_dialog_obj, legacyDialog):
			raise CannotConvertTypeError(from_=legacyDialog, to_=legacy_object)
		
		return cls(selenium_dialog=legacy_dialog_obj)
	
	def get_accounts(self) -> List[Account]:
		return self._get_accounts_impl()
	
	@property
	def legacy(self) -> legacyDialog:
		return self._legacy_impl
	
	def select_account(self, index: int) -> None:
		self._select_account_impl(index=index)
	
	def subtitle(self) -> Optional[str]:
		return self._subtitle_impl()
	
	def title(self) -> str:
		return self._title_impl()
	
	def type(self) -> Optional[str]:
		return self._type_impl()
