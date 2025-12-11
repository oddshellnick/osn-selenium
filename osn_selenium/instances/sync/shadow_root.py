from selenium.webdriver.common.by import By
from osn_selenium.instances.types import SHADOW_ROOT_TYPEHINT
from typing import (
	List,
	Optional,
	Self,
	TYPE_CHECKING
)
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.instances.sync.web_element import WebElement
from osn_selenium.abstract.instances.shadow_root import AbstractShadowRoot
from selenium.webdriver.remote.shadowroot import (
	ShadowRoot as legacyShadowRoot
)


if TYPE_CHECKING:
	from osn_selenium.instances.sync.web_element import WebElement


class ShadowRoot(AbstractShadowRoot):
	def __init__(self, selenium_shadow_root: legacyShadowRoot) -> None:
		if not isinstance(selenium_shadow_root, legacyShadowRoot):
			raise TypeError(f"Expected {type(legacyShadowRoot)}, got {type(selenium_shadow_root)}")
		
		self._selenium_shadow_root = selenium_shadow_root
	
	def find_element(self, by: str = By.ID, value: Optional[str] = None) -> "WebElement":
		impl_el = self.legacy.find_element(by=by, value=value)
		
		return WebElement.from_legacy(selenium_web_element=impl_el)
	
	def find_elements(self, by: str = By.ID, value: Optional[str] = None) -> List["WebElement"]:
		impl_list = self.legacy.find_elements(by=by, value=value)
		
		return [WebElement.from_legacy(selenium_web_element=e) for e in impl_list]
	
	@classmethod
	def from_legacy(cls, selenium_shadow_root: SHADOW_ROOT_TYPEHINT) -> Self:
		legacy_shadow_root_obj = get_legacy_instance(selenium_shadow_root)
		
		if not isinstance(legacy_shadow_root_obj, legacyShadowRoot):
			raise TypeError(
					f"Could not convert input to {type(legacyShadowRoot)}: {type(selenium_shadow_root)}"
			)
		
		return cls(selenium_shadow_root=legacy_shadow_root_obj)
	
	def id(self) -> str:
		return self.legacy.id
	
	@property
	def legacy(self) -> legacyShadowRoot:
		return self._selenium_shadow_root
