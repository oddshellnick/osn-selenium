from typing import Any, Callable, Self
from osn_selenium.instances.types import SCRIPT_TYPEHINT
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.abstract.instances.script import AbstractScript
from selenium.webdriver.common.bidi.script import (
	Script as legacyScript
)


class Script(AbstractScript):
	def __init__(self, selenium_script: legacyScript) -> None:
		if not isinstance(selenium_script, legacyScript):
			raise TypeError(f"Expected {type(legacyScript)}, got {type(selenium_script)}")
		
		self._selenium_script = selenium_script
	
	def add_console_message_handler(self, handler: Callable[[Any], None]) -> int:
		return self.legacy.add_console_message_handler(handler=handler)
	
	def add_javascript_error_handler(self, handler: Callable[[Any], None]) -> int:
		return self.legacy.add_javascript_error_handler(handler=handler)
	
	def execute(self, script: str, *args: Any) -> Any:
		return self.legacy.execute(script, *args)
	
	@classmethod
	def from_legacy(cls, selenium_script: SCRIPT_TYPEHINT) -> Self:
		legacy_script_obj = get_legacy_instance(selenium_script)
		
		if not isinstance(legacy_script_obj, legacyScript):
			raise TypeError(
					f"Could not convert input to {type(legacyScript)}: {type(selenium_script)}"
			)
		
		return cls(selenium_script=legacy_script_obj)
	
	@property
	def legacy(self) -> legacyScript:
		return self._selenium_script
	
	def pin(self, script: str) -> str:
		return self.legacy.pin(script=script)
	
	def remove_console_message_handler(self, id: int) -> None:
		self.legacy.remove_console_message_handler(id=id)
	
	def unpin(self, script_id: str) -> None:
		self.legacy.unpin(script_id=script_id)
