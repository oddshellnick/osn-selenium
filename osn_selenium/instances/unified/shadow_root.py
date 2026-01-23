from typing import Any, List, Optional
from selenium.webdriver.common.by import By
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.exceptions.instance import NotExpectedTypeError
from selenium.webdriver.remote.shadowroot import (
	ShadowRoot as legacyShadowRoot
)
from selenium.webdriver.remote.webelement import (
	WebElement as legacyWebElement
)


__all__ = ["UnifiedShadowRoot"]


class UnifiedShadowRoot:
	def __init__(self, selenium_shadow_root: legacyShadowRoot):
		if not isinstance(selenium_shadow_root, legacyShadowRoot):
			raise NotExpectedTypeError(expected_type=legacyShadowRoot, received_instance=selenium_shadow_root)
		
		self._selenium_shadow_root = selenium_shadow_root
	
	def __repr__(self) -> str:
		return self._legacy_impl.__repr__()
	
	@property
	def _legacy_impl(self) -> legacyShadowRoot:
		return self._selenium_shadow_root
	
	def __eq__(self, other: Any) -> bool:
		return self._legacy_impl == get_legacy_instance(instance=other)
	
	def __hash__(self) -> int:
		return self._legacy_impl.__hash__()
	
	def __ne__(self, other: Any) -> bool:
		return self._legacy_impl != get_legacy_instance(instance=other)
	
	def _find_element_impl(self, by: str = By.ID, value: Optional[str] = None) -> legacyWebElement:
		return self._legacy_impl.find_element(by=by, value=value)
	
	def _find_elements_impl(self, by: str = By.ID, value: Optional[str] = None) -> List[legacyWebElement]:
		return self._legacy_impl.find_elements(by=by, value=value)
	
	def _id_impl(self) -> str:
		return self._legacy_impl.id
