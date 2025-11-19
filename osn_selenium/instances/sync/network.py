from typing import (
	Callable,
	List,
	Optional,
	Self
)
from osn_selenium.abstract.instances.network import AbstractNetwork
from selenium.webdriver.common.bidi.network import (
	Network as legacyNetwork
)


class Network(AbstractNetwork):
	def __init__(self, selenium_network: legacyNetwork,) -> None:
		self._selenium_network = selenium_network
	
	def add_auth_handler(self, username: str, password: str,) -> int:
		return self.legacy.add_auth_handler(username=username, password=password)
	
	def add_request_handler(
			self,
			event: str,
			callback: Callable,
			url_patterns: Optional[List[str]] = None,
			contexts: Optional[List[str]] = None,
	) -> int:
		return self.legacy.add_request_handler(
				event=event,
				callback=callback,
				url_patterns=url_patterns,
				contexts=contexts
		)
	
	def clear_request_handlers(self) -> None:
		self.legacy.clear_request_handlers()
	
	@classmethod
	def from_legacy(cls, selenium_network: legacyNetwork,) -> Self:
		"""
		Creates an instance from a legacy Selenium Network object.

		This factory method is used to wrap an existing Selenium Network
		instance into the new interface.

		Args:
			selenium_network (legacyNetwork): The legacy Selenium Network instance.

		Returns:
			Self: A new instance of a class implementing Network.
		"""
		
		return cls(selenium_network=selenium_network)
	
	@property
	def legacy(self) -> legacyNetwork:
		return self._selenium_network
	
	def remove_auth_handler(self, callback_id: int) -> None:
		self.legacy.remove_auth_handler(callback_id=callback_id)
	
	def remove_request_handler(self, event: str, callback_id: int,) -> None:
		self.legacy.remove_request_handler(event=event, callback_id=callback_id)
