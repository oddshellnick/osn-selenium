import trio
from osn_selenium.trio_base_mixin import _TrioThreadMixin
from typing import (
	Any,
	Dict,
	Optional,
	Self,
	Union
)
from osn_selenium.instances.types import PERMISSIONS_TYPEHINT
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.abstract.instances.permissions import AbstractPermissions
from selenium.webdriver.common.bidi.permissions import (
	PermissionDescriptor,
	Permissions as legacyPermissions
)


class Permissions(_TrioThreadMixin, AbstractPermissions):
	def __init__(
			self,
			selenium_permissions: legacyPermissions,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> None:
		super().__init__(lock=lock, limiter=limiter)
		
		if not isinstance(selenium_permissions, legacyPermissions):
			raise TypeError(
					f"Expected {type(legacyPermissions)}, got {type(selenium_permissions)}"
			)
		
		self._selenium_permissions = selenium_permissions
	
	@classmethod
	def from_legacy(
			cls,
			selenium_permissions: PERMISSIONS_TYPEHINT,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> Self:
		"""
		Creates an instance from a legacy Selenium Permissions object.

		This factory method is used to wrap an existing Selenium Permissions
		instance into the new interface.

		Args:
			selenium_permissions (PERMISSIONS_TYPEHINT): The legacy Selenium Permissions instance or its wrapper.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.

		Returns:
			Self: A new instance of a class implementing Permissions.
		"""
		
		legacy_permissions_obj = get_legacy_instance(selenium_permissions)
		
		if not isinstance(legacy_permissions_obj, legacyPermissions):
			raise TypeError(
					f"Could not convert input to {type(legacyPermissions)}: {type(selenium_permissions)}"
			)
		
		return cls(
				selenium_permissions=legacy_permissions_obj,
				lock=lock,
				limiter=limiter
		)
	
	@property
	def legacy(self) -> legacyPermissions:
		return self._selenium_permissions
	
	async def set_permission(
			self,
			descriptor: Union[Dict[str, Any], PermissionDescriptor],
			state: str,
			origin: str,
			user_context: Optional[str] = None,
	) -> None:
		await self._wrap_to_trio(
				self.legacy.set_permission,
				descriptor=descriptor,
				state=state,
				origin=origin,
				user_context=user_context
		)
