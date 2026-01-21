import trio
from typing import List, Self, Union
from osn_selenium.base_mixin import TrioThreadMixin
from osn_selenium.instances.types import MOBILE_TYPEHINT
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.abstract.instances.mobile import AbstractMobile
from osn_selenium.instances.errors import (
	ExpectedTypeError,
	TypesConvertError
)
from selenium.webdriver.remote.mobile import (
	Mobile as legacyMobile,
	_ConnectionType
)


class Mobile(TrioThreadMixin, AbstractMobile):
	"""
	Wrapper for the legacy Selenium Mobile instance.

	Manages network connection types and context settings (e.g., native app vs web view)
	for mobile emulation.
	"""
	
	def __init__(
			self,
			selenium_mobile: legacyMobile,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> None:
		"""
		Initializes the Mobile wrapper.

		Args:
			selenium_mobile (legacyMobile): The legacy Selenium Mobile instance to wrap.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.
		"""
		
		super().__init__(lock=lock, limiter=limiter)
		
		if not isinstance(selenium_mobile, legacyMobile):
			raise ExpectedTypeError(expected_class=legacyMobile, received_instance=selenium_mobile)
		
		self._selenium_mobile = selenium_mobile
	
	async def context(self) -> str:
		return await self._sync_to_trio(lambda: self.legacy.context)
	
	async def contexts(self) -> List[str]:
		return await self._sync_to_trio(lambda: self.legacy.contexts)
	
	@classmethod
	def from_legacy(
			cls,
			selenium_mobile: MOBILE_TYPEHINT,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> Self:
		"""
		Creates an instance from a legacy Selenium Mobile object.

		This factory method is used to wrap an existing Selenium Mobile
		instance into the new interface.

		Args:
			selenium_mobile (MOBILE_TYPEHINT): The legacy Selenium Mobile instance or its wrapper.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.

		Returns:
			Self: A new instance of a class implementing Mobile.
		"""
		
		legacy_mobile_obj = get_legacy_instance(selenium_mobile)
		
		if not isinstance(legacy_mobile_obj, legacyMobile):
			raise TypesConvertError(from_=legacyMobile, to_=selenium_mobile)
		
		return cls(selenium_mobile=legacy_mobile_obj, lock=lock, limiter=limiter)
	
	async def network_connection(self) -> _ConnectionType:
		return await self._sync_to_trio(lambda: self.legacy.network_connection)
	
	@property
	def legacy(self) -> legacyMobile:
		return self._selenium_mobile
	
	async def set_context(self, new_context: str) -> None:
		await self._sync_to_trio(lambda: setattr(self.legacy, "context", new_context))
	
	async def set_network_connection(self, network: Union[int, _ConnectionType]) -> _ConnectionType:
		return await self._sync_to_trio(self.legacy.set_network_connection, network)
