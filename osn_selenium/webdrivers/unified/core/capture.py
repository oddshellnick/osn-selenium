from typing import Any, Optional
from osn_selenium.webdrivers._decorators import requires_driver
from osn_selenium.webdrivers.unified.core.base import UnifiedCoreBaseMixin


__all__ = ["UnifiedCoreCaptureMixin"]


class UnifiedCoreCaptureMixin(UnifiedCoreBaseMixin):
	@requires_driver
	def _get_screenshot_as_base64_impl(self) -> str:
		return self._driver_impl.get_screenshot_as_base64()
	
	@requires_driver
	def _get_screenshot_as_file_impl(self, filename: str) -> bool:
		return self._driver_impl.get_screenshot_as_file(filename=filename)
	
	@requires_driver
	def _get_screenshot_as_png_impl(self) -> bytes:
		return self._driver_impl.get_screenshot_as_png()
	
	@requires_driver
	def _page_source_impl(self) -> str:
		return self._driver_impl.page_source
	
	@requires_driver
	def _print_page_impl(self, print_options: Optional[Any] = None) -> str:
		return self._driver_impl.print_page(print_options=print_options)
	
	@requires_driver
	def _save_screenshot_impl(self, filename: str) -> bool:
		return self._driver_impl.save_screenshot(filename=filename)
