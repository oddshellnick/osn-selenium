from typing import Optional, Union
from abc import ABC, abstractmethod
from selenium.webdriver.common.bidi.permissions import (
	PermissionDescriptor,
	Permissions as legacyPermissions
)


__all__ = ["AbstractPermissions"]


class AbstractPermissions(ABC):
	"""
	Abstract base class for managing browser permissions.

	Defines the interface for setting permission states for various APIs.
	"""
	
	@property
	@abstractmethod
	def legacy(self) -> legacyPermissions:
		"""
		Returns the underlying legacy Selenium Permissions instance.

		This provides a way to access the original Selenium object for operations
		not covered by this abstract interface.

		Returns:
			legacyPermissions: The legacy Selenium Permissions object.
		"""
		
		...
	
	@abstractmethod
	def set_permission(
			self,
			descriptor: Union[str, PermissionDescriptor],
			state: str,
			origin: str,
			user_context: Optional[str] = None,
	) -> None:
		"""
		Sets the state of a permission.

		Args:
			descriptor (Union[str, PermissionDescriptor]): The permission descriptor.
			state (str): The desired state of the permission (e.g., 'granted', 'denied').
			origin (str): The origin for which to set the permission.
			user_context (Optional[str]): The user context ID.
		"""
		
		...
