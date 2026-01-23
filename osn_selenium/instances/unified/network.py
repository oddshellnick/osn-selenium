from typing import (
	Callable,
	List,
	Optional
)
from osn_selenium.exceptions.instance import NotExpectedTypeError
from selenium.webdriver.common.bidi.network import (
	Network as legacyNetwork
)


__all__ = ["UnifiedNetwork"]


class UnifiedNetwork:
	def __init__(self, selenium_network: legacyNetwork):
		if not isinstance(selenium_network, legacyNetwork):
			raise NotExpectedTypeError(expected_type=legacyNetwork, received_instance=selenium_network)
		
		self._selenium_network = selenium_network
	
	def _add_auth_handler_impl(self, username: str, password: str) -> int:
		return self._legacy_impl.add_auth_handler(username=username, password=password)
	
	def _add_request_handler_impl(
			self,
			event: str,
			callback: Callable,
			url_patterns: Optional[List[str]] = None,
			contexts: Optional[List[str]] = None,
	) -> int:
		return self._legacy_impl.add_request_handler(
				event=event,
				callback=callback,
				url_patterns=url_patterns,
				contexts=contexts
		)
	
	def _clear_request_handlers_impl(self) -> None:
		self._legacy_impl.clear_request_handlers()
	
	@property
	def _legacy_impl(self) -> legacyNetwork:
		return self._selenium_network
	
	def _remove_auth_handler_impl(self, callback_id: int) -> None:
		self._legacy_impl.remove_auth_handler(callback_id=callback_id)
	
	def _remove_request_handler_impl(self, event: str, callback_id: int) -> None:
		self._legacy_impl.remove_request_handler(event=event, callback_id=callback_id)
