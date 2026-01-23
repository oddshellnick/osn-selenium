from selenium.webdriver.common.by import By
from osn_selenium.instances.convert import get_legacy_instance
from typing import (
	Any,
	Dict,
	Iterable,
	List,
	Optional
)
from selenium.webdriver.remote.shadowroot import (
	ShadowRoot as legacyShadowRoot
)
from selenium.webdriver.remote.webelement import (
	WebElement as legacyWebElement
)
from selenium.webdriver.support.wait import (
	WebDriverWait as legacyWebDriverWait
)


__all__ = ["UnifiedWebElement"]


class UnifiedWebElement:
	def __init__(self, selenium_web_element: legacyWebElement):
		if not isinstance(selenium_web_element, legacyWebElement):
			raise ExpectedTypeError(
					expected_class=legacyWebElement,
					received_instance=selenium_web_element
			)
		
		self._selenium_web_element = selenium_web_element
	
	def __repr__(self) -> str:
		return self._legacy_impl.__repr__()
	
	@property
	def _legacy_impl(self) -> legacyWebElement:
		return self._selenium_web_element
	
	def __eq__(self, other: Any) -> bool:
		return self._legacy_impl == get_legacy_instance(instance=other)
	
	def __hash__(self) -> int:
		return self._legacy_impl.__hash__()
	
	def __ne__(self, other: Any) -> bool:
		return self._legacy_impl != get_legacy_instance(instance=other)
	
	def _accessible_name_impl(self) -> str:
		return self._legacy_impl.accessible_name
	
	def _aria_role_impl(self) -> str:
		return self._legacy_impl.aria_role
	
	def _clear_impl(self) -> None:
		self._legacy_impl.clear()
	
	def _click_impl(self) -> None:
		self._legacy_impl.click()
	
	def _find_element_impl(self, by: str = By.ID, value: Any = None) -> legacyWebElement:
		return self._legacy_impl.find_element(by=by, value=value)
	
	def _find_elements_impl(self, by: str = By.ID, value: Any = None) -> List[legacyWebElement]:
		return self._legacy_impl.find_elements(by=by, value=value)
	
	def _get_attribute_impl(self, name: str) -> Optional[str]:
		return self._legacy_impl.get_attribute(name=name)
	
	def _get_dom_attribute_impl(self, name: str) -> Optional[str]:
		return self._legacy_impl.get_dom_attribute(name=name)
	
	def _get_property_impl(self, name: str) -> Any:
		return self._legacy_impl.get_property(name=name)
	
	def _id_impl(self) -> str:
		return self._legacy_impl.id
	
	def _is_displayed_impl(self) -> bool:
		return self._legacy_impl.is_displayed()
	
	def _is_enabled_impl(self) -> bool:
		return self._legacy_impl.is_enabled()
	
	def _is_selected_impl(self) -> bool:
		return self._legacy_impl.is_selected()
	
	def _location_impl(self) -> Dict:
		return self._legacy_impl.location
	
	def _location_once_scrolled_into_view_impl(self) -> Dict:
		return self._legacy_impl.location_once_scrolled_into_view
	
	def _parent_impl(self) -> Any:
		return self._legacy_impl.parent
	
	def _rect_impl(self) -> Dict:
		return self._legacy_impl.rect
	
	def _screenshot_as_base64_impl(self) -> str:
		return self._legacy_impl.screenshot_as_base64
	
	def _screenshot_as_png_impl(self) -> bytes:
		return self._legacy_impl.screenshot_as_png
	
	def _screenshot_impl(self, filename: str) -> bool:
		return self._legacy_impl.screenshot(filename=filename)
	
	def _send_keys_impl(self, *value: str) -> None:
		self._legacy_impl.send_keys(*value)
	
	def _session_id_impl(self) -> str:
		return self._legacy_impl.session_id
	
	def _shadow_root_impl(self) -> legacyShadowRoot:
		return self._legacy_impl.shadow_root
	
	def _size_impl(self) -> Dict:
		return self._legacy_impl.size
	
	def _submit_impl(self) -> None:
		self._legacy_impl.submit()
	
	def _tag_name_impl(self) -> str:
		return self._legacy_impl.tag_name
	
	def _text_impl(self) -> str:
		return self._legacy_impl.text
	
	def _value_of_css_property_impl(self, property_name: str) -> str:
		return self._legacy_impl.value_of_css_property(property_name=property_name)
	
	def _web_driver_wait_impl(
			self,
			timeout: float,
			poll_frequency: float = 0.5,
			ignored_exceptions: Optional[Iterable[BaseException]] = None,
	) -> legacyWebDriverWait:
		return legacyWebDriverWait(
				driver=self._legacy_impl,
				timeout=timeout,
				poll_frequency=poll_frequency,
				ignored_exceptions=ignored_exceptions
		)
