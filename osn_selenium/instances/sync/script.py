from typing import Any, Callable, Self
from osn_selenium.instances._typehints import SCRIPT_TYPEHINT
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.instances.unified.script import UnifiedScript
from osn_selenium.abstract.instances.script import AbstractScript
from osn_selenium.exceptions.instance import (
	CannotConvertTypeError
)
from selenium.webdriver.common.bidi.script import (
	Script as legacyScript
)


__all__ = ["Script"]


class Script(UnifiedScript, AbstractScript):
	"""
	Wrapper for the legacy Selenium BiDi Script instance.

	Facilitates execution of JavaScript within specific contexts, adding preload scripts,
	and handling console messages or JS errors.
	"""
	
	def __init__(self, selenium_script: legacyScript) -> None:
		"""
		Initializes the Script wrapper.

		Args:
			selenium_script (legacyScript): The legacy Selenium Script instance to wrap.
		"""
		
		UnifiedScript.__init__(self, selenium_script=selenium_script)
	
	def add_console_message_handler(self, handler: Callable[[Any], None]) -> int:
		return self._add_console_message_handler_impl(handler=handler)
	
	def add_javascript_error_handler(self, handler: Callable[[Any], None]) -> int:
		return self._add_javascript_error_handler_impl(handler=handler)
	
	def execute(self, script: str, *args: Any) -> Any:
		return self._execute_impl(script, *args)
	
	@classmethod
	def from_legacy(cls, legacy_object: SCRIPT_TYPEHINT) -> Self:
		"""
		Creates an instance from a legacy Selenium Script object.

		This factory method is used to wrap an existing Selenium Script
		instance into the new interface.

		Args:
			legacy_object (SCRIPT_TYPEHINT): The legacy Selenium Script instance or its wrapper.

		Returns:
			Self: A new instance of a class implementing Script.
		"""
		
		legacy_script_obj = get_legacy_instance(instance=legacy_object)
		
		if not isinstance(legacy_script_obj, legacyScript):
			raise CannotConvertTypeError(from_=legacyScript, to_=legacy_object)
		
		return cls(selenium_script=legacy_script_obj)
	
	@property
	def legacy(self) -> legacyScript:
		return self._legacy_impl
	
	def pin(self, script: str) -> str:
		return self._pin_impl(script=script)
	
	def remove_console_message_handler(self, id: int) -> None:
		self._remove_console_message_handler_impl(id=id)
	
	def unpin(self, script_id: str) -> None:
		self._unpin_impl(script_id=script_id)
