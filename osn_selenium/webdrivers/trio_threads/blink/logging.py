from typing import Any
from osn_selenium.trio_threads_mixin import TrioThreadMixin
from osn_selenium.webdrivers.unified.blink.logging import (
	UnifiedBlinkLoggingMixin
)
from osn_selenium.abstract.webdriver.blink.logging import (
	AbstractBlinkLoggingMixin
)


__all__ = ["BlinkLoggingMixin"]


class BlinkLoggingMixin(UnifiedBlinkLoggingMixin, TrioThreadMixin, AbstractBlinkLoggingMixin):
	"""
	Mixin for retrieving and managing browser logs for Blink WebDrivers.

	Allows access to various log types (e.g., browser, performance, driver)
	generated during the session execution.
	"""
	
	async def get_log(self, log_type: str) -> Any:
		return await self.sync_to_trio(sync_function=self._get_log_impl)(log_type=log_type)
	
	async def log_types(self) -> Any:
		return await self.sync_to_trio(sync_function=self._log_types_impl)()
