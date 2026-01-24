from typing import List, Union
from osn_selenium.exceptions.instance import NotExpectedTypeError
from selenium.webdriver.remote.mobile import (
	Mobile as legacyMobile,
	_ConnectionType
)


__all__ = ["UnifiedMobile"]


class UnifiedMobile:
	def __init__(self, selenium_mobile: legacyMobile):
		if not isinstance(selenium_mobile, legacyMobile):
			raise NotExpectedTypeError(expected_type=legacyMobile, received_instance=selenium_mobile)
		
		self._selenium_mobile = selenium_mobile
	
	def _contexts_impl(self) -> List[str]:
		return self._legacy_impl.contexts
	
	def _get_context_impl(self) -> str:
		return self._legacy_impl.context
	
	@property
	def _legacy_impl(self) -> legacyMobile:
		return self._selenium_mobile
	
	def _network_connection_impl(self) -> _ConnectionType:
		return self._legacy_impl.network_connection
	
	def _set_context_impl(self, new_context: str) -> None:
		self._legacy_impl.context = new_context
	
	def _set_network_connection_impl(self, network: Union[int, _ConnectionType]) -> _ConnectionType:
		return self._legacy_impl.set_network_connection(network)
