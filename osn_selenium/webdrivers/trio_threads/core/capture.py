from typing import Any, Optional
from osn_selenium.trio_threads_mixin import TrioThreadMixin
from osn_selenium.webdrivers.unified.core.capture import (
	UnifiedCoreCaptureMixin
)
from osn_selenium.abstract.webdriver.core.capture import (
	AbstractCoreCaptureMixin
)


__all__ = ["CoreCaptureMixin"]


class CoreCaptureMixin(UnifiedCoreCaptureMixin, TrioThreadMixin, AbstractCoreCaptureMixin):
	"""
	Mixin enabling screen capture and page source retrieval for Core WebDrivers.

	Offers methods to take screenshots (file, base64, png), print pages,
	and extract the current DOM source.
	"""
	
	async def get_screenshot_as_base64(self) -> str:
		return await self.sync_to_trio(sync_function=self._get_screenshot_as_base64_impl)()
	
	async def get_screenshot_as_file(self, filename: str) -> bool:
		return await self.sync_to_trio(sync_function=self._get_screenshot_as_file_impl)(filename=filename)
	
	async def get_screenshot_as_png(self) -> bytes:
		return await self.sync_to_trio(sync_function=self._get_screenshot_as_png_impl)()
	
	async def page_source(self) -> str:
		return await self.sync_to_trio(sync_function=self._page_source_impl)()
	
	async def print_page(self, print_options: Optional[Any] = None) -> str:
		return await self.sync_to_trio(sync_function=self._print_page_impl)(print_options=print_options)
	
	async def save_screenshot(self, filename: str) -> bool:
		return await self.sync_to_trio(sync_function=self._save_screenshot_impl)(filename=filename)
