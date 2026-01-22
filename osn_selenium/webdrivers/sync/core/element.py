from typing import List, Optional
from selenium.webdriver.common.by import By
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.instances.sync.web_element import WebElement
from osn_selenium.webdrivers.sync.core.base import CoreBaseMixin
from osn_selenium.instances.convert import (
	get_sync_instance_wrapper
)
from osn_selenium.abstract.webdriver.core.element import (
	AbstractCoreElementMixin
)


class CoreElementMixin(CoreBaseMixin, AbstractCoreElementMixin):
	"""
	Mixin for DOM element retrieval in Core WebDrivers.

	Provides standard methods to locate single or multiple elements within
	the current page context.
	"""
	
	@requires_driver
	def create_web_element(self, element_id: str) -> WebElement:
		legacy = self.driver.create_web_element(element_id=element_id)
		
		return get_sync_instance_wrapper(wrapper_class=WebElement, legacy_object=legacy)
	
	@requires_driver
	def find_element(self, by: str = By.ID, value: Optional[str] = None) -> WebElement:
		element = self.driver.find_element(by=by, value=value)
		
		return get_sync_instance_wrapper(wrapper_class=WebElement, legacy_object=element)
	
	@requires_driver
	def find_elements(self, by: str = By.ID, value: Optional[str] = None) -> List[WebElement]:
		elements = self.driver.find_elements(by=by, value=value)
		
		return [
			get_sync_instance_wrapper(wrapper_class=WebElement, legacy_object=element)
			for element in elements
		]
