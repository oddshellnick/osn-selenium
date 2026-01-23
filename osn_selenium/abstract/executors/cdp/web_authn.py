from abc import ABC, abstractmethod
from typing import (
	Any,
	Dict,
	List,
	Optional
)


__all__ = ["AbstractWebAuthnCDPExecutor"]


class AbstractWebAuthnCDPExecutor(ABC):
	@abstractmethod
	def add_credential(self, authenticator_id: str, credential: Dict[str, Any]) -> None:
		...
	
	@abstractmethod
	def add_virtual_authenticator(self, options: Dict[str, Any]) -> str:
		...
	
	@abstractmethod
	def clear_credentials(self, authenticator_id: str) -> None:
		...
	
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def enable(self, enable_ui: Optional[bool] = None) -> None:
		...
	
	@abstractmethod
	def get_credential(self, authenticator_id: str, credential_id: str) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def get_credentials(self, authenticator_id: str) -> List[Dict[str, Any]]:
		...
	
	@abstractmethod
	def remove_credential(self, authenticator_id: str, credential_id: str) -> None:
		...
	
	@abstractmethod
	def remove_virtual_authenticator(self, authenticator_id: str) -> None:
		...
	
	@abstractmethod
	def set_automatic_presence_simulation(self, authenticator_id: str, enabled: bool) -> None:
		...
	
	@abstractmethod
	def set_credential_properties(
			self,
			authenticator_id: str,
			credential_id: str,
			backup_eligibility: Optional[bool] = None,
			backup_state: Optional[bool] = None
	) -> None:
		...
	
	@abstractmethod
	def set_response_override_bits(
			self,
			authenticator_id: str,
			is_bogus_signature: Optional[bool] = None,
			is_bad_uv: Optional[bool] = None,
			is_bad_up: Optional[bool] = None
	) -> None:
		...
	
	@abstractmethod
	def set_user_verified(self, authenticator_id: str, is_user_verified: bool) -> None:
		...
