from typing import (
	Any,
	Dict,
	List,
	Optional
)
from osn_selenium.instances.sync.script import Script
from osn_selenium.webdrivers.sync.base.base import BaseMixin
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.abstract.webdriver.base.script import AbstractScriptMixin


class ScriptMixin(BaseMixin, AbstractScriptMixin):
	@requires_driver
	def execute_async_script(self, script: str, *args: Any) -> Any:
		args = self._unwrap_args(args)
		
		return self._wrap_result(result=self.driver.execute_async_script(script, *args))
	
	@requires_driver
	def execute_script(self, script: str, *args: Any) -> Any:
		args = self._unwrap_args(args)
		
		return self._wrap_result(result=self.driver.execute_script(script, *args))
	
	@requires_driver
	def get_pinned_scripts(self) -> List[str]:
		return self.driver.get_pinned_scripts()
	
	@requires_driver
	def pin_script(self, script: str, script_key: Optional[Any] = None) -> Any:
		return self.driver.pin_script(script=script, script_key=script_key)
	
	@requires_driver
	def script(self) -> Script:
		legacy = self.driver.script
		
		return Script(selenium_script=legacy)
	
	@requires_driver
	def unpin(self, script_key: Any) -> None:
		self.driver.unpin(script_key=script_key)
