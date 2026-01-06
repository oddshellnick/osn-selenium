from abc import ABC, abstractmethod
from osn_selenium.abstract.executors.cdp import AbstractCDPExecutor
from osn_selenium.abstract.executors.javascript import AbstractJSExecutor


class AbstractWebDriver(ABC):
	"""
	Abstract base class for a WebDriver.

	This class defines the interface that all WebDriver implementations must adhere to.
	It includes methods for browser navigation, element interaction, script execution,
	and managing various browser features.
	"""
	
	@abstractmethod
	def cdp(self) -> AbstractCDPExecutor:
		"""
		Returns the CDP (Chrome DevTools Protocol) executor.

		Returns:
			AbstractCDPExecutor: The CDP executor instance.
		"""
		
		...
	
	@abstractmethod
	def javascript(self) -> AbstractJSExecutor:
		"""
		Returns the JavaScript executor for this WebDriver instance.

		Returns:
			AbstractJSExecutor: The JavaScript executor instance.
		"""
		
		...
