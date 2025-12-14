from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional
)
from osn_selenium.abstract.executors.cdp.web_authn import (
	AbstractWebAuthnCDPExecutor
)


class WebAuthnCDPExecutor(AbstractWebAuthnCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def add_credential(self, authenticator_id: str, credential: Any) -> None:
		return self._execute_function("WebAuthn.addCredential", locals())
	
	def add_virtual_authenticator(self, options: Any) -> str:
		return self._execute_function("WebAuthn.addVirtualAuthenticator", locals())
	
	def clear_credentials(self, authenticator_id: str) -> None:
		return self._execute_function("WebAuthn.clearCredentials", locals())
	
	def disable(self) -> None:
		return self._execute_function("WebAuthn.disable", locals())
	
	def enable(self, enable_ui: Optional[bool] = None) -> None:
		return self._execute_function("WebAuthn.enable", locals())
	
	def get_credential(self, authenticator_id: str, credential_id: str) -> Any:
		return self._execute_function("WebAuthn.getCredential", locals())
	
	def get_credentials(self, authenticator_id: str) -> List[Any]:
		return self._execute_function("WebAuthn.getCredentials", locals())
	
	def remove_credential(self, authenticator_id: str, credential_id: str) -> None:
		return self._execute_function("WebAuthn.removeCredential", locals())
	
	def remove_virtual_authenticator(self, authenticator_id: str) -> None:
		return self._execute_function("WebAuthn.removeVirtualAuthenticator", locals())
	
	def set_automatic_presence_simulation(self, authenticator_id: str, enabled: bool) -> None:
		return self._execute_function("WebAuthn.setAutomaticPresenceSimulation", locals())
	
	def set_credential_properties(
			self,
			authenticator_id: str,
			credential_id: str,
			backup_eligibility: Optional[bool] = None,
			backup_state: Optional[bool] = None
	) -> None:
		return self._execute_function("WebAuthn.setCredentialProperties", locals())
	
	def set_response_override_bits(
			self,
			authenticator_id: str,
			is_bogus_signature: Optional[bool] = None,
			is_bad_uv: Optional[bool] = None,
			is_bad_up: Optional[bool] = None
	) -> None:
		return self._execute_function("WebAuthn.setResponseOverrideBits", locals())
	
	def set_user_verified(self, authenticator_id: str, is_user_verified: bool) -> None:
		return self._execute_function("WebAuthn.setUserVerified", locals())
