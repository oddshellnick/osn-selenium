from typing import List, Self
from osn_selenium.abstract.instances.browser import AbstractBrowser
from selenium.webdriver.common.bidi.browser import (
	Browser as legacyBrowser,
	ClientWindowInfo
)


class Browser(AbstractBrowser):
	def __init__(self, selenium_browser: legacyBrowser,) -> None:
		self._selenium_browser = selenium_browser
	
	def create_user_context(self) -> str:
		return self._selenium_browser.create_user_context()
	
	@classmethod
	def from_legacy(cls, selenium_browser: legacyBrowser,) -> Self:
		"""
		Creates an instance from a legacy Selenium Browser object.

		This factory method is used to wrap an existing Selenium Browser
		instance into the new interface.

		Args:
			selenium_browser (legacyBrowser): The legacy Selenium Browser instance.

		Returns:
			Self: A new instance of a class implementing Browser.
		"""
		
		return cls(selenium_browser=selenium_browser)
	
	def get_client_windows(self) -> List[ClientWindowInfo]:
		return self._selenium_browser.get_client_windows()
	
	def get_user_contexts(self) -> List[str]:
		return self._selenium_browser.get_user_contexts()
	
	@property
	def legacy(self) -> legacyBrowser:
		return self._selenium_browser
	
	def remove_user_context(self, user_context_id: str) -> None:
		self._selenium_browser.remove_user_context(user_context_id=user_context_id)
