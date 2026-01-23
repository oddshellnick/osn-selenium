from typing import List, Optional
from selenium.webdriver.common.fedcm.account import Account
from osn_selenium.exceptions.instance import NotExpectedTypeError
from selenium.webdriver.common.fedcm.dialog import (
	Dialog as legacyDialog
)


__all__ = ["UnifiedDialog"]


class UnifiedDialog:
	def __init__(self, selenium_dialog: legacyDialog):
		if not isinstance(selenium_dialog, legacyDialog):
			raise NotExpectedTypeError(expected_type=legacyDialog, received_instance=selenium_dialog)
		
		self._selenium_dialog = selenium_dialog
	
	def _accept_impl(self) -> None:
		self._legacy_impl.accept()
	
	def _dismiss_impl(self) -> None:
		self._legacy_impl.dismiss()
	
	def _get_accounts_impl(self) -> List[Account]:
		return self._legacy_impl.get_accounts()
	
	@property
	def _legacy_impl(self) -> legacyDialog:
		return self._selenium_dialog
	
	def _select_account_impl(self, index: int) -> None:
		self._legacy_impl.select_account(index=index)
	
	def _subtitle_impl(self) -> Optional[str]:
		return self._legacy_impl.subtitle
	
	def _title_impl(self) -> str:
		return self._legacy_impl.title
	
	def _type_impl(self) -> Optional[str]:
		return self._legacy_impl.type
