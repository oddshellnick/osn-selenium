from typing import Any, List
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.webdrivers.trio_threads.blink.base import BlinkBaseMixin
from osn_selenium.abstract.webdriver.blink.logging import (
	AbstractBlinkLoggingMixin
)


class BlinkLoggingMixin(BlinkBaseMixin, AbstractBlinkLoggingMixin):
	"""
	Mixin for retrieving and managing browser logs for Blink WebDrivers.

	Allows access to various log types (e.g., browser, performance, driver)
	generated during the session execution.
	"""
	
	@requires_driver
	async def get_log(self, log_type: str) -> Any:
		return await self._wrap_to_trio(self.driver.get_log, log_type=log_type)
	
	@requires_driver
	async def log_types(self) -> List[str]:
		return await self._wrap_to_trio(lambda: self.driver.log_types)
