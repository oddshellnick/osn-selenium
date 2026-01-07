from typing import (
	Any,
	Dict,
	List,
	Optional
)
from osn_selenium.instances.trio_threads.script import Script
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.webdrivers.trio_threads.base.base import BaseMixin
from osn_selenium.abstract.webdriver.base.script import AbstractScriptMixin


class ScriptMixin(BaseMixin, AbstractScriptMixin):
	@requires_driver
	async def execute_async_script(self, script: str, *args: Any) -> Any:
		args = self._unwrap_args(args)
		
		return self._wrap_result(
				result=await self._wrap_to_trio(self.driver.execute_async_script, script, *args)
		)
	
	@requires_driver
	async def execute_script(self, script: str, *args: Any) -> Any:
		args = self._unwrap_args(args)
		
		return self._wrap_result(
				result=await self._wrap_to_trio(self.driver.execute_script, script, *args)
		)
	
	@requires_driver
	async def get_pinned_scripts(self) -> List[str]:
		return await self._wrap_to_trio(self.driver.get_pinned_scripts)
	
	@requires_driver
	async def pin_script(self, script: str, script_key: Optional[Any] = None) -> Any:
		return await self._wrap_to_trio(self.driver.pin_script, script=script, script_key=script_key)
	
	@requires_driver
	async def script(self) -> Script:
		legacy = await self._wrap_to_trio(lambda: self.driver.script)
		
		return Script(
				selenium_script=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	@requires_driver
	async def unpin(self, script_key: Any) -> None:
		await self._wrap_to_trio(self.driver.unpin, script_key=script_key)
