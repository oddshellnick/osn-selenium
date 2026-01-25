from typing import Dict, List, Optional
from selenium.webdriver.remote.fedcm import FedCM as legacyFedCM
from osn_selenium.exceptions.instance import NotExpectedTypeError


__all__ = ["UnifiedFedCM"]


class UnifiedFedCM:
	def __init__(self, selenium_fedcm: legacyFedCM):
		if not isinstance(selenium_fedcm, legacyFedCM):
			raise NotExpectedTypeError(expected_type=legacyFedCM, received_instance=selenium_fedcm)
		
		self._selenium_fedcm = selenium_fedcm
	
	def _accept_impl(self) -> None:
		self._legacy_impl.accept()
	
	def _account_list_impl(self) -> List[Dict]:
		return self._legacy_impl.account_list
	
	def _dialog_type_impl(self) -> str:
		return self._legacy_impl.dialog_type
	
	def _disable_delay_impl(self) -> None:
		self._legacy_impl.disable_delay()
	
	def _dismiss_impl(self) -> None:
		self._legacy_impl.dismiss()
	
	def _enable_delay_impl(self) -> None:
		self._legacy_impl.enable_delay()
	
	@property
	def _legacy_impl(self) -> legacyFedCM:
		return self._selenium_fedcm
	
	def _reset_cooldown_impl(self) -> None:
		self._legacy_impl.reset_cooldown()
	
	def _select_account_impl(self, index: int) -> None:
		self._legacy_impl.select_account(index=index)
	
	def _subtitle_impl(self) -> Optional[str]:
		return self._legacy_impl.subtitle
	
	def _title_impl(self) -> str:
		return self._legacy_impl.title
