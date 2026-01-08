from abc import abstractmethod
from osn_selenium.abstract.executors.cdp import AbstractCDPExecutor
from osn_selenium.abstract.webdriver.core import (
	AbstractCoreWebDriver as AbstractBaseWebDriver
)


class AbstractBlinkWebDriver(AbstractBaseWebDriver):
	"""
	Abstract base class for Blink-based WebDrivers.

	Combines the standard WebDriver interface with Blink-specific functionality,
	specifically access to the Chrome DevTools Protocol (CDP).
	"""
	
	@property
	@abstractmethod
	def cdp(self) -> AbstractCDPExecutor:
		"""
		Returns the CDP (Chrome DevTools Protocol) executor.

		Returns:
			AbstractCDPExecutor: The CDP executor instance used for sending
			commands directly to the browser via the DevTools protocol.
		"""
		
		...
