from typing import List, Optional
from selenium.webdriver.common.by import By
from osn_selenium.instances.sync.web_element import WebElement
from osn_selenium.instances.convert import (
	get_sync_instance_wrapper
)
from osn_selenium.webdrivers.unified.core.element import (
	UnifiedCoreElementMixin
)
from osn_selenium.abstract.webdriver.core.element import (
	AbstractCoreElementMixin
)


__all__ = ["CoreElementMixin"]


class CoreElementMixin(UnifiedCoreElementMixin, AbstractCoreElementMixin):
	"""
	Mixin for DOM element retrieval in Core WebDrivers.

	Provides standard methods to locate single or multiple elements within
	the current page context.
	"""
	
	def create_web_element(self, element_id: str) -> WebElement:
		legacy = self._create_web_element_impl(element_id=element_id)
		
		return get_sync_instance_wrapper(wrapper_class=WebElement, legacy_object=legacy)
	
	def find_element(self, by: str = By.ID, value: Optional[str] = None) -> WebElement:
		legacy = self._find_element_impl(by=by, value=value)
		
		return get_sync_instance_wrapper(wrapper_class=WebElement, legacy_object=legacy)
	
	def find_elements(self, by: str = By.ID, value: Optional[str] = None) -> List[WebElement]:
		legacy_elements = self._find_elements_impl(by=by, value=value)
		
		return [
			get_sync_instance_wrapper(wrapper_class=WebElement, legacy_object=element)
			for element in legacy_elements
		]
