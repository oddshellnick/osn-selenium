from typing import (
	Dict,
	Optional,
	Union
)
from osn_selenium.exceptions.instance import NotExpectedTypeError
from selenium.webdriver.common.bidi.webextension import (
	WebExtension as legacyWebExtension
)


__all__ = ["UnifiedWebExtension"]


class UnifiedWebExtension:
	def __init__(self, selenium_web_extension: legacyWebExtension):
		if not isinstance(selenium_web_extension, legacyWebExtension):
			raise NotExpectedTypeError(
					expected_type=legacyWebExtension,
					received_instance=selenium_web_extension
			)
		
		self._selenium_web_extension = selenium_web_extension
	
	def _install_impl(
			self,
			path: Optional[str] = None,
			archive_path: Optional[str] = None,
			base64_value: Optional[str] = None,
	) -> Dict:
		return self._legacy_impl.install(path=path, archive_path=archive_path, base64_value=base64_value)
	
	@property
	def _legacy_impl(self) -> legacyWebExtension:
		return self._selenium_web_extension
	
	def _uninstall_impl(self, extension_id_or_result: Union[str, Dict]) -> None:
		self._legacy_impl.uninstall(extension_id_or_result=extension_id_or_result)
