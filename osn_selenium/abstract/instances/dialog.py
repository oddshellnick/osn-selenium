from abc import ABC, abstractmethod
from typing import Optional, Sequence
from selenium.webdriver.common.fedcm.account import Account
from selenium.webdriver.common.fedcm.dialog import (
	Dialog as legacyDialog
)


__all__ = ["AbstractDialog"]


class AbstractDialog(ABC):
	"""
	Abstract base class for a FedCM (Federated Credential Management) dialog.

	Defines the interface for interacting with a FedCM dialog, such as
	retrieving accounts, selecting an account, and dismissing or accepting the dialog.
	"""
	
	@abstractmethod
	def accept(self) -> None:
		"""
		Accepts the dialog.
		"""
		
		...
	
	@abstractmethod
	def dismiss(self) -> None:
		"""
		Dismisses the dialog.
		"""
		
		...
	
	@abstractmethod
	def get_accounts(self) -> Sequence[Account]:
		"""
		Gets the list of accounts displayed in the dialog.

		Returns:
			Sequence[Account]: A sequence of Account objects.
		"""
		
		...
	
	@property
	@abstractmethod
	def legacy(self) -> legacyDialog:
		"""
		Returns the underlying legacy Selenium Dialog instance.

		This provides a way to access the original Selenium object for operations
		not covered by this abstract interface.

		Returns:
			legacyDialog: The legacy Selenium Dialog object.
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
		The subtitle of the dialog.

		Returns:
			Optional[str]: The dialog subtitle, or None if not available.
		"""
		
		...
	
	@property
	@abstractmethod
	def title(self) -> str:
		"""
		The title of the dialog.

		Returns:
			str: The dialog title.
		"""
		
		...
	
	@property
	@abstractmethod
	def type(self) -> Optional[str]:
		"""
		The type of the dialog.

		Returns:
			Optional[str]: The dialog type, or None if not available.
		"""
		
		...
