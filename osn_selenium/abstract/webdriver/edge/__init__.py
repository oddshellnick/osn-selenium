from abc import ABC
from osn_selenium.abstract.webdriver.blink import (
	AbstractBlinkWebDriver
)


__all__ = ["AbstractEdgeWebDriver"]


class AbstractEdgeWebDriver(AbstractBlinkWebDriver, ABC):
	"""
	Abstract composite class representing a full Edge WebDriver.

	Combines lifecycle, settings, and base functionality for Edge browser.
	Serves as the main entry point for abstract Edge implementations.
	"""
	
	pass
