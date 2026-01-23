from typing import List, Optional
from selenium.webdriver.common.by import By
from osn_selenium.webdrivers._decorators import requires_driver
from osn_selenium.webdrivers.unified.core.base import UnifiedCoreBaseMixin
from selenium.webdriver.remote.webelement import (
	WebElement as legacyWebElement
)


__all__ = ["UnifiedCoreElementMixin"]


class UnifiedCoreElementMixin(UnifiedCoreBaseMixin):
	@requires_driver
	def _create_web_element_impl(self, element_id: str) -> legacyWebElement:
		return self._driver_impl.create_web_element(element_id=element_id)
	
	@requires_driver
	def _find_element_impl(self, by: str = By.ID, value: Optional[str] = None) -> legacyWebElement:
		return self._driver_impl.find_element(by=by, value=value)
	
	@requires_driver
	def _find_elements_impl(self, by: str = By.ID, value: Optional[str] = None) -> List[legacyWebElement]:
		return self._driver_impl.find_elements(by=by, value=value)
