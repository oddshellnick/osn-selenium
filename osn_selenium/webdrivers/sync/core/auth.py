from osn_selenium.instances.sync.fedcm import FedCM
from typing import (
	Any,
	List,
	Optional,
	Union
)
from osn_selenium.instances.sync.dialog import Dialog
from osn_selenium.instances.convert import (
	get_sync_instance_wrapper
)
from osn_selenium.webdrivers.unified.core.auth import UnifiedCoreAuthMixin
from osn_selenium.abstract.webdriver.core.auth import (
	AbstractCoreAuthMixin
)
from selenium.webdriver.common.virtual_authenticator import (
	Credential,
	VirtualAuthenticatorOptions
)


__all__ = ["CoreAuthMixin"]


class CoreAuthMixin(UnifiedCoreAuthMixin, AbstractCoreAuthMixin):
	"""
	Mixin handling authentication and credential management for Core WebDrivers.

	Provides interfaces for adding/removing credentials, managing virtual
	authenticators, and handling Federated Credential Management (FedCM) dialogs.
	"""
	
	def add_credential(self, credential: Credential) -> None:
		self._add_credential_impl(credential=credential)
	
	def add_virtual_authenticator(self, options: VirtualAuthenticatorOptions) -> None:
		self._add_virtual_authenticator_impl(options=options)
	
	def fedcm(self) -> FedCM:
		legacy = self._fedcm_impl()
		
		return get_sync_instance_wrapper(wrapper_class=FedCM, legacy_object=legacy)
	
	def fedcm_dialog(
			self,
			timeout: int = 5,
			poll_frequency: float = 0.5,
			ignored_exceptions: Any = None,
	) -> Dialog:
		legacy = self._fedcm_dialog_impl(
				timeout=timeout,
				poll_frequency=poll_frequency,
				ignored_exceptions=ignored_exceptions,
		)
		
		return get_sync_instance_wrapper(wrapper_class=Dialog, legacy_object=legacy)
	
	def get_credentials(self) -> List[Credential]:
		return self._get_credentials_impl()
	
	def remove_all_credentials(self) -> None:
		self._remove_all_credentials_impl()
	
	def remove_credential(self, credential_id: Union[str, bytearray]) -> None:
		self._remove_credential_impl(credential_id=credential_id)
	
	def remove_virtual_authenticator(self) -> None:
		self._remove_virtual_authenticator_impl()
	
	def set_user_verified(self, verified: bool) -> None:
		self._set_user_verified_impl(verified=verified)
	
	def supports_fedcm(self) -> bool:
		return self._supports_fedcm_impl()
	
	def virtual_authenticator_id(self) -> Optional[str]:
		return self._virtual_authenticator_id_impl()
