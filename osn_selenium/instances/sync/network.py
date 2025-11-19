from typing import (
	Callable,
	List,
	Optional,
	Self
)
from osn_selenium.instances._typehints import NETWORK_TYPEHINT
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.instances.unified.network import UnifiedNetwork
from osn_selenium.abstract.instances.network import AbstractNetwork
from osn_selenium.exceptions.instance import (
	CannotConvertTypeError
)
from selenium.webdriver.common.bidi.network import (
	Network as legacyNetwork
)


__all__ = ["Network"]


class Network(UnifiedNetwork, AbstractNetwork):
	"""
	Wrapper for the legacy Selenium BiDi Network instance.

	Allows interception of network requests, adding authentication handlers,
	and managing request callbacks.
	"""
	
	def __init__(self, selenium_network: legacyNetwork) -> None:
		"""
		Initializes the Network wrapper.

		Args:
			selenium_network (legacyNetwork): The legacy Selenium Network instance to wrap.
		"""
		
		UnifiedNetwork.__init__(self, selenium_network=selenium_network)
	
	def add_auth_handler(self, username: str, password: str) -> int:
		return self._add_auth_handler_impl(username=username, password=password)
	
	def add_request_handler(
			self,
			event: str,
			callback: Callable,
			url_patterns: Optional[List[str]] = None,
			contexts: Optional[List[str]] = None,
	) -> int:
		return self._add_request_handler_impl(
				event=event,
				callback=callback,
				url_patterns=url_patterns,
				contexts=contexts
		)
	
	def clear_request_handlers(self) -> None:
		self._clear_request_handlers_impl()
	
	@classmethod
	def from_legacy(cls, legacy_object: NETWORK_TYPEHINT) -> Self:
		"""
		Creates an instance from a legacy Selenium Network object.

		This factory method is used to wrap an existing Selenium Network
		instance into the new interface.

		Args:
			legacy_object (NETWORK_TYPEHINT): The legacy Selenium Network instance or its wrapper.

		Returns:
			Self: A new instance of a class implementing Network.
		"""
		
		legacy_network_obj = get_legacy_instance(instance=legacy_object)
		
		if not isinstance(legacy_network_obj, legacyNetwork):
			raise CannotConvertTypeError(from_=legacyNetwork, to_=legacy_object)
		
		return cls(selenium_network=legacy_network_obj)
	
	@property
	def legacy(self) -> legacyNetwork:
		return self._legacy_impl
	
	def remove_auth_handler(self, callback_id: int) -> None:
		self._remove_auth_handler_impl(callback_id=callback_id)
	
	def remove_request_handler(self, event: str, callback_id: int) -> None:
		self._remove_request_handler_impl(event=event, callback_id=callback_id)
