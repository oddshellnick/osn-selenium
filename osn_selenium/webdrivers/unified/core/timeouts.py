from typing import Optional
from selenium.webdriver.common.timeouts import Timeouts
from osn_selenium.webdrivers._decorators import requires_driver
from osn_selenium.webdrivers.unified.core.base import UnifiedCoreBaseMixin


__all__ = ["UnifiedCoreTimeoutsMixin"]


class UnifiedCoreTimeoutsMixin(UnifiedCoreBaseMixin):
	@requires_driver
	def _get_timeouts_impl(self) -> Timeouts:
		return self._driver_impl.timeouts
	
	@requires_driver
	def _implicitly_wait_impl(self, time_to_wait: float) -> None:
		self._driver_impl.implicitly_wait(time_to_wait=time_to_wait)
	
	@requires_driver
	def _set_page_load_timeout_impl(self, time_to_wait: float) -> None:
		self._driver_impl.set_page_load_timeout(time_to_wait=time_to_wait)
	
	@requires_driver
	def _set_script_timeout_impl(self, time_to_wait: float) -> None:
		self._driver_impl.set_script_timeout(time_to_wait=time_to_wait)
	
	@requires_driver
	def _set_timeouts_impl(self, timeouts: Timeouts) -> None:
		self._driver_impl.timeouts = timeouts
	
	@requires_driver
	def _set_driver_timeouts_impl(
			self,
			page_load_timeout: float,
			implicit_wait_timeout: float,
			script_timeout: float,
	) -> None:
		self._driver_impl.set_page_load_timeout(page_load_timeout)
		self._driver_impl.implicitly_wait(implicit_wait_timeout)
		self._driver_impl.set_script_timeout(script_timeout)
	
	def _update_times_impl(
			self,
			temp_implicitly_wait: Optional[float] = None,
			temp_page_load_timeout: Optional[float] = None,
			temp_script_timeout: Optional[float] = None,
	) -> None:
		implicitly_wait = temp_implicitly_wait if temp_implicitly_wait is not None else self._base_implicitly_wait
		page_load_timeout = temp_page_load_timeout if temp_page_load_timeout is not None else self._base_page_load_timeout
		script_timeout = temp_script_timeout if temp_script_timeout is not None else self._base_script_timeout
		
		self._set_driver_timeouts_impl(
				page_load_timeout=page_load_timeout,
				implicit_wait_timeout=implicitly_wait,
				script_timeout=script_timeout,
		)
