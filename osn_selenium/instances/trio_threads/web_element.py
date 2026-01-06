import trio
from selenium.webdriver.common.by import By
from osn_selenium.trio_base_mixin import _TrioThreadMixin
from typing import (
	Any,
	Dict,
	List,
	Optional,
	Self
)
from osn_selenium.instances.types import WEB_ELEMENT_TYPEHINT
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.instances.trio_threads.shadow_root import ShadowRoot
from osn_selenium.abstract.instances.web_element import AbstractWebElement
from osn_selenium.instances.errors import (
	ExpectedTypeError,
	TypesConvertError
)
from selenium.webdriver.remote.webelement import (
	WebElement as legacyWebElement
)


class WebElement(_TrioThreadMixin, AbstractWebElement):
	def __init__(
			self,
			selenium_web_element: legacyWebElement,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> None:
		super().__init__(lock=lock, limiter=limiter)
		
		if not isinstance(selenium_web_element, legacyWebElement):
			raise ExpectedTypeError(
					expected_class=legacyWebElement,
					received_instance=selenium_web_element
			)
		
		self._selenium_web_element = selenium_web_element
	
	def __repr__(self) -> str:
		return self.legacy.__repr__()
	
	@property
	def legacy(self) -> legacyWebElement:
		return self._selenium_web_element
	
	def __eq__(self, other: WEB_ELEMENT_TYPEHINT) -> bool:
		return self.legacy == get_legacy_instance(other)
	
	def __hash__(self) -> int:
		return self.legacy.__hash__()
	
	def __ne__(self, other: WEB_ELEMENT_TYPEHINT) -> bool:
		return self.legacy != get_legacy_instance(other)
	
	async def accessible_name(self) -> str:
		return await self._wrap_to_trio(lambda: self.legacy.accessible_name)
	
	async def aria_role(self) -> str:
		return await self._wrap_to_trio(lambda: self.legacy.aria_role)
	
	async def clear(self) -> None:
		await self._wrap_to_trio(self.legacy.clear)
	
	async def click(self) -> None:
		await self._wrap_to_trio(self.legacy.click)
	
	@classmethod
	def from_legacy(
			cls,
			selenium_web_element: WEB_ELEMENT_TYPEHINT,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> Self:
		"""
		Creates an instance from a legacy Selenium WebElement object.

		This factory method is used to wrap an existing Selenium WebElement
		instance into the new interface.

		Args:
			selenium_web_element (WEB_ELEMENT_TYPEHINT): The legacy Selenium WebElement instance or its wrapper.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.

		Returns:
			Self: A new instance of a class implementing WebElement.
		"""
		
		legacy_element_obj = get_legacy_instance(selenium_web_element)
		
		if not isinstance(legacy_element_obj, legacyWebElement):
			raise TypesConvertError(from_=legacyWebElement, to_=selenium_web_element)
		
		return cls(selenium_web_element=legacy_element_obj, lock=lock, limiter=limiter)
	
	async def find_element(self, by: str = By.ID, value: Any = None) -> Self:
		impl_el = await self._wrap_to_trio(self.legacy.find_element, by=by, value=value)
		return self.from_legacy(
				selenium_web_element=impl_el,
				lock=self._lock,
				limiter=self._capacity_limiter
		)
	
	async def find_elements(self, by: str = By.ID, value: Any = None) -> List[Self]:
		impl_list = await self._wrap_to_trio(self.legacy.find_elements, by=by, value=value)
		return [
			self.from_legacy(
					selenium_web_element=e,
					lock=self._lock,
					limiter=self._capacity_limiter
			) for e in impl_list
		]
	
	async def get_attribute(self, name: str) -> Optional[str]:
		return await self._wrap_to_trio(self.legacy.get_attribute, name=name)
	
	async def get_dom_attribute(self, name: str) -> Optional[str]:
		return await self._wrap_to_trio(self.legacy.get_dom_attribute, name=name)
	
	async def get_property(self, name: str) -> Any:
		return await self._wrap_to_trio(self.legacy.get_property, name=name)
	
	async def id(self) -> str:
		return await self._wrap_to_trio(lambda: self.legacy.id)
	
	async def is_displayed(self) -> bool:
		return await self._wrap_to_trio(self.legacy.is_displayed)
	
	async def is_enabled(self) -> bool:
		return await self._wrap_to_trio(self.legacy.is_enabled)
	
	async def is_selected(self) -> bool:
		return await self._wrap_to_trio(self.legacy.is_selected)
	
	async def location(self) -> Dict:
		return await self._wrap_to_trio(lambda: self.legacy.location)
	
	async def location_once_scrolled_into_view(self) -> Dict:
		return await self._wrap_to_trio(lambda: self.legacy.location_once_scrolled_into_view)
	
	async def parent(self) -> Self:
		impl_parent = await self._wrap_to_trio(lambda: self.legacy.parent)
		return self.from_legacy(impl_parent, lock=self._lock, limiter=self._capacity_limiter)
	
	async def rect(self) -> Dict:
		return await self._wrap_to_trio(lambda: self.legacy.rect)
	
	async def screenshot(self, filename: str) -> bool:
		return await self._wrap_to_trio(self.legacy.screenshot, filename=filename)
	
	async def screenshot_as_base64(self) -> str:
		return await self._wrap_to_trio(lambda: self.legacy.screenshot_as_base64)
	
	async def screenshot_as_png(self) -> bytes:
		return await self._wrap_to_trio(lambda: self.legacy.screenshot_as_png)
	
	async def send_keys(self, *value: str) -> None:
		await self._wrap_to_trio(self.legacy.send_keys, *value)
	
	async def session_id(self) -> str:
		return await self._wrap_to_trio(lambda: self.legacy.session_id)
	
	async def shadow_root(self) -> ShadowRoot:
		return ShadowRoot(
				await self._wrap_to_trio(lambda: self.legacy.shadow_root),
				lock=self._lock,
				limiter=self._capacity_limiter
		)
	
	async def size(self) -> Dict:
		return await self._wrap_to_trio(lambda: self.legacy.size)
	
	async def submit(self) -> None:
		await self._wrap_to_trio(self.legacy.submit)
	
	async def tag_name(self) -> str:
		return await self._wrap_to_trio(lambda: self.legacy.tag_name)
	
	async def text(self) -> str:
		return await self._wrap_to_trio(lambda: self.legacy.text)
	
	async def value_of_css_property(self, property_name: str) -> str:
		return await self._wrap_to_trio(self.legacy.value_of_css_property, property_name=property_name)
