from typing import Any, List, Optional
from osn_selenium.instances.sync.script import Script
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.webdrivers.sync.core.base import CoreBaseMixin
from osn_selenium.instances.convert import (
	get_sync_instance_wrapper
)
from osn_selenium.webdrivers._functions import (
	unwrap_args,
	wrap_sync_args
)
from osn_selenium.abstract.webdriver.core.script import (
	AbstractCoreScriptMixin
)


class CoreScriptMixin(CoreBaseMixin, AbstractCoreScriptMixin):
	"""
	Mixin for JavaScript execution and management in Core WebDrivers.

	Allows execution of synchronous and asynchronous JavaScript, as well as
	pinning scripts for repeated use.
	"""
	
	@requires_driver
	def execute_async_script(self, script: str, *args: Any) -> Any:
		args = unwrap_args(args)
		
		return wrap_sync_args(self.driver.execute_async_script(script, *args))
	
	@requires_driver
	def execute_script(self, script: str, *args: Any) -> Any:
		args = unwrap_args(args)
		
		return wrap_sync_args(self.driver.execute_script(script, *args))
	
	@requires_driver
	def get_pinned_scripts(self) -> List[str]:
		return self.driver.get_pinned_scripts()
	
	@requires_driver
	def pin_script(self, script: str, script_key: Optional[Any] = None) -> Any:
		return self.driver.pin_script(script=script, script_key=script_key)
	
	@requires_driver
	def script(self) -> Script:
		legacy = self.driver.script
		
		return get_sync_instance_wrapper(wrapper_class=Script, legacy_object=legacy)
	
	@requires_driver
	def unpin(self, script_key: Any) -> None:
		self.driver.unpin(script_key=script_key)
