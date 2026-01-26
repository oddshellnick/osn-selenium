from typing import Any, List, Optional
from osn_selenium.trio_threads_mixin import TrioThreadMixin
from osn_selenium.instances.trio_threads.script import Script
from osn_selenium.instances.convert import (
	get_trio_thread_instance_wrapper
)
from osn_selenium.webdrivers.unified.core.script import (
	UnifiedCoreScriptMixin
)
from osn_selenium.abstract.webdriver.core.script import (
	AbstractCoreScriptMixin
)
from osn_selenium.webdrivers._args_helpers import (
	unwrap_args,
	wrap_trio_thread_args
)


__all__ = ["CoreScriptMixin"]


class CoreScriptMixin(UnifiedCoreScriptMixin, TrioThreadMixin, AbstractCoreScriptMixin):
	"""
	Mixin for JavaScript execution and management in Core WebDrivers.

	Allows execution of synchronous and asynchronous JavaScript, as well as
	pinning scripts for repeated use.
	"""
	
	async def execute_async_script(self, script: str, *args: Any) -> Any:
		unwrapped = unwrap_args(args=args)
		result = await self.sync_to_trio(sync_function=self._execute_async_script_impl)(script, *unwrapped)
		
		return wrap_trio_thread_args(args=result, lock=self._lock, limiter=self._capacity_limiter)
	
	async def execute_script(self, script: str, *args: Any) -> Any:
		unwrapped = unwrap_args(args=args)
		result = await self.sync_to_trio(sync_function=self._execute_script_impl)(script, *unwrapped)
		
		return wrap_trio_thread_args(args=result, lock=self._lock, limiter=self._capacity_limiter)
	
	async def get_pinned_scripts(self) -> List[str]:
		return await self.sync_to_trio(sync_function=self._get_pinned_scripts_impl)()
	
	async def pin_script(self, script: str, script_key: Optional[Any] = None) -> Any:
		return await self.sync_to_trio(sync_function=self._pin_script_impl)(script=script, script_key=script_key)
	
	async def script(self) -> Script:
		legacy = await self.sync_to_trio(sync_function=self._script_impl)()
		
		return get_trio_thread_instance_wrapper(
				wrapper_class=Script,
				legacy_object=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	async def unpin(self, script_key: Any) -> None:
		await self.sync_to_trio(sync_function=self._unpin_impl)(script_key=script_key)
