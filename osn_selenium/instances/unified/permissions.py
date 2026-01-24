from typing import (
	Any,
	Dict,
	Optional,
	Union
)
from osn_selenium.exceptions.instance import NotExpectedTypeError
from selenium.webdriver.common.bidi.permissions import (
	PermissionDescriptor,
	Permissions as legacyPermissions
)


__all__ = ["UnifiedPermissions"]


class UnifiedPermissions:
	def __init__(self, selenium_permissions: legacyPermissions):
		if not isinstance(selenium_permissions, legacyPermissions):
			raise NotExpectedTypeError(
					expected_type=legacyPermissions,
					received_instance=selenium_permissions
			)
		
		self._selenium_permissions = selenium_permissions
	
	@property
	def _legacy_impl(self) -> legacyPermissions:
		return self._selenium_permissions
	
	def _set_permission_impl(
			self,
			descriptor: Union[Dict[str, Any], PermissionDescriptor],
			state: str,
			origin: str,
			user_context: Optional[str] = None,
	) -> None:
		self._legacy_impl.set_permission(
				descriptor=descriptor,
				state=state,
				origin=origin,
				user_context=user_context
		)
