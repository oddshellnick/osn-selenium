from typing import List, Optional
from selenium.webdriver.common.by import By
from osn_selenium.webdrivers.sync.base.base import BaseMixin
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.instances.sync.web_element import WebElement
from osn_selenium.abstract.webdriver.base.element import AbstractElementMixin


class ElementMixin(BaseMixin, AbstractElementMixin):
	@requires_driver
	def create_web_element(self, element_id: str) -> WebElement:
		legacy = self.driver.create_web_element(element_id=element_id)
		
		return WebElement(selenium_web_element=legacy)
	
	@requires_driver
	def find_element(self, by: str = By.ID, value: Optional[str] = None) -> WebElement:
		element = self.driver.find_element(by=by, value=value)
		
		return WebElement(selenium_web_element=element)
	
	@requires_driver
	def find_elements(self, by: str = By.ID, value: Optional[str] = None) -> List[WebElement]:
		elements = self.driver.find_elements(by=by, value=value)
		
		return [WebElement(selenium_web_element=element) for element in elements]
