import trio
from typing import (
	Dict,
	Optional,
	Self,
	Union
)
from osn_selenium.base_mixin import TrioThreadMixin
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.instances.types import (
	WEB_EXTENSION_TYPEHINT
)
from osn_selenium.abstract.instances.web_extension import AbstractWebExtension
from osn_selenium.instances.errors import (
	ExpectedTypeError,
	TypesConvertError
)
from selenium.webdriver.common.bidi.webextension import (
	WebExtension as legacyWebExtension
)


class WebExtension(TrioThreadMixin, AbstractWebExtension):
	"""
	Wrapper for the legacy Selenium WebExtension instance.

	Manages the installation and uninstallation of browser extensions via the
	WebDriver BiDi protocol.
	"""
	
	def __init__(
			self,
			selenium_web_extension: legacyWebExtension,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> None:
		"""
		Initializes the WebExtension wrapper.

		Args:
			selenium_web_extension (legacyWebExtension): The legacy Selenium WebExtension instance to wrap.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.
		"""
		
		super().__init__(lock=lock, limiter=limiter)
		
		if not isinstance(selenium_web_extension, legacyWebExtension):
			raise ExpectedTypeError(
					expected_class=legacyWebExtension,
					received_instance=selenium_web_extension
			)
		
		self._selenium_web_extension = selenium_web_extension
	
	@classmethod
	def from_legacy(
			cls,
			selenium_web_extension: WEB_EXTENSION_TYPEHINT,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> Self:
		"""
		Creates an instance from a legacy Selenium WebExtension object.

		This factory method is used to wrap an existing Selenium WebExtension
		instance into the new interface.

		Args:
			selenium_web_extension (WEB_EXTENSION_TYPEHINT): The legacy Selenium WebExtension instance or its wrapper.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.

		Returns:
			Self: A new instance of a class implementing WebExtension.
		"""
		
		legacy_web_extension_obj = get_legacy_instance(selenium_web_extension)
		
		if not isinstance(legacy_web_extension_obj, legacyWebExtension):
			raise TypesConvertError(from_=legacyWebExtension, to_=selenium_web_extension)
		
		return cls(
				selenium_web_extension=legacy_web_extension_obj,
				lock=lock,
				limiter=limiter
		)
	
	async def install(
			self,
			path: Optional[str] = None,
			archive_path: Optional[str] = None,
			base64_value: Optional[str] = None,
	) -> Dict:
		return await self._sync_to_trio(
				self.legacy.install,
				path=path,
				archive_path=archive_path,
				base64_value=base64_value
		)
	
	@property
	def legacy(self) -> legacyWebExtension:
		return self._selenium_web_extension
	
	async def uninstall(self, extension_id_or_result: Union[str, Dict]) -> None:
		await self._sync_to_trio(self.legacy.uninstall, extension_id_or_result=extension_id_or_result)
