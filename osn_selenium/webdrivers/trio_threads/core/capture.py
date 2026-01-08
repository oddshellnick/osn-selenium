from typing import Any, Optional
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.webdrivers.trio_threads.core.base import CoreBaseMixin
from osn_selenium.abstract.webdriver.core.capture import AbstractCoreCaptureMixin


class CoreCaptureMixin(CoreBaseMixin, AbstractCoreCaptureMixin):
	@requires_driver
	async def get_screenshot_as_base64(self) -> str:
		return await self._wrap_to_trio(self.driver.get_screenshot_as_base64)
	
	@requires_driver
	async def get_screenshot_as_file(self, filename: str) -> bool:
		return await self._wrap_to_trio(self.driver.get_screenshot_as_file, filename=filename)
	
	@requires_driver
	async def get_screenshot_as_png(self) -> bytes:
		return await self._wrap_to_trio(self.driver.get_screenshot_as_png)
	
	@requires_driver
	async def page_source(self) -> str:
		return await self._wrap_to_trio(lambda: self.driver.page_source)
	
	@requires_driver
	async def print_page(self, print_options: Optional[Any] = None) -> str:
		return await self._wrap_to_trio(self.driver.print_page, print_options=print_options)
	
	@requires_driver
	async def save_screenshot(self, filename: str) -> bool:
		return await self._wrap_to_trio(self.driver.save_screenshot, filename=filename)
