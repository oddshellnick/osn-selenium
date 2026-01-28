from osn_selenium.trio_threads_mixin import TrioThreadMixin
from typing import (
	Any,
	List,
	Optional,
	Union
)
from osn_selenium.instances.trio_threads.fedcm import FedCM
from osn_selenium.instances.trio_threads.dialog import Dialog
from osn_selenium.webdrivers.unified.core.auth import UnifiedCoreAuthMixin
from osn_selenium.abstract.webdriver.core.auth import (
	AbstractCoreAuthMixin
)
from osn_selenium.instances.convert import (
	get_trio_thread_instance_wrapper
)
from selenium.webdriver.common.virtual_authenticator import (
	Credential,
	VirtualAuthenticatorOptions
)


__all__ = ["CoreAuthMixin"]


class CoreAuthMixin(UnifiedCoreAuthMixin, TrioThreadMixin, AbstractCoreAuthMixin):
	"""
	Mixin handling authentication and credential management for Core WebDrivers.

	Provides interfaces for adding/removing credentials, managing virtual
	authenticators, and handling Federated Credential Management (FedCM) dialogs.
	"""
	
	async def add_credential(self, credential: Credential) -> None:
		await self.sync_to_trio(sync_function=self._add_credential_impl)(credential=credential)
	
	async def add_virtual_authenticator(self, options: VirtualAuthenticatorOptions) -> None:
		await self.sync_to_trio(sync_function=self._add_virtual_authenticator_impl)(options=options)
	
	async def fedcm(self) -> FedCM:
		legacy = await self.sync_to_trio(sync_function=self._fedcm_impl)()
		
		return get_trio_thread_instance_wrapper(
				wrapper_class=FedCM,
				legacy_object=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	async def fedcm_dialog(
			self,
			timeout: int = 5,
			poll_frequency: float = 0.5,
			ignored_exceptions: Any = None,
	) -> Dialog:
		legacy = await self.sync_to_trio(sync_function=self._fedcm_dialog_impl)(
				timeout=timeout,
				poll_frequency=poll_frequency,
				ignored_exceptions=ignored_exceptions,
		)
		
		return get_trio_thread_instance_wrapper(
				wrapper_class=Dialog,
				legacy_object=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	async def get_credentials(self) -> List[Credential]:
		return await self.sync_to_trio(sync_function=self._get_credentials_impl)()
	
	async def remove_all_credentials(self) -> None:
		await self.sync_to_trio(sync_function=self._remove_all_credentials_impl)()
	
	async def remove_credential(self, credential_id: Union[str, bytearray]) -> None:
		await self.sync_to_trio(sync_function=self._remove_credential_impl)(credential_id=credential_id)
	
	async def remove_virtual_authenticator(self) -> None:
		await self.sync_to_trio(sync_function=self._remove_virtual_authenticator_impl)()
	
	async def set_user_verified(self, verified: bool) -> None:
		await self.sync_to_trio(sync_function=self._set_user_verified_impl)(verified=verified)
	
	async def supports_fedcm(self) -> bool:
		return await self.sync_to_trio(sync_function=self._supports_fedcm_impl)()
	
	async def virtual_authenticator_id(self) -> Optional[str]:
		return await self.sync_to_trio(sync_function=self._virtual_authenticator_id_impl)()
