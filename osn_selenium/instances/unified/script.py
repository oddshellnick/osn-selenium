from typing import Any, Callable
from osn_selenium.exceptions.instance import NotExpectedTypeError
from selenium.webdriver.common.bidi.script import (
	Script as legacyScript
)


__all__ = ["UnifiedScript"]


class UnifiedScript:
	def __init__(self, selenium_script: legacyScript):
		if not isinstance(selenium_script, legacyScript):
			raise NotExpectedTypeError(expected_type=legacyScript, received_instance=selenium_script)
		
		self._selenium_script = selenium_script
	
	def _add_console_message_handler_impl(self, handler: Callable[[Any], None]) -> int:
		return self._legacy_impl.add_console_message_handler(handler=handler)
	
	def _add_javascript_error_handler_impl(self, handler: Callable[[Any], None]) -> int:
		return self._legacy_impl.add_javascript_error_handler(handler=handler)
	
	def _execute_impl(self, script: str, *args: Any) -> Any:
		return self._legacy_impl.execute(script, *args)
	
	@property
	def _legacy_impl(self) -> legacyScript:
		return self._selenium_script
	
	def _pin_impl(self, script: str) -> str:
		return self._legacy_impl.pin(script=script)
	
	def _remove_console_message_handler_impl(self, id: int) -> None:
		self._legacy_impl.remove_console_message_handler(id=id)
	
	def _unpin_impl(self, script_id: str) -> None:
		self._legacy_impl.unpin(script_id=script_id)
