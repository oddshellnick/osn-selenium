from typing import (
	Any,
	Dict,
	Optional,
	Self,
	Union
)
from osn_selenium.abstract.instances.permissions import AbstractPermissions
from selenium.webdriver.common.bidi.permissions import (
	PermissionDescriptor,
	Permissions as legacyPermissions
)


class Permissions(AbstractPermissions):
	def __init__(self, selenium_permissions: legacyPermissions,) -> None:
		self._selenium_permissions = selenium_permissions
	
	@classmethod
	def from_legacy(cls, selenium_permissions: legacyPermissions,) -> Self:
		"""
		Creates an instance from a legacy Selenium Permissions object.

		This factory method is used to wrap an existing Selenium Permissions
		instance into the new interface.

		Args:
			selenium_permissions (legacyPermissions): The legacy Selenium Permissions instance.

		Returns:
			Self: A new instance of a class implementing Permissions.
		"""
		
		return cls(selenium_permissions=selenium_permissions)
	
	@property
	def legacy(self) -> legacyPermissions:
		return self._selenium_permissions
	
	def set_permission(
			self,
			descriptor: Union[Dict[str, Any], PermissionDescriptor],
			state: str,
			origin: str,
			user_context: Optional[str] = None,
	) -> None:
		self.legacy.set_permission(
				descriptor=descriptor,
				state=state,
				origin=origin,
				user_context=user_context
		)
