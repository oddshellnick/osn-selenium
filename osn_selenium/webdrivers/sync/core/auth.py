from osn_selenium.instances.sync.fedcm import FedCM
from typing import (
	Any,
	List,
	Optional,
	Union
)
from osn_selenium.instances.sync.dialog import Dialog
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.webdrivers.sync.core.base import CoreBaseMixin
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
	def add_credential(self, credential: Credential) -> None:
		self.driver.add_credential(credential=credential)
	
	@requires_driver
	def add_virtual_authenticator(self, options: VirtualAuthenticatorOptions) -> None:
		self.driver.add_virtual_authenticator(options=options)
	
	@requires_driver
	def fedcm(self) -> FedCM:
		legacy = self.driver.fedcm
		
		return FedCM(selenium_fedcm=legacy)
	
	@requires_driver
	def fedcm_dialog(
			self,
			timeout: int = 5,
			poll_frequency: float = 0.5,
			ignored_exceptions: Any = None,
	) -> Dialog:
		legacy = self.driver.fedcm_dialog(
				timeout=timeout,
				poll_frequency=poll_frequency,
				ignored_exceptions=ignored_exceptions,
		)
		
		return Dialog(selenium_dialog=legacy)
	
	@requires_driver
	def get_credentials(self) -> List[Credential]:
		return self.driver.get_credentials()
	
	@requires_driver
	def remove_all_credentials(self) -> None:
		self.driver.remove_all_credentials()
	
	@requires_driver
	def remove_credential(self, credential_id: Union[str, bytearray]) -> None:
		self.driver.remove_credential(credential_id=credential_id)
	
	@requires_driver
	def remove_virtual_authenticator(self) -> None:
		self.driver.remove_virtual_authenticator()
	
	@requires_driver
	def set_user_verified(self, verified: bool) -> None:
		self.driver.set_user_verified(verified=verified)
	
	@requires_driver
	def supports_fedcm(self) -> bool:
		return self.driver.supports_fedcm
	
	@requires_driver
	def virtual_authenticator_id(self) -> Optional[str]:
		return self.driver.virtual_authenticator_id
