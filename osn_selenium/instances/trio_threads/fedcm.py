import trio
from osn_selenium.trio_threads_mixin import TrioThreadMixin
from typing import (
	Dict,
	List,
	Optional,
	Self
)
from osn_selenium.instances._typehints import FEDCM_TYPEHINT
from osn_selenium.instances.unified.fedcm import UnifiedFedCM
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.abstract.instances.fedcm import AbstractFedCM
from selenium.webdriver.remote.fedcm import FedCM as legacyFedCM
from osn_selenium.exceptions.instance import (
	CannotConvertTypeError
)


__all__ = ["FedCM"]


class FedCM(UnifiedFedCM, TrioThreadMixin, AbstractFedCM):
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
		
		UnifiedFedCM.__init__(self, selenium_fedcm=selenium_fedcm)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def accept(self) -> None:
		await self.sync_to_trio(sync_function=self._accept_impl)()
	
	async def account_list(self) -> List[Dict]:
		return await self.sync_to_trio(sync_function=self._account_list_impl)()
	
	async def dialog_type(self) -> str:
		return await self.sync_to_trio(sync_function=self._dialog_type_impl)()
	
	async def disable_delay(self) -> None:
		await self.sync_to_trio(sync_function=self._disable_delay_impl)()
	
	async def dismiss(self) -> None:
		await self.sync_to_trio(sync_function=self._dismiss_impl)()
	
	async def enable_delay(self) -> None:
		await self.sync_to_trio(sync_function=self._enable_delay_impl)()
	
	@classmethod
	def from_legacy(
			cls,
			legacy_object: FEDCM_TYPEHINT,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> Self:
		"""
		Creates an instance from a legacy Selenium FedCM object.

		This factory method is used to wrap an existing Selenium FedCM
		instance into the new interface.

		Args:
			legacy_object (FEDCM_TYPEHINT): The legacy Selenium FedCM instance or its wrapper.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.

		Returns:
			Self: A new instance of a class implementing FedCM.
		"""
		
		legacy_fedcm_obj = get_legacy_instance(instance=legacy_object)
		
		if not isinstance(legacy_fedcm_obj, legacyFedCM):
			raise CannotConvertTypeError(from_=legacyFedCM, to_=legacy_object)
		
		return cls(selenium_fedcm=legacy_fedcm_obj, lock=lock, limiter=limiter)
	
	@property
	def legacy(self) -> legacyFedCM:
		return self._legacy_impl
	
	async def reset_cooldown(self) -> None:
		await self.sync_to_trio(sync_function=self._reset_cooldown_impl)()
	
	async def select_account(self, index: int) -> None:
		await self.sync_to_trio(sync_function=self._select_account_impl)(index=index)
	
	async def subtitle(self) -> Optional[str]:
		return await self.sync_to_trio(sync_function=self._subtitle_impl)()
	
	async def title(self) -> str:
		return await self.sync_to_trio(sync_function=self._title_impl)()
