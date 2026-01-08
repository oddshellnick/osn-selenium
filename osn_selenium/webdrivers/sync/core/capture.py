from typing import Any, Optional
from osn_selenium.webdrivers.sync.core.base import CoreBaseMixin
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.abstract.webdriver.core.capture import AbstractCoreCaptureMixin


class CoreCaptureMixin(CoreBaseMixin, AbstractCoreCaptureMixin):
	@requires_driver
	def get_screenshot_as_base64(self) -> str:
		return self.driver.get_screenshot_as_base64()
	
	@requires_driver
	def get_screenshot_as_file(self, filename: str) -> bool:
		return self.driver.get_screenshot_as_file(filename=filename)
	
	@requires_driver
	def get_screenshot_as_png(self) -> bytes:
		return self.driver.get_screenshot_as_png()
	
	@requires_driver
	def page_source(self) -> str:
		return self.driver.page_source
	
	@requires_driver
	def print_page(self, print_options: Optional[Any] = None) -> str:
		return self.driver.print_page(print_options=print_options)
	
	@requires_driver
	def save_screenshot(self, filename: str) -> bool:
		return self.driver.save_screenshot(filename=filename)
