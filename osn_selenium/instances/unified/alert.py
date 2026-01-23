from selenium.webdriver.common.alert import Alert as legacyAlert
from osn_selenium.exceptions.instance import NotExpectedTypeError


__all__ = ["UnifiedAlert"]


class UnifiedAlert:
	def __init__(self, selenium_alert: legacyAlert):
		if not isinstance(selenium_alert, legacyAlert):
			raise NotExpectedTypeError(expected_type=legacyAlert, received_instance=selenium_alert)
		
		self._selenium_alert = selenium_alert
	
	def _accept_impl(self) -> None:
		self._legacy_impl.accept()
	
	def _dismiss_impl(self) -> None:
		self._legacy_impl.dismiss()
	
	@property
	def _legacy_impl(self) -> legacyAlert:
		return self._selenium_alert
	
	def _send_keys_impl(self, keysToSend: str) -> None:
		self._legacy_impl.send_keys(keysToSend=keysToSend)
	
	def _text_impl(self) -> str:
		return self._legacy_impl.text
