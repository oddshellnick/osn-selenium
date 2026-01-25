from typing import List, Self, Union
from osn_selenium.instances._typehints import MOBILE_TYPEHINT
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.instances.unified.mobile import UnifiedMobile
from osn_selenium.abstract.instances.mobile import AbstractMobile
from osn_selenium.exceptions.instance import (
	CannotConvertTypeError
)
from selenium.webdriver.remote.mobile import (
	Mobile as legacyMobile,
	_ConnectionType
)


__all__ = ["Mobile"]


class Mobile(UnifiedMobile, AbstractMobile):
	"""
	Wrapper for the legacy Selenium Mobile instance.

	Manages network connection types and context settings (e.g., native app vs web view)
	for mobile emulation.
	"""
	
	def __init__(self, selenium_mobile: legacyMobile) -> None:
		"""
		Initializes the Mobile wrapper.

		Args:
			selenium_mobile (legacyMobile): The legacy Selenium Mobile instance to wrap.
		"""
		
		UnifiedMobile.__init__(self, selenium_mobile=selenium_mobile)
	
	def context(self) -> str:
		return self._get_context_impl()
	
	def contexts(self) -> List[str]:
		return self._contexts_impl()
	
	@classmethod
	def from_legacy(cls, legacy_object: MOBILE_TYPEHINT) -> Self:
		"""
		Creates an instance from a legacy Selenium Mobile object.

		This factory method is used to wrap an existing Selenium Mobile
		instance into the new interface.

		Args:
			legacy_object (MOBILE_TYPEHINT): The legacy Selenium Mobile instance or its wrapper.

		Returns:
			Self: A new instance of a class implementing Mobile.
		"""
		
		legacy_mobile_obj = get_legacy_instance(instance=legacy_object)
		
		if not isinstance(legacy_mobile_obj, legacyMobile):
			raise CannotConvertTypeError(from_=legacyMobile, to_=legacy_object)
		
		return cls(selenium_mobile=legacy_mobile_obj)
	
	@property
	def legacy(self) -> legacyMobile:
		return self._legacy_impl
	
	def network_connection(self) -> _ConnectionType:
		return self._network_connection_impl()
	
	def set_context(self, new_context: str) -> None:
		self._set_context_impl(new_context=new_context)
	
	def set_network_connection(self, network: Union[int, _ConnectionType]) -> _ConnectionType:
		return self._set_network_connection_impl(network=network)
