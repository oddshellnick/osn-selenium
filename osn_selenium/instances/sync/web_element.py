from selenium.webdriver.common.by import By
from osn_selenium.instances.sync.shadow_root import ShadowRoot
from typing import (
	Any,
	Dict,
	List,
	Optional,
	Self,
	Type
)
from osn_selenium.abstract.instances.web_element import AbstractWebElement
from selenium.webdriver.remote.webelement import (
	WebElement as legacyWebElement
)


class WebElement(AbstractWebElement):
	def __init__(self, selenium_web_element: legacyWebElement,) -> None:
		self._selenium_web_element = selenium_web_element
	
	def __repr__(self) -> str:
		return self.legacy.__repr__()
	
	@property
	def legacy(self) -> legacyWebElement:
		return self._selenium_web_element
	
	def __eq__(self, other: Type[AbstractWebElement]) -> bool:
		return self.legacy == other.legacy
	
	def __hash__(self) -> int:
		return self.legacy.__hash__()
	
	def __ne__(self, other: Type[AbstractWebElement]) -> bool:
		return self.legacy != other.legacy
	
	def accessible_name(self) -> str:
		return self.legacy.accessible_name
	
	def aria_role(self) -> str:
		return self.legacy.aria_role
	
	def clear(self) -> None:
		self.legacy.clear()
	
	def click(self) -> None:
		self.legacy.click()
	
	@classmethod
	def from_legacy(cls, selenium_web_element: legacyWebElement,) -> Self:
		"""
		Creates an instance from a legacy Selenium WebElement object.

		This factory method is used to wrap an existing Selenium WebElement
		instance into the new interface.

		Args:
			selenium_web_element (legacyWebElement): The legacy Selenium WebElement instance.

		Returns:
			Self: A new instance of a class implementing WebElement.
		"""
		
		return cls(selenium_web_element=selenium_web_element)
	
	def find_element(self, by: str = By.ID, value: Any = None,) -> "WebElement":
		impl_el = self.legacy.find_element(by=by, value=value)
		return self.from_legacy(selenium_web_element=impl_el)
	
	def find_elements(self, by: str = By.ID, value: Any = None,) -> List["WebElement"]:
		impl_list = self.legacy.find_elements(by=by, value=value)
		return [self.from_legacy(selenium_web_element=e) for e in impl_list]
	
	def get_attribute(self, name: str,) -> Optional[str]:
		return self.legacy.get_attribute(name=name)
	
	def get_dom_attribute(self, name: str,) -> Optional[str]:
		return self.legacy.get_dom_attribute(name=name)
	
	def get_property(self, name: str,) -> Any:
		return self.legacy.get_property(name=name)
	
	def id(self) -> str:
		return self.legacy.id
	
	def is_displayed(self) -> bool:
		return self.legacy.is_displayed()
	
	def is_enabled(self) -> bool:
		return self.legacy.is_enabled()
	
	def is_selected(self) -> bool:
		return self.legacy.is_selected()
	
	def location(self) -> Dict:
		return self.legacy.location
	
	def location_once_scrolled_into_view(self) -> Dict:
		return self.legacy.location_once_scrolled_into_view
	
	def parent(self) -> "WebElement":
		impl_parent = self.legacy.parent
		return self.from_legacy(selenium_web_element=impl_parent)
	
	def rect(self) -> Dict:
		return self.legacy.rect
	
	def screenshot(self, filename: str,) -> bool:
		return self.legacy.screenshot(filename=filename)
	
	def screenshot_as_base64(self) -> str:
		return self.legacy.screenshot_as_base64
	
	def screenshot_as_png(self) -> bytes:
		return self.legacy.screenshot_as_png
	
	def send_keys(self, *value: str,) -> None:
		self.legacy.send_keys(*value)
	
	def session_id(self) -> str:
		return self.legacy.session_id
	
	def shadow_root(self) -> ShadowRoot:
		return ShadowRoot(selenium_shadow_root=self.legacy.shadow_root)
	
	def size(self) -> Dict:
		return self.legacy.size
	
	def submit(self) -> None:
		self.legacy.submit()
	
	def tag_name(self) -> str:
		return self.legacy.tag_name
	
	def text(self) -> str:
		return self.legacy.text
	
	def value_of_css_property(self, property_name: str,) -> str:
		return self.legacy.value_of_css_property(property_name=property_name)
