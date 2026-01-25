from typing import Optional
from osn_selenium.models import WindowRect
from osn_selenium._typehints import PATH_TYPEHINT
from osn_selenium.flags.models.yandex import YandexFlags
from osn_selenium.webdrivers.unified.yandex.settings import (
	UnifiedYandexSettingsMixin
)
from osn_selenium.abstract.webdriver.yandex.settings import (
	AbstractYandexSettingsMixin
)


__all__ = ["YandexSettingsMixin"]


class YandexSettingsMixin(UnifiedYandexSettingsMixin, AbstractYandexSettingsMixin):
	"""
	Mixin for configuring and updating settings of the Yandex WebDriver.

	Provides methods to modify browser flags, window rectangles, and other
	configuration parameters either before startup either during a reset.
	"""
	
	def reset_settings(
			self,
			flags: Optional[YandexFlags] = None,
			browser_exe: Optional[PATH_TYPEHINT] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: str = "",
			window_rect: Optional[WindowRect] = None,
	) -> None:
		self._reset_settings_impl(
				flags=flags,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				start_page_url=start_page_url,
				window_rect=window_rect,
		)
	
	def update_settings(
			self,
			flags: Optional[YandexFlags] = None,
			browser_exe: Optional[PATH_TYPEHINT] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		self._update_settings_impl(
				flags=flags,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				start_page_url=start_page_url,
				window_rect=window_rect,
		)
