from typing import (
	Dict,
	Optional,
	Self,
	Union
)
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.instances.types import (
	WEB_EXTENSION_TYPEHINT
)
from osn_selenium.abstract.instances.web_extension import AbstractWebExtension
from selenium.webdriver.common.bidi.webextension import (
	WebExtension as legacyWebExtension
)


class WebExtension(AbstractWebExtension):
	def __init__(self, selenium_web_extension: legacyWebExtension) -> None:
		if not isinstance(selenium_web_extension, legacyWebExtension):
			raise TypeError(
					f"Expected {type(legacyWebExtension)}, got {type(selenium_web_extension)}"
			)
		
		self._selenium_web_extension = selenium_web_extension
	
	@classmethod
	def from_legacy(cls, selenium_web_extension: WEB_EXTENSION_TYPEHINT) -> Self:
		legacy_web_extension_obj = get_legacy_instance(selenium_web_extension)
		
		if not isinstance(legacy_web_extension_obj, legacyWebExtension):
			raise TypeError(
					f"Could not convert input to {type(legacyWebExtension)}: {type(selenium_web_extension)}"
			)
		
		return cls(selenium_web_extension=legacy_web_extension_obj)
	
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
