import trio
from selenium.webdriver.common.by import By
from osn_selenium.trio_base_mixin import _TrioThreadMixin
from osn_selenium.instances.types import SHADOW_ROOT_TYPEHINT
from typing import (
	List,
	Optional,
	Self,
	TYPE_CHECKING
)
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.abstract.instances.shadow_root import AbstractShadowRoot
from osn_selenium.instances.errors import (
	ExpectedTypeError,
	TypesConvertError
)
from selenium.webdriver.remote.shadowroot import (
	ShadowRoot as legacyShadowRoot
)


if TYPE_CHECKING:
	from osn_selenium.instances.trio_threads.web_element import WebElement


class ShadowRoot(_TrioThreadMixin, AbstractShadowRoot):
	"""
	Wrapper for the legacy Selenium ShadowRoot instance.

	Represents the root of a Shadow DOM tree, allowing element search
	within the encapsulated shadow scope.
	"""
	
	def __init__(
			self,
			selenium_shadow_root: legacyShadowRoot,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> None:
		"""
		Initializes the ShadowRoot wrapper.

		Args:
			selenium_shadow_root (legacyShadowRoot): The legacy Selenium ShadowRoot instance to wrap.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.
		"""
		
		super().__init__(lock=lock, limiter=limiter)
		
		if not isinstance(selenium_shadow_root, legacyShadowRoot):
			raise ExpectedTypeError(
					expected_class=legacyShadowRoot,
					received_instance=selenium_shadow_root
			)
		
		self._selenium_shadow_root = selenium_shadow_root
	
	async def find_element(self, by: str = By.ID, value: Optional[str] = None) -> "WebElement":
		impl_el = await self._wrap_to_trio(self.legacy.find_element, by=by, value=value)
		
		from osn_selenium.instances.trio_threads.web_element import WebElement

		return WebElement.from_legacy(impl_el, lock=self._lock, limiter=self._capacity_limiter)
	
	async def find_elements(self, by: str = By.ID, value: Optional[str] = None) -> List["WebElement"]:
		impl_list = await self._wrap_to_trio(self.legacy.find_elements, by=by, value=value)
		
		from osn_selenium.instances.trio_threads.web_element import WebElement

		return [
			WebElement.from_legacy(e, lock=self._lock, limiter=self._capacity_limiter) for e in impl_list
		]
	
	@classmethod
	def from_legacy(
			cls,
			selenium_shadow_root: SHADOW_ROOT_TYPEHINT,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> Self:
		"""
		Creates an instance from a legacy Selenium ShadowRoot object.

		This factory method is used to wrap an existing Selenium ShadowRoot
		instance into the new interface.

		Args:
			selenium_shadow_root (SHADOW_ROOT_TYPEHINT): The legacy Selenium ShadowRoot instance or its wrapper.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.

		Returns:
			Self: A new instance of a class implementing ShadowRoot.
		"""
		
		legacy_shadow_root_obj = get_legacy_instance(selenium_shadow_root)
		
		if not isinstance(legacy_shadow_root_obj, legacyShadowRoot):
			raise TypesConvertError(from_=legacyShadowRoot, to_=selenium_shadow_root)
		
		return cls(
				selenium_shadow_root=legacy_shadow_root_obj,
				lock=lock,
				limiter=limiter
		)
	
	async def id(self) -> str:
		return await self._wrap_to_trio(lambda: self.legacy.id)
	
	@property
	def legacy(self) -> legacyShadowRoot:
		return self._selenium_shadow_root
