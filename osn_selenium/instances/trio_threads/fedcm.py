import trio
from typing import (
	Dict,
	List,
	Optional,
	Self
)
from osn_selenium.abstract.instances.fedcm import AbstractFedCM
from selenium.webdriver.remote.fedcm import FedCM as legacyFedCM
from osn_selenium.trio_base_mixin import _TrioThreadMixin


class FedCM(_TrioThreadMixin, AbstractFedCM):
	def __init__(
			self,
			selenium_fedcm: legacyFedCM,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> None:
		super().__init__(lock=lock, limiter=limiter)
		
		self._selenium_fedcm = selenium_fedcm
	
	async def accept(self) -> None:
		await self._wrap_to_trio(self.legacy.accept)
	
	async def account_list(self) -> List[Dict]:
		return await self._wrap_to_trio(lambda: self.legacy.account_list)
	
	async def dialog_type(self) -> str:
		return await self._wrap_to_trio(lambda: self.legacy.dialog_type)
	
	async def disable_delay(self) -> None:
		await self._wrap_to_trio(self.legacy.disable_delay)
	
	async def dismiss(self) -> None:
		await self._wrap_to_trio(self.legacy.dismiss)
	
	async def enable_delay(self) -> None:
		await self._wrap_to_trio(self.legacy.enable_delay)
	
	@classmethod
	def from_legacy(
			cls,
			selenium_fedcm: legacyFedCM,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> Self:
		"""
		Creates an instance from a legacy Selenium FedCM object.

		This factory method is used to wrap an existing Selenium FedCM
		instance into the new interface.

		Args:
			selenium_fedcm (legacyFedCM): The legacy Selenium FedCM instance.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.

		Returns:
			Self: A new instance of a class implementing FedCM.
		"""
		
		return cls(selenium_fedcm=selenium_fedcm, lock=lock, limiter=limiter)
	
	@property
	def legacy(self) -> legacyFedCM:
		return self._selenium_fedcm
	
	async def reset_cooldown(self) -> None:
		await self._wrap_to_trio(self.legacy.reset_cooldown)
	
	async def select_account(self, index: int) -> None:
		await self._wrap_to_trio(self.legacy.select_account, index)
	
	async def subtitle(self) -> Optional[str]:
		return await self._wrap_to_trio(lambda: self.legacy.subtitle)
	
	async def title(self) -> str:
		return await self._wrap_to_trio(lambda: self.legacy.title)
