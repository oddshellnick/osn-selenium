import trio
from osn_selenium.trio_threads_mixin import TrioThreadMixin
from typing import (
	Any,
	Dict,
	Optional,
	Self,
	Union
)
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.instances._typehints import PERMISSIONS_TYPEHINT
from osn_selenium.exceptions.instance import (
	CannotConvertTypeError
)
from osn_selenium.instances.unified.permissions import UnifiedPermissions
from osn_selenium.abstract.instances.permissions import AbstractPermissions
from selenium.webdriver.common.bidi.permissions import (
	PermissionDescriptor,
	Permissions as legacyPermissions
)


__all__ = ["Permissions"]


class Permissions(UnifiedPermissions, TrioThreadMixin, AbstractPermissions):
	"""
	Wrapper for the legacy Selenium Permissions instance.

	Provides methods to set and modify browser permissions (e.g., camera, microphone, geolocation)
	via the WebDriver BiDi protocol.
	"""
	
	def __init__(
			self,
			selenium_permissions: legacyPermissions,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> None:
		"""
		Initializes the Permissions wrapper.

		Args:
			selenium_permissions (legacyPermissions): The legacy Selenium Permissions instance to wrap.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.
		"""
		
		UnifiedPermissions.__init__(self, selenium_permissions=selenium_permissions)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	@classmethod
	def from_legacy(
			cls,
			legacy_object: PERMISSIONS_TYPEHINT,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> Self:
		"""
		Creates an instance from a legacy Selenium Permissions object.

		This factory method is used to wrap an existing Selenium Permissions
		instance into the new interface.

		Args:
			legacy_object (PERMISSIONS_TYPEHINT): The legacy Selenium Permissions instance or its wrapper.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.

		Returns:
			Self: A new instance of a class implementing Permissions.
		"""
		
		legacy_permissions_obj = get_legacy_instance(instance=legacy_object)
		
		if not isinstance(legacy_permissions_obj, legacyPermissions):
			raise CannotConvertTypeError(from_=legacyPermissions, to_=legacy_object)
		
		return cls(
				selenium_permissions=legacy_permissions_obj,
				lock=lock,
				limiter=limiter
		)
	
	@property
	def legacy(self) -> legacyPermissions:
		return self._legacy_impl
	
	async def set_permission(
			self,
			descriptor: Union[Dict[str, Any], PermissionDescriptor],
			state: str,
			origin: str,
			user_context: Optional[str] = None,
	) -> None:
		await self.sync_to_trio(sync_function=self._set_permission_impl)(
				descriptor=descriptor,
				state=state,
				origin=origin,
				user_context=user_context
		)
