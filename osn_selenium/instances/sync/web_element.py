from selenium.webdriver.common.by import By
from osn_selenium.instances.sync.shadow_root import ShadowRoot
from osn_selenium.instances._typehints import WEB_ELEMENT_TYPEHINT
from osn_selenium.instances.sync.web_driver_wait import WebDriverWait
from typing import (
	Any,
	Dict,
	Iterable,
	List,
	Optional,
	Self
)
from osn_selenium.exceptions.instance import (
	CannotConvertTypeError
)
from osn_selenium.instances.unified.web_element import UnifiedWebElement
from osn_selenium.abstract.instances.web_element import AbstractWebElement
from selenium.webdriver.remote.webelement import (
	WebElement as legacyWebElement
)
from osn_selenium.instances.convert import (
	get_legacy_instance,
	get_sync_instance_wrapper
)


__all__ = ["WebElement"]


class WebElement(UnifiedWebElement, AbstractWebElement):
	"""
	Represents an HTML element in the DOM, offering methods for interaction (click, type),
	property retrieval, and finding child elements.
	"""
	
	def __init__(self, selenium_web_element: legacyWebElement) -> None:
		"""
		Initializes the WebElement wrapper.

		Args:
			selenium_web_element (legacyWebElement): The legacy Selenium WebElement instance to wrap.
		"""
		
		UnifiedWebElement.__init__(self, selenium_web_element=selenium_web_element)
	
	def accessible_name(self) -> str:
		return self._accessible_name_impl()
	
	def aria_role(self) -> str:
		return self._aria_role_impl()
	
	def clear(self) -> None:
		self._clear_impl()
	
	def click(self) -> None:
		self._click_impl()
	
	def find_element(self, by: str = By.ID, value: Any = None) -> Self:
		web_element = self._find_element_impl(by=by, value=value)
		
		return get_sync_instance_wrapper(wrapper_class=self.__class__, legacy_object=web_element)
	
	def find_elements(self, by: str = By.ID, value: Any = None) -> List[Self]:
		web_elements = self._find_elements_impl(by=by, value=value)
		
		return [
			get_sync_instance_wrapper(wrapper_class=self.__class__, legacy_object=web_element)
			for web_element in web_elements
		]
	
	def get_attribute(self, name: str) -> Optional[str]:
		return self._get_attribute_impl(name=name)
	
	def get_dom_attribute(self, name: str) -> Optional[str]:
		return self._get_dom_attribute_impl(name=name)
	
	def get_property(self, name: str) -> Any:
		return self._get_property_impl(name=name)
	
	def id(self) -> str:
		return self._id_impl()
	
	def is_displayed(self) -> bool:
		return self._is_displayed_impl()
	
	def is_enabled(self) -> bool:
		return self._is_enabled_impl()
	
	def is_selected(self) -> bool:
		return self._is_selected_impl()
	
	@property
	def legacy(self) -> legacyWebElement:
		return self._legacy_impl
	
	def location(self) -> Dict:
		return self._location_impl()
	
	def location_once_scrolled_into_view(self) -> Dict:
		return self._location_once_scrolled_into_view_impl()
	
	@classmethod
	def from_legacy(cls, legacy_object: WEB_ELEMENT_TYPEHINT) -> Self:
		"""
		Creates an instance from a legacy Selenium WebElement object.

		This factory method is used to wrap an existing Selenium WebElement
		instance into the new interface.

		Args:
			legacy_object (WEB_ELEMENT_TYPEHINT): The legacy Selenium WebElement instance or its wrapper.

		Returns:
			Self: A new instance of a class implementing WebElement.
		"""
		
		legacy_element_obj = get_legacy_instance(instance=legacy_object)
		
		if not isinstance(legacy_element_obj, legacyWebElement):
			raise CannotConvertTypeError(from_=legacyWebElement, to_=legacy_object)
		
		return cls(selenium_web_element=legacy_element_obj)
	
	def parent(self) -> Self:
		web_element = self._parent_impl()
		
		return self.from_legacy(legacy_object=web_element)
	
	def rect(self) -> Dict:
		return self._rect_impl()
	
	def screenshot(self, filename: str) -> bool:
		return self._screenshot_impl(filename=filename)
	
	def screenshot_as_base64(self) -> str:
		return self._screenshot_as_base64_impl()
	
	def screenshot_as_png(self) -> bytes:
		return self._screenshot_as_png_impl()
	
	def send_keys(self, *value: str) -> None:
		self._send_keys_impl(*value)
	
	def session_id(self) -> str:
		return self._session_id_impl()
	
	def shadow_root(self) -> ShadowRoot:
		shadow_root = self._shadow_root_impl()
		
		return get_sync_instance_wrapper(wrapper_class=ShadowRoot, legacy_object=shadow_root)
	
	def size(self) -> Dict:
		return self._size_impl()
	
	def submit(self) -> None:
		self._submit_impl()
	
	def tag_name(self) -> str:
		return self._tag_name_impl()
	
	def text(self) -> str:
		return self._text_impl()
	
	def value_of_css_property(self, property_name: str) -> str:
		return self._value_of_css_property_impl(property_name=property_name)
	
	def web_driver_wait(
			self,
			timeout: float,
			poll_frequency: float = 0.5,
			ignored_exceptions: Optional[Iterable[BaseException]] = None,
	) -> WebDriverWait:
		web_driver_wait = self._web_driver_wait_impl(
				timeout=timeout,
				poll_frequency=poll_frequency,
				ignored_exceptions=ignored_exceptions,
		)
		
		return get_sync_instance_wrapper(wrapper_class=WebDriverWait, legacy_object=web_driver_wait)
