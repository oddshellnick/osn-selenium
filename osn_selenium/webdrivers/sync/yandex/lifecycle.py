from typing import Optional
from osn_selenium.models import WindowRect
from osn_selenium._typehints import PATH_TYPEHINT
from osn_selenium.flags.models.yandex import YandexFlags
from osn_selenium.webdrivers.sync.chrome import ChromeLifecycleMixin
from osn_selenium.webdrivers.unified.yandex.lifecycle import (
	UnifiedYandexLifecycleMixin
)
from osn_selenium.abstract.webdriver.yandex.lifecycle import (
	AbstractYandexLifecycleMixin
)


__all__ = ["YandexLifecycleMixin"]


class YandexLifecycleMixin(
		UnifiedYandexLifecycleMixin,
		ChromeLifecycleMixin,
		AbstractYandexLifecycleMixin
):
	"""
	Mixin for managing the lifecycle of the Yandex WebDriver.

	Handles the creation, startup, shutdown, and restarting processes of the
	underlying browser instance, ensuring clean session management.
	"""
	
	def restart_webdriver(
			self,
			flags: Optional[YandexFlags] = None,
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
			flags: Optional[YandexFlags] = None,
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
