from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional
)
from osn_selenium.executors.unified.cdp.web_authn import (
	UnifiedWebAuthnCDPExecutor
)
from osn_selenium.abstract.executors.cdp.web_authn import (
	AbstractWebAuthnCDPExecutor
)


__all__ = ["WebAuthnCDPExecutor"]


class WebAuthnCDPExecutor(UnifiedWebAuthnCDPExecutor, AbstractWebAuthnCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedWebAuthnCDPExecutor.__init__(self, execute_function=execute_function)
	
	def add_credential(self, authenticator_id: str, credential: Dict[str, Any]) -> None:
		return self._add_credential_impl(authenticator_id=authenticator_id, credential=credential)
	
	def add_virtual_authenticator(self, options: Dict[str, Any]) -> str:
		return self._add_virtual_authenticator_impl(options=options)
	
	def clear_credentials(self, authenticator_id: str) -> None:
		return self._clear_credentials_impl(authenticator_id=authenticator_id)
	
	def disable(self) -> None:
		return self._disable_impl()
	
	def enable(self, enable_ui: Optional[bool] = None) -> None:
		return self._enable_impl(enable_ui=enable_ui)
	
	def get_credential(self, authenticator_id: str, credential_id: str) -> Dict[str, Any]:
		return self._get_credential_impl(authenticator_id=authenticator_id, credential_id=credential_id)
	
	def get_credentials(self, authenticator_id: str) -> List[Dict[str, Any]]:
		return self._get_credentials_impl(authenticator_id=authenticator_id)
	
	def remove_credential(self, authenticator_id: str, credential_id: str) -> None:
		return self._remove_credential_impl(authenticator_id=authenticator_id, credential_id=credential_id)
	
	def remove_virtual_authenticator(self, authenticator_id: str) -> None:
		return self._remove_virtual_authenticator_impl(authenticator_id=authenticator_id)
	
	def set_automatic_presence_simulation(self, authenticator_id: str, enabled: bool) -> None:
		return self._set_automatic_presence_simulation_impl(authenticator_id=authenticator_id, enabled=enabled)
	
	def set_credential_properties(
			self,
			authenticator_id: str,
			credential_id: str,
			backup_eligibility: Optional[bool] = None,
			backup_state: Optional[bool] = None
	) -> None:
		return self._set_credential_properties_impl(
				authenticator_id=authenticator_id,
				credential_id=credential_id,
				backup_eligibility=backup_eligibility,
				backup_state=backup_state
		)
	
	def set_response_override_bits(
			self,
			authenticator_id: str,
			is_bogus_signature: Optional[bool] = None,
			is_bad_uv: Optional[bool] = None,
			is_bad_up: Optional[bool] = None
	) -> None:
		return self._set_response_override_bits_impl(
				authenticator_id=authenticator_id,
				is_bogus_signature=is_bogus_signature,
				is_bad_uv=is_bad_uv,
				is_bad_up=is_bad_up
		)
	
	def set_user_verified(self, authenticator_id: str, is_user_verified: bool) -> None:
		return self._set_user_verified_impl(authenticator_id=authenticator_id, is_user_verified=is_user_verified)
