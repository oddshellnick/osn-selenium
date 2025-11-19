from osn_selenium.instances.sync.alert import Alert
from typing import (
	Optional,
	Self,
	Union
)
from osn_selenium.instances.sync.web_element import WebElement
from osn_selenium.abstract.instances.switch_to import AbstractSwitchTo
from osn_selenium.abstract.instances.web_element import AbstractWebElement
from selenium.webdriver.remote.switch_to import (
	SwitchTo as legacySwitchTo
)


class SwitchTo(AbstractSwitchTo):
	def __init__(self, selenium_switch_to: legacySwitchTo,) -> None:
		self._selenium_switch_to = selenium_switch_to
	
	def active_element(self) -> WebElement:
		return WebElement.from_legacy(selenium_web_element=self.legacy.active_element)
	
	def alert(self) -> Alert:
		return Alert(selenium_alert=self.legacy.alert)
	
	def default_content(self) -> None:
		self.legacy.default_content()
	
	def frame(self, frame_reference: Union[str, int, AbstractWebElement],) -> None:
		self.legacy.frame(
				frame_reference=frame_reference.legacy
				if isinstance(frame_reference, AbstractWebElement)
				else frame_reference
		)
	
	@classmethod
	def from_legacy(cls, selenium_switch_to: legacySwitchTo,) -> Self:
		"""
		Creates an instance from a legacy Selenium SwitchTo object.

		This factory method is used to wrap an existing Selenium SwitchTo
		instance into the new interface.

		Args:
			selenium_switch_to (legacySwitchTo): The legacy Selenium SwitchTo instance.

		Returns:
			Self: A new instance of a class implementing SwitchTo.
		"""
		
		return cls(selenium_switch_to=selenium_switch_to)
	
	@property
	def legacy(self) -> legacySwitchTo:
		return self._selenium_switch_to
	
	def new_window(self, type_hint: Optional[str] = None,) -> None:
		self.legacy.new_window(type_hint=type_hint)
	
	def parent_frame(self) -> None:
		self.legacy.parent_frame()
	
	def window(self, window_name: str,) -> None:
		self.legacy.window(window_name=window_name)
