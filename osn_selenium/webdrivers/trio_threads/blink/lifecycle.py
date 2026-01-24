from typing import Optional
from osn_selenium.models import WindowRect
from osn_selenium._typehints import PATH_TYPEHINT
from osn_selenium.flags.models.blink import BlinkFlags
from osn_selenium.webdrivers.trio_threads.core.lifecycle import CoreLifecycleMixin
from osn_selenium.webdrivers.unified.blink.lifecycle import (
	UnifiedBlinkLifecycleMixin
)
from osn_selenium.abstract.webdriver.blink.lifecycle import (
	AbstractBlinkLifecycleMixin
)


__all__ = ["BlinkLifecycleMixin"]


class BlinkLifecycleMixin(
		UnifiedBlinkLifecycleMixin,
		CoreLifecycleMixin,
		AbstractBlinkLifecycleMixin
):
	"""
	Mixin for managing the lifecycle of the Blink WebDriver.

	Handles the creation, startup, shutdown, and restarting processes of the
	underlying browser instance, ensuring clean session management.
	"""
	
	async def close_webdriver(self) -> None:
		await self.sync_to_trio(sync_function=self._close_webdriver_impl)()
	
	async def restart_webdriver(
			self,
			flags: Optional[BlinkFlags] = None,
			browser_exe: Optional[PATH_TYPEHINT] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		await self.sync_to_trio(sync_function=self._restart_webdriver_impl)(
				flags=flags,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				start_page_url=start_page_url,
				window_rect=window_rect
		)
	
	async def start_webdriver(
			self,
			flags: Optional[BlinkFlags] = None,
			browser_exe: Optional[PATH_TYPEHINT] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		await self.sync_to_trio(sync_function=self._start_webdriver_impl)(
				flags=flags,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				start_page_url=start_page_url,
				window_rect=window_rect,
		)
