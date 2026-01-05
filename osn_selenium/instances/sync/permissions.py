from typing import (
	Any,
	Dict,
	Optional,
	Self,
	Union
)

from osn_selenium.instances.errors import TypesConvertError, ExpectedTypeError
from osn_selenium.instances.types import PERMISSIONS_TYPEHINT
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.abstract.instances.permissions import AbstractPermissions
from selenium.webdriver.common.bidi.permissions import (
	PermissionDescriptor,
	Permissions as legacyPermissions
)


class Permissions(AbstractPermissions):
	def __init__(self, selenium_permissions: legacyPermissions) -> None:
		if not isinstance(selenium_permissions, legacyPermissions):
			raise ExpectedTypeError(expected_class=legacyPermissions, received_instance=selenium_permissions)
		
		self._selenium_permissions = selenium_permissions
	
	@classmethod
	def from_legacy(cls, selenium_permissions: PERMISSIONS_TYPEHINT) -> Self:
		"""
		Creates an instance from a legacy Selenium Permissions object.

		This factory method is used to wrap an existing Selenium Permissions
		instance into the new interface.

		Args:
			selenium_permissions (PERMISSIONS_TYPEHINT): The legacy Selenium Permissions instance or its wrapper.

		Returns:
			Self: A new instance of a class implementing Permissions.
		"""

		legacy_permissions_obj = get_legacy_instance(selenium_permissions)
		
		if not isinstance(legacy_permissions_obj, legacyPermissions):
			raise TypesConvertError(from_=legacyPermissions, to_=selenium_permissions)
		
		return cls(selenium_permissions=legacy_permissions_obj)
	
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
