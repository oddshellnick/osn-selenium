from typing import Optional, Union
from selenium.webdriver.common.alert import Alert as legacyAlert
from osn_selenium.exceptions.instance import NotExpectedTypeError
from osn_selenium.instances._typehints import WEB_ELEMENT_TYPEHINT
from osn_selenium.instances.convert import (
	get_legacy_frame_reference
)
from selenium.webdriver.remote.switch_to import (
	SwitchTo as legacySwitchTo
)
from selenium.webdriver.remote.webelement import (
	WebElement as legacyWebElement
)


__all__ = ["UnifiedSwitchTo"]


class UnifiedSwitchTo:
	def __init__(self, selenium_switch_to: legacySwitchTo):
		if not isinstance(selenium_switch_to, legacySwitchTo):
			raise NotExpectedTypeError(expected_type=legacySwitchTo, received_instance=selenium_switch_to)
		
		self._selenium_switch_to = selenium_switch_to
	
	def _active_element_impl(self) -> legacyWebElement:
		return self._legacy_impl.active_element
	
	def _alert_impl(self) -> legacyAlert:
		return self._legacy_impl.alert
	
	def _default_content_impl(self) -> None:
		self._legacy_impl.default_content()
	
	def _frame_impl(self, frame_reference: Union[str, int, WEB_ELEMENT_TYPEHINT]) -> None:
		self._legacy_impl.frame(frame_reference=get_legacy_frame_reference(frame_reference))
	
	@property
	def _legacy_impl(self) -> legacySwitchTo:
		return self._selenium_switch_to
	
	def _new_window_impl(self, type_hint: Optional[str] = None) -> None:
		self._legacy_impl.new_window(type_hint=type_hint)
	
	def _parent_frame_impl(self) -> None:
		self._legacy_impl.parent_frame()
	
	def _window_impl(self, window_name: str) -> None:
		self._legacy_impl.window(window_name=window_name)
