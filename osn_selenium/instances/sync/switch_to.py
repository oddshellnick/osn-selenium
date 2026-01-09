from typing import (
	Optional,
	Self,
	Union
)
from osn_selenium.instances.sync.alert import Alert
from osn_selenium.instances.sync.web_element import WebElement
from osn_selenium.abstract.instances.switch_to import AbstractSwitchTo
from selenium.webdriver.remote.switch_to import (
	SwitchTo as legacySwitchTo
)
from osn_selenium.instances.errors import (
	ExpectedTypeError,
	TypesConvertError
)
from osn_selenium.instances.types import (
	SWITCH_TO_TYPEHINT,
	WEB_ELEMENT_TYPEHINT
)
from osn_selenium.instances.convert import (
	get_legacy_frame_reference,
	get_legacy_instance
)


class SwitchTo(AbstractSwitchTo):
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
		
		if not isinstance(selenium_switch_to, legacySwitchTo):
			raise ExpectedTypeError(expected_class=legacySwitchTo, received_instance=selenium_switch_to)
		
		self._selenium_switch_to = selenium_switch_to
	
	def active_element(self) -> WebElement:
		return WebElement.from_legacy(selenium_web_element=self.legacy.active_element)
	
	def alert(self) -> Alert:
		return Alert(selenium_alert=self.legacy.alert)
	
	def default_content(self) -> None:
		self.legacy.default_content()
	
	def frame(self, frame_reference: Union[str, int, WEB_ELEMENT_TYPEHINT]) -> None:
		self.legacy.frame(frame_reference=get_legacy_frame_reference(frame_reference))
	
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
		return self._selenium_switch_to
	
	def new_window(self, type_hint: Optional[str] = None) -> None:
		self.legacy.new_window(type_hint=type_hint)
	
	def parent_frame(self) -> None:
		self.legacy.parent_frame()
	
	def window(self, window_name: str) -> None:
		self.legacy.window(window_name=window_name)
