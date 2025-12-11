from typing import List, Self
from osn_selenium.instances.types import BROWSER_TYPEHINT
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.abstract.instances.browser import AbstractBrowser
from selenium.webdriver.common.bidi.browser import (
	Browser as legacyBrowser,
	ClientWindowInfo
)


class Browser(AbstractBrowser):
	def __init__(self, selenium_browser: legacyBrowser) -> None:
		if not isinstance(selenium_browser, legacyBrowser):
			raise TypeError(f"Expected {type(legacyBrowser)}, got {type(selenium_browser)}")
		
		self._selenium_browser = selenium_browser
	
	def create_user_context(self) -> str:
		return self._selenium_browser.create_user_context()
	
	@classmethod
	def from_legacy(cls, selenium_browser: BROWSER_TYPEHINT) -> Self:
		legacy_browser_obj = get_legacy_instance(selenium_browser)
		
		if not isinstance(legacy_browser_obj, legacyBrowser):
			raise TypeError(
					f"Could not convert input to {type(legacyBrowser)}: {type(selenium_browser)}"
			)
		
		return cls(selenium_browser=legacy_browser_obj)
	
	def get_client_windows(self) -> List[ClientWindowInfo]:
		return self._selenium_browser.get_client_windows()
	
	def get_user_contexts(self) -> List[str]:
		return self._selenium_browser.get_user_contexts()
	
	@property
	def legacy(self) -> legacyBrowser:
		return self._selenium_browser
	
	def remove_user_context(self, user_context_id: str) -> None:
		self._selenium_browser.remove_user_context(user_context_id=user_context_id)
