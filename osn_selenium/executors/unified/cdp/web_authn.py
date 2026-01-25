from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional
)


__all__ = ["UnifiedWebAuthnCDPExecutor"]


class UnifiedWebAuthnCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _add_credential_impl(self, authenticator_id: str, credential: Dict[str, Any]) -> None:
		return self._execute_function(
				"WebAuthn.addCredential",
				{"authenticator_id": authenticator_id, "credential": credential}
		)
	
	def _add_virtual_authenticator_impl(self, options: Dict[str, Any]) -> str:
		return self._execute_function("WebAuthn.addVirtualAuthenticator", {"options": options})
	
	def _clear_credentials_impl(self, authenticator_id: str) -> None:
		return self._execute_function("WebAuthn.clearCredentials", {"authenticator_id": authenticator_id})
	
	def _disable_impl(self) -> None:
		return self._execute_function("WebAuthn.disable", {})
	
	def _enable_impl(self, enable_ui: Optional[bool] = None) -> None:
		return self._execute_function("WebAuthn.enable", {"enable_ui": enable_ui})
	
	def _get_credential_impl(self, authenticator_id: str, credential_id: str) -> Dict[str, Any]:
		return self._execute_function(
				"WebAuthn.getCredential",
				{"authenticator_id": authenticator_id, "credential_id": credential_id}
		)
	
	def _get_credentials_impl(self, authenticator_id: str) -> List[Dict[str, Any]]:
		return self._execute_function("WebAuthn.getCredentials", {"authenticator_id": authenticator_id})
	
	def _remove_credential_impl(self, authenticator_id: str, credential_id: str) -> None:
		return self._execute_function(
				"WebAuthn.removeCredential",
				{"authenticator_id": authenticator_id, "credential_id": credential_id}
		)
	
	def _remove_virtual_authenticator_impl(self, authenticator_id: str) -> None:
		return self._execute_function(
				"WebAuthn.removeVirtualAuthenticator",
				{"authenticator_id": authenticator_id}
		)
	
	def _set_automatic_presence_simulation_impl(self, authenticator_id: str, enabled: bool) -> None:
		return self._execute_function(
				"WebAuthn.setAutomaticPresenceSimulation",
				{"authenticator_id": authenticator_id, "enabled": enabled}
		)
	
	def _set_credential_properties_impl(
			self,
			authenticator_id: str,
			credential_id: str,
			backup_eligibility: Optional[bool] = None,
			backup_state: Optional[bool] = None
	) -> None:
		return self._execute_function(
				"WebAuthn.setCredentialProperties",
				{
					"authenticator_id": authenticator_id,
					"credential_id": credential_id,
					"backup_eligibility": backup_eligibility,
					"backup_state": backup_state
				}
		)
	
	def _set_response_override_bits_impl(
			self,
			authenticator_id: str,
			is_bogus_signature: Optional[bool] = None,
			is_bad_uv: Optional[bool] = None,
			is_bad_up: Optional[bool] = None
	) -> None:
		return self._execute_function(
				"WebAuthn.setResponseOverrideBits",
				{
					"authenticator_id": authenticator_id,
					"is_bogus_signature": is_bogus_signature,
					"is_bad_uv": is_bad_uv,
					"is_bad_up": is_bad_up
				}
		)
	
	def _set_user_verified_impl(self, authenticator_id: str, is_user_verified: bool) -> None:
		return self._execute_function(
				"WebAuthn.setUserVerified",
				{
					"authenticator_id": authenticator_id,
					"is_user_verified": is_user_verified
				}
		)
