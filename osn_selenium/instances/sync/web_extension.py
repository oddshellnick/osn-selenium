from typing import (
	Dict,
	Optional,
	Self,
	Union
)
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.exceptions.instance import (
	CannotConvertTypeError
)
from osn_selenium.instances._typehints import (
	WEB_EXTENSION_TYPEHINT
)
from osn_selenium.instances.unified.web_extension import UnifiedWebExtension
from osn_selenium.abstract.instances.web_extension import AbstractWebExtension
from selenium.webdriver.common.bidi.webextension import (
	WebExtension as legacyWebExtension
)


__all__ = ["WebExtension"]


class WebExtension(UnifiedWebExtension, AbstractWebExtension):
	"""
	Wrapper for the legacy Selenium WebExtension instance.

	Manages the installation and uninstallation of browser extensions via the
	WebDriver BiDi protocol.
	"""
	
	def __init__(self, selenium_web_extension: legacyWebExtension) -> None:
		"""
		Initializes the WebExtension wrapper.

		Args:
			selenium_web_extension (legacyWebExtension): The legacy Selenium WebExtension instance to wrap.
		"""
		
		UnifiedWebExtension.__init__(self, selenium_web_extension=selenium_web_extension)
	
	@classmethod
	def from_legacy(cls, legacy_object: WEB_EXTENSION_TYPEHINT) -> Self:
		"""
		Creates an instance from a legacy Selenium WebExtension object.

		This factory method is used to wrap an existing Selenium WebExtension
		instance into the new interface.

		Args:
			legacy_object (WEB_EXTENSION_TYPEHINT): The legacy Selenium WebExtension instance or its wrapper.

		Returns:
			Self: A new instance of a class implementing WebExtension.
		"""
		
		legacy_web_extension_obj = get_legacy_instance(instance=legacy_object)
		
		if not isinstance(legacy_web_extension_obj, legacyWebExtension):
			raise CannotConvertTypeError(from_=legacyWebExtension, to_=legacy_object)
		
		return cls(selenium_web_extension=legacy_web_extension_obj)
	
	def install(
			self,
			path: Optional[str] = None,
			archive_path: Optional[str] = None,
			base64_value: Optional[str] = None,
	) -> Dict:
		return self._install_impl(path=path, archive_path=archive_path, base64_value=base64_value)
	
	@property
	def legacy(self) -> legacyWebExtension:
		return self._legacy_impl
	
	def uninstall(self, extension_id_or_result: Union[str, Dict]) -> None:
		self._uninstall_impl(extension_id_or_result=extension_id_or_result)
