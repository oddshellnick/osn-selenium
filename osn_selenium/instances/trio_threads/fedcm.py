import trio
from typing import (
	Dict,
	List,
	Optional,
	Self
)
from osn_selenium.instances.types import FEDCM_TYPEHINT
from osn_selenium.base_mixin import TrioThreadMixin
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.abstract.instances.fedcm import AbstractFedCM
from selenium.webdriver.remote.fedcm import FedCM as legacyFedCM
from osn_selenium.instances.errors import (
	ExpectedTypeError,
	TypesConvertError
)


class FedCM(TrioThreadMixin, AbstractFedCM):
	"""
	Wrapper for the legacy Selenium FedCM instance.

	Provides an interface for controlling the Federated Credential Management API,
	including dialog delays and cooldown resets.
	"""
	
	def __init__(
			self,
			selenium_fedcm: legacyFedCM,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> None:
		"""
		Initializes the FedCM wrapper.

		Args:
			selenium_fedcm (legacyFedCM): The legacy Selenium FedCM instance to wrap.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.
		"""
		
		super().__init__(lock=lock, limiter=limiter)
		
		if not isinstance(selenium_fedcm, legacyFedCM):
			raise ExpectedTypeError(expected_class=legacyFedCM, received_instance=selenium_fedcm)
		
		self._selenium_fedcm = selenium_fedcm
	
	async def accept(self) -> None:
		await self._sync_to_trio(self.legacy.accept)
	
	async def account_list(self) -> List[Dict]:
		return await self._sync_to_trio(lambda: self.legacy.account_list)
	
	async def dialog_type(self) -> str:
		return await self._sync_to_trio(lambda: self.legacy.dialog_type)
	
	async def disable_delay(self) -> None:
		await self._sync_to_trio(self.legacy.disable_delay)
	
	async def dismiss(self) -> None:
		await self._sync_to_trio(self.legacy.dismiss)
	
	async def enable_delay(self) -> None:
		await self._sync_to_trio(self.legacy.enable_delay)
	
	@classmethod
	def from_legacy(
			cls,
			selenium_fedcm: FEDCM_TYPEHINT,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> Self:
		"""
		Creates an instance from a legacy Selenium FedCM object.

		This factory method is used to wrap an existing Selenium FedCM
		instance into the new interface.

		Args:
			selenium_fedcm (FEDCM_TYPEHINT): The legacy Selenium FedCM instance or its wrapper.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.

		Returns:
			Self: A new instance of a class implementing FedCM.
		"""
		
		legacy_fedcm_obj = get_legacy_instance(selenium_fedcm)
		
		if not isinstance(legacy_fedcm_obj, legacyFedCM):
			raise TypesConvertError(from_=legacyFedCM, to_=selenium_fedcm)
		
		return cls(selenium_fedcm=legacy_fedcm_obj, lock=lock, limiter=limiter)
	
	@property
	def legacy(self) -> legacyFedCM:
		return self._selenium_fedcm
	
	async def reset_cooldown(self) -> None:
		await self._sync_to_trio(self.legacy.reset_cooldown)
	
	async def select_account(self, index: int) -> None:
		await self._sync_to_trio(self.legacy.select_account, index)
	
	async def subtitle(self) -> Optional[str]:
		return await self._sync_to_trio(lambda: self.legacy.subtitle)
	
	async def title(self) -> str:
		return await self._sync_to_trio(lambda: self.legacy.title)
