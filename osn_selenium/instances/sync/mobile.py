from typing import List, Self, Union
from osn_selenium.abstract.instances.mobile import AbstractMobile
from selenium.webdriver.remote.mobile import (
	Mobile as legacyMobile,
	_ConnectionType
)


class Mobile(AbstractMobile):
	def __init__(self, selenium_mobile: legacyMobile,) -> None:
		self._selenium_mobile = selenium_mobile
	
	def context(self) -> str:
		return self.legacy.context
	
	def contexts(self) -> List[str]:
		return self.legacy.contexts
	
	@classmethod
	def from_legacy(cls, selenium_mobile: legacyMobile,) -> Self:
		"""
		Creates an instance from a legacy Selenium Mobile object.

		This factory method is used to wrap an existing Selenium Mobile
		instance into the new interface.

		Args:
			selenium_mobile (legacyMobile): The legacy Selenium Mobile instance.

		Returns:
			Self: A new instance of a class implementing Mobile.
		"""
		
		return cls(selenium_mobile=selenium_mobile)
	
	def network_connection(self) -> _ConnectionType:
		return self.legacy.network_connection
	
	@property
	def legacy(self) -> legacyMobile:
		return self._selenium_mobile
	
	def set_context(self, new_context: str) -> None:
		setattr(self.legacy, "context", new_context)
	
	def set_network_connection(self, network: Union[int, _ConnectionType],) -> _ConnectionType:
		return self.legacy.set_network_connection(network)
