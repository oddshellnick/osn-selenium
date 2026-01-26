import trio
from selenium.webdriver.common.by import By
from osn_selenium.trio_threads_mixin import TrioThreadMixin
from osn_selenium.instances._typehints import SHADOW_ROOT_TYPEHINT
from typing import (
	List,
	Optional,
	Self,
	TYPE_CHECKING,
	Type
)
from osn_selenium.exceptions.instance import (
	CannotConvertTypeError
)
from osn_selenium.instances.unified.shadow_root import UnifiedShadowRoot
from osn_selenium.abstract.instances.shadow_root import AbstractShadowRoot
from selenium.webdriver.remote.shadowroot import (
	ShadowRoot as legacyShadowRoot
)
from selenium.webdriver.remote.webelement import (
	WebElement as legacyWebElement
)
from osn_selenium.instances.convert import (
	get_legacy_instance,
	get_trio_thread_instance_wrapper
)


__all__ = ["ShadowRoot"]

if TYPE_CHECKING:
	from osn_selenium.instances.trio_threads.web_element import WebElement

_WEB_ELEMENT_TYPE: Optional[Type["WebElement"]] = None


def _build_web_element(
		legacy_element: legacyWebElement,
		lock: trio.Lock,
		limiter: trio.CapacityLimiter,
):
	"""
	Builds a wrapped WebElement from a legacy element.

	Args:
		legacy_element (legacyWebElement): The legacy Selenium WebElement instance.
		lock (trio.Lock): A Trio lock for managing concurrent access.
		limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.

	Returns:
		WebElement: The wrapped WebElement instance.
	"""
	
	global _WEB_ELEMENT_TYPE
	
	if _WEB_ELEMENT_TYPE is None:
		from osn_selenium.instances.trio_threads.web_element import WebElement
		_WEB_ELEMENT_TYPE = WebElement
	
	return get_trio_thread_instance_wrapper(
			wrapper_class=_WEB_ELEMENT_TYPE,
			legacy_object=legacy_element,
			lock=lock,
			limiter=limiter,
	)


class ShadowRoot(UnifiedShadowRoot, TrioThreadMixin, AbstractShadowRoot):
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
		
		UnifiedShadowRoot.__init__(self, selenium_shadow_root=selenium_shadow_root)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def find_element(self, by: str = By.ID, value: Optional[str] = None) -> "WebElement":
		legacy_element = await self.sync_to_trio(sync_function=self._find_element_impl)(by=by, value=value)
		
		return _build_web_element(
				legacy_element=legacy_element,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	async def find_elements(self, by: str = By.ID, value: Optional[str] = None) -> List["WebElement"]:
		legacy_elements = await self.sync_to_trio(sync_function=self._find_elements_impl)(by=by, value=value)
		
		return [
			_build_web_element(
					legacy_element=legacy_element,
					lock=self._lock,
					limiter=self._capacity_limiter,
			)
			for legacy_element in legacy_elements
		]
	
	@classmethod
	def from_legacy(
			cls,
			legacy_object: SHADOW_ROOT_TYPEHINT,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> Self:
		"""
		Creates an instance from a legacy Selenium ShadowRoot object.

		This factory method is used to wrap an existing Selenium ShadowRoot
		instance into the new interface.

		Args:
			legacy_object (SHADOW_ROOT_TYPEHINT): The legacy Selenium ShadowRoot instance or its wrapper.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.

		Returns:
			Self: A new instance of a class implementing ShadowRoot.
		"""
		
		legacy_shadow_root_obj = get_legacy_instance(instance=legacy_object)
		
		if not isinstance(legacy_shadow_root_obj, legacyShadowRoot):
			raise CannotConvertTypeError(from_=legacyShadowRoot, to_=legacy_object)
		
		return cls(
				selenium_shadow_root=legacy_shadow_root_obj,
				lock=lock,
				limiter=limiter
		)
	
	async def id(self) -> str:
		return await self.sync_to_trio(sync_function=self._id_impl)()
	
	@property
	def legacy(self) -> legacyShadowRoot:
		return self._legacy_impl
