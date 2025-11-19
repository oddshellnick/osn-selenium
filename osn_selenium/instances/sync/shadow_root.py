from selenium.webdriver.common.by import By
from typing import (
	List,
	Optional,
	Self,
	TYPE_CHECKING
)
from osn_selenium.instances.sync.web_element import WebElement
from osn_selenium.abstract.instances.shadow_root import AbstractShadowRoot
from selenium.webdriver.remote.shadowroot import (
	ShadowRoot as legacyShadowRoot
)


if TYPE_CHECKING:
	from osn_selenium.instances.sync.web_element import WebElement


class ShadowRoot(AbstractShadowRoot):
	def __init__(self, selenium_shadow_root: legacyShadowRoot,) -> None:
		self._selenium_shadow_root = selenium_shadow_root
	
	def find_element(self, by: str = By.ID, value: Optional[str] = None,) -> "WebElement":
		impl_el = self.legacy.find_element(by=by, value=value)
		return WebElement.from_legacy(selenium_web_element=impl_el)
	
	def find_elements(self, by: str = By.ID, value: Optional[str] = None,) -> List["WebElement"]:
		impl_list = self.legacy.find_elements(by=by, value=value)
		return [WebElement.from_legacy(selenium_web_element=e) for e in impl_list]
	
	@classmethod
	def from_legacy(cls, selenium_shadow_root: legacyShadowRoot,) -> Self:
		"""
		Creates an instance from a legacy Selenium ShadowRoot object.

		This factory method is used to wrap an existing Selenium ShadowRoot
		instance into the new interface.

		Args:
			selenium_shadow_root (legacyShadowRoot): The legacy Selenium ShadowRoot instance.

		Returns:
			Self: A new instance of a class implementing ShadowRoot.
		"""
		
		return cls(selenium_shadow_root=selenium_shadow_root)
	
	def id(self) -> str:
		return self.legacy.id
	
	@property
	def legacy(self) -> legacyShadowRoot:
		return self._selenium_shadow_root
