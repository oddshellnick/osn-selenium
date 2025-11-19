from typing import Any, Callable, Self
from osn_selenium.abstract.instances.script import AbstractScript
from selenium.webdriver.common.bidi.script import (
	Script as legacyScript
)


class Script(AbstractScript):
	def __init__(self, selenium_script: legacyScript,) -> None:
		self._selenium_script = selenium_script
	
	def add_console_message_handler(self, handler: Callable[[Any], None],) -> int:
		return self.legacy.add_console_message_handler(handler=handler)
	
	def add_javascript_error_handler(self, handler: Callable[[Any], None],) -> int:
		return self.legacy.add_javascript_error_handler(handler=handler)
	
	def execute(self, script: str, *args: Any) -> Any:
		return self.legacy.execute(script, *args)
	
	@classmethod
	def from_legacy(cls, selenium_script: legacyScript,) -> Self:
		"""
		Creates an instance from a legacy Selenium Script object.

		This factory method is used to wrap an existing Selenium Script
		instance into the new interface.

		Args:
			selenium_script (legacyScript): The legacy Selenium Script instance.

		Returns:
			Self: A new instance of a class implementing Script.
		"""
		
		return cls(selenium_script=selenium_script)
	
	@property
	def legacy(self) -> legacyScript:
		return self._selenium_script
	
	def pin(self, script: str) -> str:
		return self.legacy.pin(script=script)
	
	def remove_console_message_handler(self, id: int) -> None:
		self.legacy.remove_console_message_handler(id=id)
	
	def unpin(self, script_id: str) -> None:
		self.legacy.unpin(script_id=script_id)
