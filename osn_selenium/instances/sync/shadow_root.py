from selenium.webdriver.common.by import By
from osn_selenium.instances.errors import CannotConvertTypeError
from typing import (
	List,
	Optional,
	Self,
	TYPE_CHECKING
)
from osn_selenium.instances._typehints import SHADOW_ROOT_TYPEHINT
from osn_selenium.instances.unified.shadow_root import UnifiedShadowRoot
from osn_selenium.abstract.instances.shadow_root import AbstractShadowRoot
from selenium.webdriver.remote.shadowroot import (
	ShadowRoot as legacyShadowRoot
)
from osn_selenium.instances.convert import (
	get_legacy_instance,
	get_sync_instance_wrapper
)


__all__ = ["ShadowRoot"]

if TYPE_CHECKING:
	from osn_selenium.instances.sync.web_element import WebElement


class ShadowRoot(UnifiedShadowRoot, AbstractShadowRoot):
	"""
	Wrapper for the legacy Selenium ShadowRoot instance.

	Represents the root of a Shadow DOM tree, allowing element search
	within the encapsulated shadow scope.
	"""
	
	def __init__(self, selenium_shadow_root: legacyShadowRoot) -> None:
		"""
		Initializes the ShadowRoot wrapper.

		Args:
			selenium_shadow_root (legacyShadowRoot): The legacy Selenium ShadowRoot instance to wrap.
		"""
		
		UnifiedShadowRoot.__init__(self, selenium_shadow_root=selenium_shadow_root)
	
	def find_element(self, by: str = By.ID, value: Optional[str] = None) -> "WebElement":
		legacy_element = self._find_element_impl(by=by, value=value)
		
		from osn_selenium.instances.sync.web_element import WebElement
		
		return get_sync_instance_wrapper(wrapper_class=WebElement, legacy_object=legacy_element)
	
	def find_elements(self, by: str = By.ID, value: Optional[str] = None) -> List["WebElement"]:
		legacy_elements = self._find_elements_impl(by=by, value=value)
		
		from osn_selenium.instances.sync.web_element import WebElement
		
		return [
			get_sync_instance_wrapper(wrapper_class=WebElement, legacy_object=legacy_element)
			for legacy_element in legacy_elements
		]
	
	@classmethod
	def from_legacy(cls, legacy_object: SHADOW_ROOT_TYPEHINT) -> Self:
		"""
		Creates an instance from a legacy Selenium ShadowRoot object.

		This factory method is used to wrap an existing Selenium ShadowRoot
		instance into the new interface.

		Args:
			legacy_object (SHADOW_ROOT_TYPEHINT): The legacy Selenium ShadowRoot instance or its wrapper.

		Returns:
			Self: A new instance of a class implementing ShadowRoot.
		"""
		
		legacy_shadow_root_obj = get_legacy_instance(instance=legacy_object)
		
		if not isinstance(legacy_shadow_root_obj, legacyShadowRoot):
			raise CannotConvertTypeError(from_=legacyShadowRoot, to_=legacy_object)
		
		return cls(selenium_shadow_root=legacy_shadow_root_obj)
	
	def id(self) -> str:
		return self._id_impl()
	
	@property
	def legacy(self) -> legacyShadowRoot:
		return self._legacy_impl
