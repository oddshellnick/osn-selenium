import pathlib
from typing import Optional, Union
from osn_selenium.types import WindowRect
from osn_selenium.flags.models.yandex import YandexFlags
from osn_selenium.webdrivers.unified.core.window import (
	UnifiedCoreWindowMixin
)
from osn_selenium.webdrivers.unified.core.timeouts import (
	UnifiedCoreTimeoutsMixin
)
from osn_selenium.webdrivers.unified.chrome.lifecycle import (
	UnifiedChromeLifecycleMixin
)


__all__ = ["UnifiedYandexLifecycleMixin"]


class UnifiedYandexLifecycleMixin(
		UnifiedChromeLifecycleMixin,
		UnifiedCoreTimeoutsMixin,
		UnifiedCoreWindowMixin
):
	def _restart_webdriver_impl(
			self,
			flags: Optional[YandexFlags] = None,
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		super()._restart_webdriver_impl(
				flags=flags,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				start_page_url=start_page_url,
				window_rect=window_rect,
		)
	
	def _start_webdriver_impl(
			self,
			flags: Optional[YandexFlags] = None,
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		super()._start_webdriver_impl(
				flags=flags,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				start_page_url=start_page_url,
				window_rect=window_rect,
		)
