from abc import ABC, abstractmethod
from typing import (
	Any,
	List,
	Optional,
	Union
)
from osn_selenium.abstract.instances.fedcm import AbstractFedCM
from osn_selenium.abstract.instances.dialog import AbstractDialog
from selenium.webdriver.common.virtual_authenticator import (
	Credential,
	VirtualAuthenticatorOptions
)


__all__ = ["AbstractCoreAuthMixin"]


class AbstractCoreAuthMixin(ABC):
	"""Mixin responsible for credentials, virtual authenticators, and FedCM."""
	
	@abstractmethod
	def add_credential(self, credential: Credential) -> None:
		"""
		Adds a credential to the virtual authenticator.

		Args:
			credential (Credential): The credential to add.
		"""
		
		...
	
	@abstractmethod
	def add_virtual_authenticator(self, options: VirtualAuthenticatorOptions) -> None:
		"""
		Adds a virtual authenticator for testing web authentication.

		Args:
			options (VirtualAuthenticatorOptions): Configuration for the virtual authenticator.
		"""
		
		...
	
	@abstractmethod
	def fedcm(self) -> AbstractFedCM:
		"""
		Provides access to the FedCM (Federated Credential Management) interface.

		Returns:
			AbstractFedCM: An object for interacting with FedCM.
		"""
		
		...
	
	@abstractmethod
	def fedcm_dialog(
			self,
			timeout: int = 5,
			poll_frequency: float = 0.5,
			ignored_exceptions: Optional[Any] = None,
	) -> AbstractDialog:
		"""
		Waits for and returns a FedCM (Federated Credential Management) dialog.

		Args:
			timeout (int): The maximum time to wait for the dialog.
			poll_frequency (float): The frequency to check for the dialog's presence.
			ignored_exceptions (Optional[Any]): Exceptions to ignore during polling.

		Returns:
			AbstractDialog: The FedCM dialog object.
		"""
		
		...
	
	@abstractmethod
	def get_credentials(self) -> List[Credential]:
		"""
		Gets all credentials from the virtual authenticator.

		Returns:
			List[Credential]: A list of Credential objects.
		"""
		
		...
	
	@abstractmethod
	def remove_all_credentials(self) -> None:
		"""
		Removes all credentials from the virtual authenticator.
		"""
		
		...
	
	@abstractmethod
	def remove_credential(self, credential_id: Union[str, bytearray]) -> None:
		"""
		Removes a credential from the virtual authenticator.

		Args:
			credential_id (Union[str, bytearray]): The ID of the credential to remove.
		"""
		
		...
	
	@abstractmethod
	def remove_virtual_authenticator(self) -> None:
		"""
		Removes the currently active virtual authenticator.
		"""
		
		...
	
	@abstractmethod
	def set_user_verified(self, verified: bool) -> None:
		"""
		Sets the user-verified status for a virtual authenticator.

		Args:
			verified (bool): The new verification status.
		"""
		
		...
	
	@abstractmethod
	def supports_fedcm(self) -> bool:
		"""
		Checks if the browser supports Federated Credential Management (FedCM).

		Returns:
			bool: True if FedCM is supported, False otherwise.
		"""
		
		...
	
	@abstractmethod
	def virtual_authenticator_id(self) -> Optional[str]:
		"""
		Returns the ID of the currently active virtual authenticator.

		Returns:
			Optional[str]: The ID of the virtual authenticator, or None if not set.
		"""
		
		...
