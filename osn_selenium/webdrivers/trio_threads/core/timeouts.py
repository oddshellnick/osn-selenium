from typing import Optional
from osn_selenium.trio_threads_mixin import TrioThreadMixin
from selenium.webdriver.common.timeouts import Timeouts
from osn_selenium.webdrivers.unified.core.timeouts import (
	UnifiedCoreTimeoutsMixin
)
from osn_selenium.abstract.webdriver.core.timeouts import (
	AbstractCoreTimeoutsMixin
)


__all__ = ["CoreTimeoutsMixin"]


class CoreTimeoutsMixin(UnifiedCoreTimeoutsMixin, TrioThreadMixin, AbstractCoreTimeoutsMixin):
	"""
	Mixin for configuring execution timeouts in Core WebDrivers.

	Manages implicit waits, page load timeouts, and script execution limits
	to control driver behavior during delays.
	"""
	
	async def get_timeouts(self) -> Timeouts:
		return await self.sync_to_trio(sync_function=self._get_timeouts_impl)()
	
	async def implicitly_wait(self, time_to_wait: float) -> None:
		await self.sync_to_trio(sync_function=self._implicitly_wait_impl)(time_to_wait=time_to_wait)
	
	async def set_driver_timeouts(
			self,
			page_load_timeout: float,
			implicit_wait_timeout: float,
			script_timeout: float,
	) -> None:
		await self.sync_to_trio(sync_function=self._set_driver_timeouts_impl)(
				page_load_timeout=page_load_timeout,
				implicit_wait_timeout=implicit_wait_timeout,
				script_timeout=script_timeout,
		)
	
	async def set_page_load_timeout(self, time_to_wait: float) -> None:
		await self.sync_to_trio(sync_function=self._set_page_load_timeout_impl)(time_to_wait=time_to_wait)
	
	async def set_script_timeout(self, time_to_wait: float) -> None:
		await self.sync_to_trio(sync_function=self._set_script_timeout_impl)(time_to_wait=time_to_wait)
	
	async def set_timeouts(self, timeouts: Timeouts) -> None:
		await self.sync_to_trio(sync_function=self._set_timeouts_impl)(timeouts=timeouts)
	
	async def update_times(
			self,
			temp_implicitly_wait: Optional[float] = None,
			temp_page_load_timeout: Optional[float] = None,
			temp_script_timeout: Optional[float] = None,
	) -> None:
		await self.sync_to_trio(sync_function=self._update_times_impl)(
				temp_implicitly_wait=temp_implicitly_wait,
				temp_page_load_timeout=temp_page_load_timeout,
				temp_script_timeout=temp_script_timeout,
		)
