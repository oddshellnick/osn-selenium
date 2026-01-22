from typing import Any, List, Optional
from osn_selenium.instances.trio_threads.script import Script
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.webdrivers.trio_threads.core.base import CoreBaseMixin
from osn_selenium.instances.convert import (
	get_trio_thread_instance_wrapper
)
from osn_selenium.abstract.webdriver.core.script import (
	AbstractCoreScriptMixin
)
from osn_selenium.webdrivers._functions import (
	unwrap_args,
	wrap_trio_thread_args
)


class CoreScriptMixin(CoreBaseMixin, AbstractCoreScriptMixin):
	"""
	Mixin for JavaScript execution and management in Core WebDrivers.

	Allows execution of synchronous and asynchronous JavaScript, as well as
	pinning scripts for repeated use.
	"""
	
	@requires_driver
	async def execute_async_script(self, script: str, *args: Any) -> Any:
		args = unwrap_args(args)
		
		return wrap_trio_thread_args(
				await self.sync_to_trio(sync_function=self.driver.execute_async_script)(script, *args),
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	@requires_driver
	async def execute_script(self, script: str, *args: Any) -> Any:
		args = unwrap_args(args)
		
		return wrap_trio_thread_args(
				await self.sync_to_trio(sync_function=self.driver.execute_script)(script, *args),
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	@requires_driver
	async def get_pinned_scripts(self) -> List[str]:
		return await self.sync_to_trio(sync_function=self.driver.get_pinned_scripts)()
	
	@requires_driver
	async def pin_script(self, script: str, script_key: Optional[Any] = None) -> Any:
		return await self.sync_to_trio(sync_function=self.driver.pin_script)(script=script, script_key=script_key)
	
	@requires_driver
	async def script(self) -> Script:
		legacy = await self.sync_to_trio(sync_function=lambda: self.driver.script)()
		
		return get_trio_thread_instance_wrapper(
				wrapper_class=Script,
				legacy_object=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	@requires_driver
	async def unpin(self, script_key: Any) -> None:
		await self.sync_to_trio(sync_function=self.driver.unpin)(script_key=script_key)
