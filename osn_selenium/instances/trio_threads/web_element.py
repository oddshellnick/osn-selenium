import trio
from selenium.webdriver.common.by import By
from osn_selenium.trio_threads_mixin import TrioThreadMixin
from osn_selenium.instances._typehints import WEB_ELEMENT_TYPEHINT
from typing import (
	Any,
	Dict,
	Iterable,
	List,
	Optional,
	Self
)
from osn_selenium.instances.trio_threads.shadow_root import ShadowRoot
from osn_selenium.exceptions.instance import (
	CannotConvertTypeError
)
from osn_selenium.instances.unified.web_element import UnifiedWebElement
from osn_selenium.abstract.instances.web_element import AbstractWebElement
from osn_selenium.instances.trio_threads.web_driver_wait import WebDriverWait
from selenium.webdriver.remote.webelement import (
	WebElement as legacyWebElement
)
from osn_selenium.instances.convert import (
	get_legacy_instance,
	get_trio_thread_instance_wrapper
)


__all__ = ["WebElement"]


class WebElement(UnifiedWebElement, TrioThreadMixin, AbstractWebElement):
	"""
	Represents an HTML element in the DOM, offering methods for interaction (click, type),
	property retrieval, and finding child elements.
	"""
	
	def __init__(
			self,
			selenium_web_element: legacyWebElement,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> None:
		"""
		Initializes the WebElement wrapper.

		Args:
			selenium_web_element (legacyWebElement): The legacy Selenium WebElement instance to wrap.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.
		"""
		
		UnifiedWebElement.__init__(self, selenium_web_element=selenium_web_element)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def accessible_name(self) -> str:
		return await self.sync_to_trio(sync_function=self._accessible_name_impl)()
	
	async def aria_role(self) -> str:
		return await self.sync_to_trio(sync_function=self._aria_role_impl)()
	
	async def clear(self) -> None:
		await self.sync_to_trio(sync_function=self._clear_impl)()
	
	async def click(self) -> None:
		await self.sync_to_trio(sync_function=self._click_impl)()
	
	async def find_element(self, by: str = By.ID, value: Any = None) -> Self:
		web_element = await self.sync_to_trio(sync_function=self._find_element_impl)(by=by, value=value)
		
		return get_trio_thread_instance_wrapper(
				wrapper_class=self.__class__,
				legacy_object=web_element,
				lock=self._lock,
				limiter=self._capacity_limiter
		)
	
	async def find_elements(self, by: str = By.ID, value: Any = None) -> List[Self]:
		web_elements = await self.sync_to_trio(sync_function=self._find_elements_impl)(by=by, value=value)
		
		return [
			get_trio_thread_instance_wrapper(
					wrapper_class=self.__class__,
					legacy_object=web_element,
					lock=self._lock,
					limiter=self._capacity_limiter,
			)
			for web_element in web_elements
		]
	
	async def get_attribute(self, name: str) -> Optional[str]:
		return await self.sync_to_trio(sync_function=self._get_attribute_impl)(name=name)
	
	async def get_dom_attribute(self, name: str) -> Optional[str]:
		return await self.sync_to_trio(sync_function=self._get_dom_attribute_impl)(name=name)
	
	async def get_property(self, name: str) -> Any:
		return await self.sync_to_trio(sync_function=self._get_property_impl)(name=name)
	
	async def id(self) -> str:
		return await self.sync_to_trio(sync_function=self._id_impl)()
	
	async def is_displayed(self) -> bool:
		return await self.sync_to_trio(sync_function=self._is_displayed_impl)()
	
	async def is_enabled(self) -> bool:
		return await self.sync_to_trio(sync_function=self._is_enabled_impl)()
	
	async def is_selected(self) -> bool:
		return await self.sync_to_trio(sync_function=self._is_selected_impl)()
	
	@property
	def legacy(self) -> legacyWebElement:
		return self._legacy_impl
	
	async def location(self) -> Dict:
		return await self.sync_to_trio(sync_function=self._location_impl)()
	
	async def location_once_scrolled_into_view(self) -> Dict:
		return await self.sync_to_trio(sync_function=self._location_once_scrolled_into_view_impl)()
	
	@classmethod
	def from_legacy(
			cls,
			legacy_object: WEB_ELEMENT_TYPEHINT,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	) -> Self:
		"""
		Creates an instance from a legacy Selenium WebElement object.

		This factory method is used to wrap an existing Selenium WebElement
		instance into the new interface.

		Args:
			legacy_object (WEB_ELEMENT_TYPEHINT): The legacy Selenium WebElement instance or its wrapper.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.

		Returns:
			Self: A new instance of a class implementing WebElement.
		"""
		
		legacy_element_obj = get_legacy_instance(instance=legacy_object)
		
		if not isinstance(legacy_element_obj, legacyWebElement):
			raise CannotConvertTypeError(from_=legacyWebElement, to_=legacy_object)
		
		return cls(selenium_web_element=legacy_element_obj, lock=lock, limiter=limiter)
	
	async def parent(self) -> Self:
		parent = await self.sync_to_trio(sync_function=self._parent_impl)()
		
		return self.from_legacy(legacy_object=parent, lock=self._lock, limiter=self._capacity_limiter,)
	
	async def rect(self) -> Dict:
		return await self.sync_to_trio(sync_function=self._rect_impl)()
	
	async def screenshot(self, filename: str) -> bool:
		return await self.sync_to_trio(sync_function=self._screenshot_impl)(filename=filename)
	
	async def screenshot_as_base64(self) -> str:
		return await self.sync_to_trio(sync_function=self._screenshot_as_base64_impl)()
	
	async def screenshot_as_png(self) -> bytes:
		return await self.sync_to_trio(sync_function=self._screenshot_as_png_impl)()
	
	async def send_keys(self, *value: str) -> None:
		await self.sync_to_trio(sync_function=self._send_keys_impl)(*value)
	
	async def session_id(self) -> str:
		return await self.sync_to_trio(sync_function=self._session_id_impl)()
	
	async def shadow_root(self) -> ShadowRoot:
		shadow_root = await self.sync_to_trio(sync_function=self._shadow_root_impl)()
		
		return get_trio_thread_instance_wrapper(
				wrapper_class=ShadowRoot,
				legacy_object=shadow_root,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	async def size(self) -> Dict:
		return await self.sync_to_trio(sync_function=self._size_impl)()
	
	async def submit(self) -> None:
		await self.sync_to_trio(sync_function=self._submit_impl)()
	
	async def tag_name(self) -> str:
		return await self.sync_to_trio(sync_function=self._tag_name_impl)()
	
	async def text(self) -> str:
		return await self.sync_to_trio(sync_function=self._text_impl)()
	
	async def value_of_css_property(self, property_name: str) -> str:
		return await self.sync_to_trio(sync_function=self._value_of_css_property_impl)(property_name=property_name)
	
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
		
		return get_trio_thread_instance_wrapper(
				wrapper_class=WebDriverWait,
				legacy_object=web_driver_wait,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
