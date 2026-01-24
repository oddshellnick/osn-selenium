from typing import Optional
from osn_selenium.models import WindowRect
from osn_selenium._typehints import PATH_TYPEHINT
from osn_selenium.flags.models.chrome import ChromeFlags
from osn_selenium.webdrivers.sync.blink import BlinkLifecycleMixin
from osn_selenium.webdrivers.unified.chrome.lifecycle import (
	UnifiedChromeLifecycleMixin
)
from osn_selenium.abstract.webdriver.chrome.lifecycle import (
	AbstractChromeLifecycleMixin
)


__all__ = ["ChromeLifecycleMixin"]


class ChromeLifecycleMixin(
		UnifiedChromeLifecycleMixin,
		BlinkLifecycleMixin,
		AbstractChromeLifecycleMixin
):
	"""
	Mixin for managing the lifecycle of the Chrome WebDriver.

	Handles the creation, startup, shutdown, and restarting processes of the
	underlying browser instance, ensuring clean session management.
	"""
	
	def restart_webdriver(
			self,
			flags: Optional[ChromeFlags] = None,
			browser_exe: Optional[PATH_TYPEHINT] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		self._restart_webdriver_impl(
				flags=flags,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				start_page_url=start_page_url,
				window_rect=window_rect,
		)
	
	def start_webdriver(
			self,
			flags: Optional[ChromeFlags] = None,
			browser_exe: Optional[PATH_TYPEHINT] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		self._start_webdriver_impl(
				flags=flags,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				start_page_url=start_page_url,
				window_rect=window_rect,
		)
