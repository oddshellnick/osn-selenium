from typing import List, Self, Union
from osn_selenium.instances.types import MOBILE_TYPEHINT
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.abstract.instances.mobile import AbstractMobile
from selenium.webdriver.remote.mobile import (
	Mobile as legacyMobile,
	_ConnectionType
)


class Mobile(AbstractMobile):
	def __init__(self, selenium_mobile: legacyMobile) -> None:
		if not isinstance(selenium_mobile, legacyMobile):
			raise TypeError(f"Expected {type(legacyMobile)}, got {type(selenium_mobile)}")
		
		self._selenium_mobile = selenium_mobile
	
	def context(self) -> str:
		return self.legacy.context
	
	def contexts(self) -> List[str]:
		return self.legacy.contexts
	
	@classmethod
	def from_legacy(cls, selenium_mobile: MOBILE_TYPEHINT) -> Self:
		legacy_mobile_obj = get_legacy_instance(selenium_mobile)
		
		if not isinstance(legacy_mobile_obj, legacyMobile):
			raise TypeError(
					f"Could not convert input to {type(legacyMobile)}: {type(selenium_mobile)}"
			)
		
		return cls(selenium_mobile=legacy_mobile_obj)
	
	def network_connection(self) -> _ConnectionType:
		return self.legacy.network_connection
	
	@property
	def legacy(self) -> legacyMobile:
		return self._selenium_mobile
	
	def set_context(self, new_context: str) -> None:
		setattr(self.legacy, "context", new_context)
	
	def set_network_connection(self, network: Union[int, _ConnectionType]) -> _ConnectionType:
		return self.legacy.set_network_connection(network)
