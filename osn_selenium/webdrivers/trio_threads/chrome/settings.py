from typing import Optional
from osn_selenium.models import WindowRect
from osn_selenium._typehints import PATH_TYPEHINT
from osn_selenium.flags.models.chrome import ChromeFlags
from osn_selenium.webdrivers.trio_threads.blink import BlinkSettingsMixin
from osn_selenium.webdrivers.unified.chrome.settings import (
	UnifiedChromeSettingsMixin
)
from osn_selenium.abstract.webdriver.chrome.settings import (
	AbstractChromeSettingsMixin
)


__all__ = ["ChromeSettingsMixin"]


class ChromeSettingsMixin(
		UnifiedChromeSettingsMixin,
		BlinkSettingsMixin,
		AbstractChromeSettingsMixin
):
	"""
	Mixin for configuring and updating settings of the Chrome WebDriver.

	Provides methods to modify browser flags, window rectangles, and other
	configuration parameters either before startup or during a reset.
	"""
	
	async def reset_settings(
			self,
			flags: Optional[ChromeFlags] = None,
			browser_exe: Optional[PATH_TYPEHINT] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: str = "",
			window_rect: Optional[WindowRect] = None,
	) -> None:
		await self.sync_to_trio(sync_function=self._reset_settings_impl)(
				flags=flags,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				start_page_url=start_page_url,
				window_rect=window_rect,
		)
	
	async def update_settings(
			self,
			flags: Optional[ChromeFlags] = None,
			browser_exe: Optional[PATH_TYPEHINT] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		await self.sync_to_trio(sync_function=self._update_settings_impl)(
				flags=flags,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				start_page_url=start_page_url,
				window_rect=window_rect,
		)
