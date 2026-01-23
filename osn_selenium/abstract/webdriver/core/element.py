from typing import List, Optional
from abc import ABC, abstractmethod
from selenium.webdriver.common.by import By
from osn_selenium.abstract.instances.web_element import AbstractWebElement


__all__ = ["AbstractCoreElementMixin"]


class AbstractCoreElementMixin(ABC):
	"""Mixin responsible for finding and creating web elements."""
	
	@abstractmethod
	def create_web_element(self, element_id: str) -> AbstractWebElement:
		"""
		Creates a WebElement from an element ID.

		Args:
			element_id (str): The ID of the element.

		Returns:
			AbstractWebElement: The created WebElement instance.
		"""
		
		...
	
	@abstractmethod
	def find_element(self, by: By = By.ID, value: Optional[str] = None) -> AbstractWebElement:
		"""
		Finds an element within the current context using the given mechanism.

		Args:
			by (By): The strategy to use for finding the element (e.g., By.ID).
			value (Optional[str]): The value to search for.

		Returns:
			AbstractWebElement: The found WebElement.
		"""
		
		...
	
	@abstractmethod
	def find_elements(self, by: By = By.ID, value: Optional[str] = None) -> List[AbstractWebElement]:
		"""
		Finds all elements within the current context using the given mechanism.

		Args:
			by (By): The strategy to use for finding elements (e.g., By.ID).
			value (Optional[str]): The value to search for.

		Returns:
			List[AbstractWebElement]: A list of found WebElements.
		"""
		
		...
