from abc import ABC
from osn_selenium.abstract.webdriver.core import (
	AbstractCoreWebDriver as AbstractBaseWebDriver
)


__all__ = ["AbstractBlinkWebDriver"]


class AbstractBlinkWebDriver(AbstractBaseWebDriver, ABC):
	"""
	Abstract base class for Blink-based WebDrivers.

	Combines the standard WebDriver interface with Blink-specific functionality,
	specifically access to the Chrome DevTools Protocol (CDP).
	"""
	
	pass
