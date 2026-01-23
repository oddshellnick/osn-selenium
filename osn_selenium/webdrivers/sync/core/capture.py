from typing import Any, Optional
from osn_selenium.webdrivers.unified.core.capture import (
	UnifiedCoreCaptureMixin
)
from osn_selenium.abstract.webdriver.core.capture import (
	AbstractCoreCaptureMixin
)


__all__ = ["CoreCaptureMixin"]


class CoreCaptureMixin(UnifiedCoreCaptureMixin, AbstractCoreCaptureMixin):
	"""
	Mixin enabling screen capture and page source retrieval for Core WebDrivers.

	Offers methods to take screenshots (file, base64, png), print pages,
	and extract the current DOM source.
	"""
	
	def get_screenshot_as_base64(self) -> str:
		return self._get_screenshot_as_base64_impl()
	
	def get_screenshot_as_file(self, filename: str) -> bool:
		return self._get_screenshot_as_file_impl(filename=filename)
	
	def get_screenshot_as_png(self) -> bytes:
		return self._get_screenshot_as_png_impl()
	
	def page_source(self) -> str:
		return self._page_source_impl()
	
	def print_page(self, print_options: Optional[Any] = None) -> str:
		return self._print_page_impl(print_options=print_options)
	
	def save_screenshot(self, filename: str) -> bool:
		return self._save_screenshot_impl(filename=filename)
