from typing import (
	Any,
	List,
	Optional,
	Union
)
from osn_selenium.webdrivers._decorators import requires_driver
from osn_selenium.webdrivers.unified.core.base import UnifiedCoreBaseMixin
from selenium.webdriver.common.virtual_authenticator import (
	Credential,
	VirtualAuthenticatorOptions
)


__all__ = ["UnifiedCoreAuthMixin"]


class UnifiedCoreAuthMixin(UnifiedCoreBaseMixin):
	@requires_driver
	def _add_credential_impl(self, credential: Credential) -> None:
		self._driver_impl.add_credential(credential=credential)
	
	@requires_driver
	def _add_virtual_authenticator_impl(self, options: VirtualAuthenticatorOptions) -> None:
		self._driver_impl.add_virtual_authenticator(options=options)
	
	@requires_driver
	def _fedcm_dialog_impl(
			self,
			timeout: int = 5,
			poll_frequency: float = 0.5,
			ignored_exceptions: Any = None,
	) -> Any:
		return self._driver_impl.fedcm_dialog(
				timeout=timeout,
				poll_frequency=poll_frequency,
				ignored_exceptions=ignored_exceptions,
		)
	
	@requires_driver
	def _fedcm_impl(self) -> Any:
		return self._driver_impl.fedcm
	
	@requires_driver
	def _get_credentials_impl(self) -> List[Credential]:
		return self._driver_impl.get_credentials()
	
	@requires_driver
	def _remove_all_credentials_impl(self) -> None:
		self._driver_impl.remove_all_credentials()
	
	@requires_driver
	def _remove_credential_impl(self, credential_id: Union[str, bytearray]) -> None:
		self._driver_impl.remove_credential(credential_id=credential_id)
	
	@requires_driver
	def _remove_virtual_authenticator_impl(self) -> None:
		self._driver_impl.remove_virtual_authenticator()
	
	@requires_driver
	def _set_user_verified_impl(self, verified: bool) -> None:
		self._driver_impl.set_user_verified(verified=verified)
	
	@requires_driver
	def _supports_fedcm_impl(self) -> bool:
		return self._driver_impl.supports_fedcm
	
	@requires_driver
	def _virtual_authenticator_id_impl(self) -> Optional[str]:
		return self._driver_impl.virtual_authenticator_id
