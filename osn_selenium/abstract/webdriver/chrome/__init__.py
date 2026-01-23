from abc import ABC
from osn_selenium.abstract.webdriver.blink import (
	AbstractBlinkWebDriver
)


__all__ = ["AbstractChromeWebDriver"]


class AbstractChromeWebDriver(AbstractBlinkWebDriver, ABC):
	"""
	Abstract composite class representing a full Chrome WebDriver.

	Combines lifecycle, settings, and base functionality for Chrome-based browsers.
	Serves as the main entry point for abstract Chrome implementations.
	"""
	
	pass
