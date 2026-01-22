from typing import (
	Any,
	List,
	Optional,
	Union
)
from osn_selenium.instances.trio_threads.fedcm import FedCM
from osn_selenium.instances.trio_threads.dialog import Dialog
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.webdrivers.trio_threads.core.base import CoreBaseMixin
from osn_selenium.abstract.webdriver.core.auth import (
	AbstractCoreAuthMixin
)
from selenium.webdriver.common.virtual_authenticator import (
	Credential,
	VirtualAuthenticatorOptions
)


class CoreAuthMixin(CoreBaseMixin, AbstractCoreAuthMixin):
	"""
	Mixin handling authentication and credential management for Core WebDrivers.

	Provides interfaces for adding/removing credentials, managing virtual
	authenticators, and handling Federated Credential Management (FedCM) dialogs.
	"""
	
	@requires_driver
	async def add_credential(self, credential: Credential) -> None:
		await self.sync_to_trio(sync_function=self.driver.add_credential)(credential=credential)
	
	@requires_driver
	async def add_virtual_authenticator(self, options: VirtualAuthenticatorOptions) -> None:
		await self.sync_to_trio(sync_function=self.driver.add_virtual_authenticator)(options=options)
	
	@requires_driver
	async def fedcm(self) -> FedCM:
		legacy = await self.sync_to_trio(sync_function=lambda: self.driver.fedcm)()
		
		return FedCM(selenium_fedcm=legacy, lock=self._lock, limiter=self._capacity_limiter)
	
	@requires_driver
	async def fedcm_dialog(
			self,
			timeout: int = 5,
			poll_frequency: float = 0.5,
			ignored_exceptions: Any = None,
	) -> Dialog:
		legacy = await self.sync_to_trio(sync_function=self.driver.fedcm_dialog)(
				timeout=timeout,
				poll_frequency=poll_frequency,
				ignored_exceptions=ignored_exceptions,
		)
		
		return Dialog(
				selenium_dialog=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	@requires_driver
	async def get_credentials(self) -> List[Credential]:
		return await self.sync_to_trio(sync_function=self.driver.get_credentials)()
	
	@requires_driver
	async def remove_all_credentials(self) -> None:
		await self.sync_to_trio(sync_function=self.driver.remove_all_credentials)()
	
	@requires_driver
	async def remove_credential(self, credential_id: Union[str, bytearray]) -> None:
		await self.sync_to_trio(sync_function=self.driver.remove_credential)(credential_id=credential_id)
	
	@requires_driver
	async def remove_virtual_authenticator(self) -> None:
		await self.sync_to_trio(sync_function=self.driver.remove_virtual_authenticator)()
	
	@requires_driver
	async def set_user_verified(self, verified: bool) -> None:
		await self.sync_to_trio(sync_function=self.driver.set_user_verified)(verified=verified)
	
	@requires_driver
	async def supports_fedcm(self) -> bool:
		return await self.sync_to_trio(sync_function=lambda: self.driver.supports_fedcm)()
	
	@requires_driver
	async def virtual_authenticator_id(self) -> Optional[str]:
		return await self.sync_to_trio(sync_function=lambda: self.driver.virtual_authenticator_id)()
