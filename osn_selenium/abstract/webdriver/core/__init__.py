from abc import ABC, abstractmethod
from osn_selenium.abstract.executors.javascript import AbstractJSExecutor


class AbstractCoreWebDriver(ABC):
	"""
	Abstract base class for a WebDriver.

	This class defines the interface that all WebDriver implementations must adhere to.
	It includes methods for browser navigation, element interaction, script execution,
	and managing various browser features.
	"""
	
	@property
	@abstractmethod
	def javascript(self) -> AbstractJSExecutor:
		"""
		Returns the JavaScript executor for this WebDriver instance.

		Returns:
			AbstractJSExecutor: The JavaScript executor instance.
		"""
		
		...
