from typing import Self
from osn_selenium.instances._typehints import ALERT_TYPEHINT
from osn_selenium.instances.unified.alert import UnifiedAlert
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.abstract.instances.alert import AbstractAlert
from selenium.webdriver.common.alert import Alert as legacyAlert
from osn_selenium.exceptions.instance import (
	CannotConvertTypeError
)


__all__ = ["Alert"]


class Alert(UnifiedAlert, AbstractAlert):
	"""
	Wrapper for the legacy Selenium Alert instance.

	Manages browser alerts, prompts, and confirmation dialogs, allowing
	acceptance, dismissal, text retrieval, and input.
	"""
	
	def __init__(self, selenium_alert: legacyAlert) -> None:
		"""
		Initializes the Alert wrapper.

		Args:
			selenium_alert (legacyAlert): The legacy Selenium Alert instance to wrap.
		"""
		
		UnifiedAlert.__init__(self, selenium_alert=selenium_alert)
	
	def accept(self) -> None:
		self._accept_impl()
	
	def dismiss(self) -> None:
		self._dismiss_impl()
	
	@classmethod
	def from_legacy(cls, legacy_object: ALERT_TYPEHINT) -> Self:
		"""
		Creates an instance from a legacy Selenium Alert object.

		This factory method is used to wrap an existing Selenium Alert
		instance into the new interface.

		Args:
			legacy_object (ALERT_TYPEHINT): The legacy Selenium Alert instance or its wrapper.

		Returns:
			Self: A new instance of a class implementing Alert.
		"""
		
		legacy_alert_obj = get_legacy_instance(instance=legacy_object)
		
		if not isinstance(legacy_alert_obj, legacyAlert):
			raise CannotConvertTypeError(from_=legacyAlert, to_=legacy_object)
		
		return cls(selenium_alert=legacy_alert_obj)
	
	@property
	def legacy(self) -> legacyAlert:
		return self._legacy_impl
	
	def send_keys(self, keysToSend: str) -> None:
		self._send_keys_impl(keysToSend=keysToSend)
	
	def text(self) -> str:
		return self._text_impl()
