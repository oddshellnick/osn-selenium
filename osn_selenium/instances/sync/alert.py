from typing import Self

from osn_selenium.instances.errors import TypesConvertError, ExpectedTypeError
from osn_selenium.instances.types import ALERT_TYPEHINT
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.abstract.instances.alert import AbstractAlert
from selenium.webdriver.common.alert import Alert as legacyAlert


class Alert(AbstractAlert):
	def __init__(self, selenium_alert: legacyAlert) -> None:
		if not isinstance(selenium_alert, legacyAlert):
			raise ExpectedTypeError(expected_class=legacyAlert, received_instance=selenium_alert)
		
		self._selenium_alert = selenium_alert
	
	def accept(self) -> None:
		self._selenium_alert.accept()
	
	def dismiss(self) -> None:
		self._selenium_alert.dismiss()
	
	@classmethod
	def from_legacy(cls, selenium_alert: ALERT_TYPEHINT) -> Self:
		"""
		Creates an instance from a legacy Selenium Alert object.

		This factory method is used to wrap an existing Selenium Alert
		instance into the new interface.

		Args:
			selenium_alert (ALERT_TYPEHINT): The legacy Selenium Alert instance or its wrapper.

		Returns:
			Self: A new instance of a class implementing Alert.
		"""

		legacy_alert_obj = get_legacy_instance(selenium_alert)
		
		if not isinstance(legacy_alert_obj, legacyAlert):
			raise TypesConvertError(from_=legacyAlert, to_=selenium_alert)
		
		return cls(selenium_alert=legacy_alert_obj)
	
	@property
	def legacy(self) -> legacyAlert:
		return self._selenium_alert
	
	def send_keys(self, keysToSend: str) -> None:
		self._selenium_alert.send_keys(keysToSend=keysToSend)
	
	def text(self) -> str:
		return self._selenium_alert.text
