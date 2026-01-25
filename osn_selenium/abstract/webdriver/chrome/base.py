from typing import Optional
from abc import abstractmethod
from selenium.webdriver.chrome.webdriver import (
	WebDriver as legacyWebDriver
)
from osn_selenium.abstract.webdriver.blink.base import (
	AbstractBlinkBaseMixin
)


__all__ = ["AbstractChromeBaseMixin"]


class AbstractChromeBaseMixin(AbstractBlinkBaseMixin):
	"""
	Abstract mixin defining the base interface for Chrome-based WebDrivers.

	This class serves as a foundational component for Chrome WebDriver implementations,
	providing access to the underlying Selenium WebDriver instance.
	"""
	
	@property
	@abstractmethod
	def driver(self) -> Optional[legacyWebDriver]:
		"""
		Gets the underlying Selenium WebDriver instance associated with this object.

		This property provides direct access to the WebDriver object (e.g., Chrome)
		that is being controlled, allowing for direct Selenium operations if needed.

		Returns:
			Optional[legacyWebDriver]:
				The active WebDriver instance, or None if no driver is currently set or active.
		"""
		
		...
