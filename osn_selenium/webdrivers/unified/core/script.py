from typing import Any, List, Optional
from osn_selenium.webdrivers._decorators import requires_driver
from osn_selenium.webdrivers.unified.core.base import UnifiedCoreBaseMixin


__all__ = ["UnifiedCoreScriptMixin"]


class UnifiedCoreScriptMixin(UnifiedCoreBaseMixin):
	@requires_driver
	def _execute_async_script_impl(self, script: str, *args: Any) -> Any:
		return self._driver_impl.execute_async_script(script, *args)
	
	@requires_driver
	def _execute_script_impl(self, script: str, *args: Any) -> Any:
		return self._driver_impl.execute_script(script, *args)
	
	@requires_driver
	def _get_pinned_scripts_impl(self) -> List[str]:
		return self._driver_impl.get_pinned_scripts()
	
	@requires_driver
	def _pin_script_impl(self, script: str, script_key: Optional[Any] = None) -> Any:
		return self._driver_impl.pin_script(script=script, script_key=script_key)
	
	@requires_driver
	def _script_impl(self) -> Any:
		return self._driver_impl.script
	
	@requires_driver
	def _unpin_impl(self, script_key: Any) -> None:
		self._driver_impl.unpin(script_key=script_key)
