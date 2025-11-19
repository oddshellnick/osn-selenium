from typing import (
	Dict,
	Optional,
	Self,
	Union
)
from osn_selenium.abstract.instances.web_extension import AbstractWebExtension
from selenium.webdriver.common.bidi.webextension import (
	WebExtension as legacyWebExtension
)


class WebExtension(AbstractWebExtension):
	def __init__(self, selenium_web_extension: legacyWebExtension,) -> None:
		self._selenium_web_extension = selenium_web_extension
	
	@classmethod
	def from_legacy(cls, selenium_web_extension: legacyWebExtension,) -> Self:
		"""
		Creates an instance from a legacy Selenium WebExtension object.

		This factory method is used to wrap an existing Selenium WebExtension
		instance into the new interface.

		Args:
			selenium_web_extension (legacyWebExtension): The legacy Selenium WebExtension instance.

		Returns:
			Self: A new instance of a class implementing WebExtension.
		"""
		
		return cls(selenium_web_extension=selenium_web_extension)
	
	def install(
			self,
			path: Optional[str] = None,
			archive_path: Optional[str] = None,
			base64_value: Optional[str] = None,
	) -> Dict:
		return self.legacy.install(path=path, archive_path=archive_path, base64_value=base64_value)
	
	@property
	def legacy(self) -> legacyWebExtension:
		return self._selenium_web_extension
	
	def uninstall(self, extension_id_or_result: Union[str, Dict]) -> None:
		self.legacy.uninstall(extension_id_or_result=extension_id_or_result)
