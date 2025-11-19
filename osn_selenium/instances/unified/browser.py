from typing import List
from osn_selenium.exceptions.instance import NotExpectedTypeError
from selenium.webdriver.common.bidi.browser import (
	Browser as legacyBrowser,
	ClientWindowInfo
)


__all__ = ["UnifiedBrowser"]


class UnifiedBrowser:
	def __init__(self, selenium_browser: legacyBrowser):
		if not isinstance(selenium_browser, legacyBrowser):
			raise NotExpectedTypeError(expected_type=legacyBrowser, received_instance=selenium_browser)
		
		self._selenium_browser = selenium_browser
	
	def _create_user_context_impl(self) -> str:
		return self._legacy_impl.create_user_context()
	
	def _get_client_windows_impl(self) -> List[ClientWindowInfo]:
		return self._legacy_impl.get_client_windows()
	
	def _get_user_contexts_impl(self) -> List[str]:
		return self._legacy_impl.get_user_contexts()
	
	@property
	def _legacy_impl(self) -> legacyBrowser:
		return self._selenium_browser
	
	def _remove_user_context_impl(self, user_context_id: str) -> None:
		self._legacy_impl.remove_user_context(user_context_id=user_context_id)
