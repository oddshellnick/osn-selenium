from typing import List, Self
from osn_selenium.instances.types import BROWSER_TYPEHINT
from osn_selenium.instances.errors import TypesConvertError
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.instances.unified.browser import UnifiedBrowser
from osn_selenium.abstract.instances.browser import AbstractBrowser
from selenium.webdriver.common.bidi.browser import (
	Browser as legacyBrowser,
	ClientWindowInfo
)


class Browser(UnifiedBrowser, AbstractBrowser):
	"""
	Wrapper for the legacy Selenium BiDi Browser instance.

	Provides methods to manage user contexts (profiles) and inspect client
	window information via the WebDriver BiDi protocol.
	"""
	
	def __init__(self, selenium_browser: legacyBrowser) -> None:
		"""
		Initializes the Browser wrapper.

		Args:
			selenium_browser (legacyBrowser): The legacy Selenium Browser instance to wrap.
		"""
		
		UnifiedBrowser.__init__(self, selenium_browser=selenium_browser)
	
	def create_user_context(self) -> str:
		return self._create_user_context_impl()
	
	@classmethod
	def from_legacy(cls, selenium_browser: BROWSER_TYPEHINT) -> Self:
		"""
		Creates an instance from a legacy Selenium Browser object.

		This factory method is used to wrap an existing Selenium Browser
		instance into the new interface.

		Args:
			selenium_browser (BROWSER_TYPEHINT): The legacy Selenium Browser instance or its wrapper.

		Returns:
			Self: A new instance of a class implementing Browser.
		"""
		
		legacy_browser_obj = get_legacy_instance(selenium_browser)
		
		if not isinstance(legacy_browser_obj, legacyBrowser):
			raise TypesConvertError(from_=legacyBrowser, to_=selenium_browser)
		
		return cls(selenium_browser=legacy_browser_obj)
	
	def get_client_windows(self) -> List[ClientWindowInfo]:
		return self._get_client_windows_impl()
	
	def get_user_contexts(self) -> List[str]:
		return self._get_user_contexts_impl()
	
	@property
	def legacy(self) -> legacyBrowser:
		return self._legacy_impl
	
	def remove_user_context(self, user_context_id: str) -> None:
		self._remove_user_context_impl(user_context_id=user_context_id)
