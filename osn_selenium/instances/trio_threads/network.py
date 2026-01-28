import trio
from osn_selenium.trio_threads_mixin import TrioThreadMixin
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


class Network(UnifiedNetwork, TrioThreadMixin, AbstractNetwork):
	"""
	Wrapper for the legacy Selenium BiDi Network instance.

	Allows interception of network requests, adding authentication handlers,
	and managing request callbacks.
	"""
	
	def __init__(
			self,
			selenium_network: legacyNetwork,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> None:
		"""
		Initializes the Network wrapper.

		Args:
			selenium_network (legacyNetwork): The legacy Selenium Network instance to wrap.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.
		"""
		
		UnifiedNetwork.__init__(self, selenium_network=selenium_network)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def add_auth_handler(self, username: str, password: str) -> int:
		return await self.sync_to_trio(sync_function=self._add_auth_handler_impl)(username=username, password=password)
	
	async def add_request_handler(
			self,
			event: str,
			callback: Callable,
			url_patterns: Optional[List[str]] = None,
			contexts: Optional[List[str]] = None,
	) -> int:
		return await self.sync_to_trio(sync_function=self._add_request_handler_impl)(
				event=event,
				callback=callback,
				url_patterns=url_patterns,
				contexts=contexts
		)
	
	async def clear_request_handlers(self) -> None:
		await self.sync_to_trio(sync_function=self._clear_request_handlers_impl)()
	
	@classmethod
	def from_legacy(
			cls,
			legacy_object: NETWORK_TYPEHINT,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> Self:
		"""
		Creates an instance from a legacy Selenium Network object.

		This factory method is used to wrap an existing Selenium Network
		instance into the new interface.

		Args:
			legacy_object (NETWORK_TYPEHINT): The legacy Selenium Network instance or its wrapper.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.

		Returns:
			Self: A new instance of a class implementing Network.
		"""
		
		legacy_network_obj = get_legacy_instance(instance=legacy_object)
		
		if not isinstance(legacy_network_obj, legacyNetwork):
			raise CannotConvertTypeError(from_=legacyNetwork, to_=legacy_object)
		
		return cls(selenium_network=legacy_network_obj, lock=lock, limiter=limiter)
	
	@property
	def legacy(self) -> legacyNetwork:
		return self._legacy_impl
	
	async def remove_auth_handler(self, callback_id: int) -> None:
		await self.sync_to_trio(sync_function=self._remove_auth_handler_impl)(callback_id=callback_id)
	
	async def remove_request_handler(self, event: str, callback_id: int) -> None:
		await self.sync_to_trio(sync_function=self._remove_request_handler_impl)(event=event, callback_id=callback_id)
