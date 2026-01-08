from typing import Any
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.webdrivers.sync.blink.base import BlinkBaseMixin
from osn_selenium.abstract.webdriver.blink.logging import (
	AbstractBlinkLoggingMixin
)


class BlinkLoggingMixin(BlinkBaseMixin, AbstractBlinkLoggingMixin):
	@requires_driver
	def get_log(self, log_type: str) -> Any:
		return self.driver.get_log(log_type=log_type)
	
	@requires_driver
	def log_types(self) -> Any:
		return self.driver.log_types
