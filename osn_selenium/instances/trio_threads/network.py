import trio
from typing import (
	Callable,
	List,
	Optional,
	Self
)

from osn_selenium.instances.errors import TypesConvertError, ExpectedTypeError
from osn_selenium.trio_base_mixin import _TrioThreadMixin
from osn_selenium.instances.types import NETWORK_TYPEHINT
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.abstract.instances.network import AbstractNetwork
from selenium.webdriver.common.bidi.network import (
	Network as legacyNetwork
)


class Network(_TrioThreadMixin, AbstractNetwork):
	def __init__(
			self,
			selenium_network: legacyNetwork,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> None:
		super().__init__(lock=lock, limiter=limiter)
		
		if not isinstance(selenium_network, legacyNetwork):
			raise ExpectedTypeError(expected_class=legacyNetwork, received_instance=selenium_network)
		
		self._selenium_network = selenium_network
	
	async def add_auth_handler(self, username: str, password: str) -> int:
		return await self._wrap_to_trio(self.legacy.add_auth_handler, username=username, password=password)
	
	async def add_request_handler(
			self,
			event: str,
			callback: Callable,
			url_patterns: Optional[List[str]] = None,
			contexts: Optional[List[str]] = None,
	) -> int:
		return await self._wrap_to_trio(
				self.legacy.add_request_handler,
				event=event,
				callback=callback,
				url_patterns=url_patterns,
				contexts=contexts
		)
	
	async def clear_request_handlers(self) -> None:
		await self._wrap_to_trio(self.legacy.clear_request_handlers)
	
	@classmethod
	def from_legacy(
			cls,
			selenium_network: NETWORK_TYPEHINT,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> Self:
		"""
		Creates an instance from a legacy Selenium Network object.

		This factory method is used to wrap an existing Selenium Network
		instance into the new interface.

		Args:
			selenium_network (NETWORK_TYPEHINT): The legacy Selenium Network instance or its wrapper.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.

		Returns:
			Self: A new instance of a class implementing Network.
		"""
		
		legacy_network_obj = get_legacy_instance(selenium_network)
		
		if not isinstance(legacy_network_obj, legacyNetwork):
			raise TypesConvertError(from_=legacyNetwork, to_=selenium_network)
		
		return cls(selenium_network=legacy_network_obj, lock=lock, limiter=limiter)
	
	@property
	def legacy(self) -> legacyNetwork:
		return self._selenium_network
	
	async def remove_auth_handler(self, callback_id: int) -> None:
		await self._wrap_to_trio(self.legacy.remove_auth_handler, callback_id=callback_id)
	
	async def remove_request_handler(self, event: str, callback_id: int) -> None:
		await self._wrap_to_trio(
				self.legacy.remove_request_handler,
				event=event,
				callback_id=callback_id
		)
