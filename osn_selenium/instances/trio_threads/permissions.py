import trio
from typing import (
	Any,
	Dict,
	Optional,
	Self,
	Union
)
from osn_selenium.abstract.instances.permissions import AbstractPermissions
from osn_selenium.trio_base_mixin import _TrioThreadMixin
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
		
		self._selenium_permissions = selenium_permissions
	
	@classmethod
	def from_legacy(
			cls,
			selenium_permissions: legacyPermissions,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> Self:
		"""
		Creates an instance from a legacy Selenium Permissions object.

		This factory method is used to wrap an existing Selenium Permissions
		instance into the new interface.

		Args:
			selenium_permissions (legacyPermissions): The legacy Selenium Permissions instance.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.

		Returns:
			Self: A new instance of a class implementing Permissions.
		"""
		
		return cls(selenium_permissions=selenium_permissions, lock=lock, limiter=limiter)
	
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
