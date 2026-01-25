from typing import Any, List, Optional
from osn_selenium.instances.sync.script import Script
from osn_selenium.instances.convert import (
	get_sync_instance_wrapper
)
from osn_selenium.webdrivers._args_helpers import (
	unwrap_args,
	wrap_sync_args
)
from osn_selenium.webdrivers.unified.core.script import (
	UnifiedCoreScriptMixin
)
from osn_selenium.abstract.webdriver.core.script import (
	AbstractCoreScriptMixin
)


__all__ = ["CoreScriptMixin"]


class CoreScriptMixin(UnifiedCoreScriptMixin, AbstractCoreScriptMixin):
	"""
	Mixin for JavaScript execution and management in Core WebDrivers.

	Allows execution of synchronous and asynchronous JavaScript, as well as
	pinning scripts for repeated use.
	"""
	
	def execute_async_script(self, script: str, *args: Any) -> Any:
		unwrapped = unwrap_args(args=args)
		result = self._execute_async_script_impl(script, *unwrapped)
		
		return wrap_sync_args(args=result)
	
	def execute_script(self, script: str, *args: Any) -> Any:
		unwrapped = unwrap_args(args=args)
		result = self._execute_script_impl(script, *unwrapped)
		
		return wrap_sync_args(args=result)
	
	def get_pinned_scripts(self) -> List[str]:
		return self._get_pinned_scripts_impl()
	
	def pin_script(self, script: str, script_key: Optional[Any] = None) -> Any:
		return self._pin_script_impl(script=script, script_key=script_key)
	
	def script(self) -> Script:
		legacy = self._script_impl()
		
		return get_sync_instance_wrapper(wrapper_class=Script, legacy_object=legacy)
	
	def unpin(self, script_key: Any) -> None:
		self._unpin_impl(script_key=script_key)
