from typing import (
	Optional,
	Self,
	Union
)
from osn_selenium.instances.sync.alert import Alert
from osn_selenium.instances.errors import TypesConvertError
from osn_selenium.instances.sync.web_element import WebElement
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.instances.unified.switch_to import UnifiedSwitchTo
from osn_selenium.abstract.instances.switch_to import AbstractSwitchTo
from selenium.webdriver.remote.switch_to import (
	SwitchTo as legacySwitchTo
)
from osn_selenium.instances.types import (
	SWITCH_TO_TYPEHINT,
	WEB_ELEMENT_TYPEHINT
)


class SwitchTo(UnifiedSwitchTo, AbstractSwitchTo):
	"""
	Wrapper for the legacy Selenium SwitchTo instance.

	Provides mechanisms to change the driver's focus to different frames,
	windows, or alerts.
	"""
	
	def __init__(self, selenium_switch_to: legacySwitchTo) -> None:
		"""
		Initializes the SwitchTo wrapper.

		Args:
			selenium_switch_to (legacySwitchTo): The legacy Selenium SwitchTo instance to wrap.
		"""
		
		UnifiedSwitchTo.__init__(self, selenium_switch_to=selenium_switch_to)
	
	def active_element(self) -> WebElement:
		return WebElement.from_legacy(selenium_web_element=self._active_element_impl())
	
	def alert(self) -> Alert:
		return Alert(selenium_alert=self._alert_impl())
	
	def default_content(self) -> None:
		self._default_content_impl()
	
	def frame(self, frame_reference: Union[str, int, WEB_ELEMENT_TYPEHINT]) -> None:
		self._frame_impl(frame_reference=frame_reference)
	
	@classmethod
	def from_legacy(cls, selenium_switch_to: SWITCH_TO_TYPEHINT) -> Self:
		"""
		Creates an instance from a legacy Selenium SwitchTo object.

		This factory method is used to wrap an existing Selenium SwitchTo
		instance into the new interface.

		Args:
			selenium_switch_to (SWITCH_TO_TYPEHINT): The legacy Selenium SwitchTo instance or its wrapper.

		Returns:
			Self: A new instance of a class implementing SwitchTo.
		"""
		
		legacy_switch_to_obj = get_legacy_instance(selenium_switch_to)
		
		if not isinstance(legacy_switch_to_obj, legacySwitchTo):
			raise TypesConvertError(from_=legacySwitchTo, to_=selenium_switch_to)
		
		return cls(selenium_switch_to=legacy_switch_to_obj)
	
	@property
	def legacy(self) -> legacySwitchTo:
		return self._legacy_impl
	
	def new_window(self, type_hint: Optional[str] = None) -> None:
		self._new_window_impl(type_hint=type_hint)
	
	def parent_frame(self) -> None:
		self._parent_frame_impl()
	
	def window(self, window_name: str) -> None:
		self._window_impl(window_name=window_name)
