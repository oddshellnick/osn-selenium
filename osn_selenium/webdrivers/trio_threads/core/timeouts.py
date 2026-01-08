from typing import Any, Optional
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.webdrivers.trio_threads.core.base import CoreBaseMixin
from osn_selenium.abstract.webdriver.core.timeouts import (
	AbstractCoreTimeoutsMixin
)


class CoreTimeoutsMixin(CoreBaseMixin, AbstractCoreTimeoutsMixin):
	@requires_driver
	async def implicitly_wait(self, time_to_wait: float) -> None:
		await self._wrap_to_trio(self.driver.implicitly_wait, time_to_wait=time_to_wait)
	
	@requires_driver
	async def set_page_load_timeout(self, time_to_wait: float) -> None:
		await self._wrap_to_trio(self.driver.set_page_load_timeout, time_to_wait=time_to_wait)
	
	@requires_driver
	async def set_script_timeout(self, time_to_wait: float) -> None:
		await self._wrap_to_trio(self.driver.set_script_timeout, time_to_wait=time_to_wait)
	
	@requires_driver
	async def set_timeouts(self, timeouts: Any) -> None:
		await self._wrap_to_trio(lambda: setattr(self.driver, "timeouts", timeouts))
	
	@requires_driver
	async def timeouts(self) -> Any:
		return await self._wrap_to_trio(lambda: self.driver.timeouts)
	
	@requires_driver
	async def set_driver_timeouts(
			self,
			page_load_timeout: float,
			implicit_wait_timeout: float,
			script_timeout: float,
	) -> None:
		def _set() -> None:
			self.driver.set_page_load_timeout(page_load_timeout)
			self.driver.implicitly_wait(implicit_wait_timeout)
			self.driver.set_script_timeout(script_timeout)
		
		await self._wrap_to_trio(_set)
	
	async def update_times(
			self,
			temp_implicitly_wait: Optional[float] = None,
			temp_page_load_timeout: Optional[float] = None,
			temp_script_timeout: Optional[float] = None,
	) -> None:
		implicitly_wait = temp_implicitly_wait if temp_implicitly_wait is not None else self._base_implicitly_wait
		page_load_timeout = temp_page_load_timeout if temp_page_load_timeout is not None else self._base_page_load_timeout
		script_timeout = temp_script_timeout if temp_script_timeout is not None else self._base_script_timeout
		
		await self.set_driver_timeouts(
				page_load_timeout=page_load_timeout,
				implicit_wait_timeout=implicitly_wait,
				script_timeout=script_timeout,
		)
