from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	List,
	Optional
)
from osn_selenium.abstract.executors.cdp.web_authn import (
	AbstractWebAuthnCDPExecutor
)


class WebAuthnCDPExecutor(AbstractWebAuthnCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def add_credential(self, authenticator_id: str, credential: Any) -> None:
		return await self._execute_function("WebAuthn.addCredential", locals())
	
	async def add_virtual_authenticator(self, options: Any) -> str:
		return await self._execute_function("WebAuthn.addVirtualAuthenticator", locals())
	
	async def clear_credentials(self, authenticator_id: str) -> None:
		return await self._execute_function("WebAuthn.clearCredentials", locals())
	
	async def disable(self) -> None:
		return await self._execute_function("WebAuthn.disable", locals())
	
	async def enable(self, enable_ui: Optional[bool] = None) -> None:
		return await self._execute_function("WebAuthn.enable", locals())
	
	async def get_credential(self, authenticator_id: str, credential_id: str) -> Any:
		return await self._execute_function("WebAuthn.getCredential", locals())
	
	async def get_credentials(self, authenticator_id: str) -> List[Any]:
		return await self._execute_function("WebAuthn.getCredentials", locals())
	
	async def remove_credential(self, authenticator_id: str, credential_id: str) -> None:
		return await self._execute_function("WebAuthn.removeCredential", locals())
	
	async def remove_virtual_authenticator(self, authenticator_id: str) -> None:
		return await self._execute_function("WebAuthn.removeVirtualAuthenticator", locals())
	
	async def set_automatic_presence_simulation(self, authenticator_id: str, enabled: bool) -> None:
		return await self._execute_function("WebAuthn.setAutomaticPresenceSimulation", locals())
	
	async def set_credential_properties(
			self,
			authenticator_id: str,
			credential_id: str,
			backup_eligibility: Optional[bool] = None,
			backup_state: Optional[bool] = None
	) -> None:
		return await self._execute_function("WebAuthn.setCredentialProperties", locals())
	
	async def set_response_override_bits(
			self,
			authenticator_id: str,
			is_bogus_signature: Optional[bool] = None,
			is_bad_uv: Optional[bool] = None,
			is_bad_up: Optional[bool] = None
	) -> None:
		return await self._execute_function("WebAuthn.setResponseOverrideBits", locals())
	
	async def set_user_verified(self, authenticator_id: str, is_user_verified: bool) -> None:
		return await self._execute_function("WebAuthn.setUserVerified", locals())
