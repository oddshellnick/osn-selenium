from typing import List, Optional
from selenium.webdriver.common.by import By
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.webdrivers.trio_threads.base.base import BaseMixin
from osn_selenium.instances.trio_threads.web_element import WebElement
from osn_selenium.abstract.webdriver.base.element import AbstractElementMixin


class ElementMixin(BaseMixin, AbstractElementMixin):
	@requires_driver
	async def create_web_element(self, element_id: str) -> WebElement:
		legacy = await self._wrap_to_trio(self.driver.create_web_element, element_id=element_id)
		
		return WebElement(
				selenium_web_element=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	@requires_driver
	async def find_element(self, by: str = By.ID, value: Optional[str] = None) -> WebElement:
		element = await self._wrap_to_trio(self.driver.find_element, by=by, value=value)
		
		return WebElement(
				selenium_web_element=element,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	@requires_driver
	async def find_elements(self, by: str = By.ID, value: Optional[str] = None) -> List[WebElement]:
		elements = await self._wrap_to_trio(self.driver.find_elements, by=by, value=value)
		
		return [
			WebElement(
					selenium_web_element=element,
					lock=self._lock,
					limiter=self._capacity_limiter,
			) for element in elements
		]
