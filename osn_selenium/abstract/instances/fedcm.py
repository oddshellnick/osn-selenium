from abc import ABC, abstractmethod
from typing import (
	Mapping,
	Optional,
	Sequence
)
from selenium.webdriver.remote.fedcm import FedCM as legacyFedCM


__all__ = ["AbstractFedCM"]


class AbstractFedCM(ABC):
	"""
	Abstract base class for Federated Credential Management (FedCM) API.

	Defines the interface for interacting with the FedCM dialog, managing accounts,
	and controlling cooldown periods.
	"""
	
	@abstractmethod
	def accept(self) -> None:
		"""
		Accepts the FedCM dialog, typically confirming the selected account.
		"""
		
		...
	
	@property
	@abstractmethod
	def account_list(self) -> Sequence[Mapping]:
		"""
		The list of accounts displayed in the FedCM dialog.

		Returns:
			Sequence[Mapping]: A sequence of dictionaries, each representing an account.
		"""
		
		...
	
	@property
	@abstractmethod
	def dialog_type(self) -> str:
		"""
		The type of the FedCM dialog.

		Returns:
			str: The dialog type (e.g., 'AccountChooser', 'AutoReauthn').
		"""
		
		...
	
	@abstractmethod
	def disable_delay(self) -> None:
		"""
		Disables the delay for FedCM operations.
		"""
		
		...
	
	@abstractmethod
	def dismiss(self) -> None:
		"""
		Dismisses the FedCM dialog.
		"""
		
		...
	
	@abstractmethod
	def enable_delay(self) -> None:
		"""
		Enables the delay for FedCM operations, useful for testing.
		"""
		
		...
	
	@property
	@abstractmethod
	def legacy(self) -> legacyFedCM:
		"""
		Returns the underlying legacy Selenium FedCM instance.

		This provides a way to access the original Selenium object for operations
		not covered by this abstract interface.

		Returns:
			legacyFedCM: The legacy Selenium FedCM object.
		"""
		
		...
	
	@abstractmethod
	def reset_cooldown(self) -> None:
		"""
		Resets the FedCM cooldown timer.
		"""
		
		...
	
	@abstractmethod
	def select_account(self, index: int) -> None:
		"""
		Selects an account from the list in the dialog.

		Args:
			index (int): The index of the account to select.
		"""
		
		...
	
	@property
	@abstractmethod
	def subtitle(self) -> Optional[str]:
		"""
		The subtitle of the FedCM dialog.

		Returns:
			Optional[str]: The dialog subtitle, or None if it doesn't exist.
		"""
		
		...
	
	@property
	@abstractmethod
	def title(self) -> str:
		"""
		The title of the FedCM dialog.

		Returns:
			str: The dialog title.
		"""
		
		...
