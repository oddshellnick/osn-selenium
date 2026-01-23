from abc import ABC, abstractmethod
from selenium.webdriver.common.action_chains import (
	ActionChains as legacyActionChains
)


__all__ = ["AbstractBaseMixin"]


class AbstractBaseMixin(ABC):
	"""
	Base mixin class providing access to the legacy Selenium ActionChains.
	"""
	
	@property
	@abstractmethod
	def legacy(self) -> legacyActionChains:
		"""
		Returns the legacy Selenium ActionChains object.

		Returns:
			legacyActionChains: The underlying Selenium action chain object.
		"""
		
		...
