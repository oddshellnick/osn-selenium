import trio
from typing import List, Self, Union
from osn_selenium.abstract.instances.mobile import AbstractMobile
from osn_selenium.instances.trio_threads.base_mixin import _TrioThreadMixin
from selenium.webdriver.remote.mobile import (
	Mobile as legacyMobile,
	_ConnectionType
)


class Mobile(_TrioThreadMixin, AbstractMobile):
	def __init__(
			self,
			selenium_mobile: legacyMobile,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> None:
		super().__init__(lock=lock, limiter=limiter)
		
		self._selenium_mobile = selenium_mobile
	
	async def context(self) -> str:
		return await self._wrap_to_trio(lambda: self.legacy.context)
	
	async def contexts(self) -> List[str]:
		return await self._wrap_to_trio(lambda: self.legacy.contexts)
	
	@classmethod
	def from_legacy(
			cls,
			selenium_mobile: legacyMobile,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> Self:
		"""
		Creates an instance from a legacy Selenium Mobile object.

		This factory method is used to wrap an existing Selenium Mobile
		instance into the new interface.

		Args:
			selenium_mobile (legacyMobile): The legacy Selenium Mobile instance.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.

		Returns:
			Self: A new instance of a class implementing Mobile.
		"""
		
		return cls(selenium_mobile=selenium_mobile, lock=lock, limiter=limiter)
	
	async def network_connection(self) -> _ConnectionType:
		return await self._wrap_to_trio(lambda: self.legacy.network_connection)
	
	@property
	def legacy(self) -> legacyMobile:
		return self._selenium_mobile
	
	async def set_context(self, new_context: str) -> None:
		await self._wrap_to_trio(lambda: setattr(self.legacy, "context", new_context))
	
	async def set_network_connection(self, network: Union[int, _ConnectionType],) -> _ConnectionType:
		return await self._wrap_to_trio(self.legacy.set_network_connection, network)
