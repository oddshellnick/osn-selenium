from typing import Self
from osn_selenium.abstract.instances.alert import AbstractAlert
from selenium.webdriver.common.alert import Alert as legacyAlert


class Alert(AbstractAlert):
	def __init__(self, selenium_alert: legacyAlert) -> None:
		self._selenium_alert = selenium_alert
	
	def accept(self) -> None:
		self._selenium_alert.accept()
	
	def dismiss(self) -> None:
		self._selenium_alert.dismiss()
	
	@classmethod
	def from_legacy(cls, selenium_alert: legacyAlert,) -> Self:
		"""
		Creates an instance from a legacy Selenium Alert object.

		This factory method is used to wrap an existing Selenium Alert
		instance into the new interface.

		Args:
			selenium_alert (legacyAlert): The legacy Selenium Alert instance.

		Returns:
			Self: A new instance of a class implementing Alert.
		"""
		
		return cls(selenium_alert=selenium_alert)
	
	@property
	def legacy(self) -> legacyAlert:
		return self._selenium_alert
	
	def send_keys(self, keysToSend: str,) -> None:
		self._selenium_alert.send_keys(keysToSend=keysToSend)
	
	def text(self) -> str:
		return self._selenium_alert.text
