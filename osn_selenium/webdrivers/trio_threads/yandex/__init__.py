import trio
import pathlib
from osn_selenium.models import WindowRect
from typing import (
	Optional,
	Type,
	Union
)
from osn_selenium.flags.yandex import YandexFlagsManager
from osn_selenium.flags.models.yandex import YandexFlags
from osn_selenium.dev_tools.settings import DevToolsSettings
from osn_selenium.webdrivers.trio_threads.chrome import ChromeWebDriver
from osn_selenium.webdrivers.trio_threads.yandex.base import YandexBaseMixin
from osn_selenium.abstract.webdriver.yandex import (
	AbstractYandexWebDriver
)
from osn_selenium.webdrivers.trio_threads.yandex.settings import YandexSettingsMixin
from osn_selenium.webdrivers.trio_threads.yandex.lifecycle import YandexLifecycleMixin


__all__ = ["YandexWebDriver"]


class YandexWebDriver(
		YandexBaseMixin,
		YandexLifecycleMixin,
		YandexSettingsMixin,
		ChromeWebDriver,
		AbstractYandexWebDriver,
):
	"""
	Concrete Yandex WebDriver implementation combining all functional mixins.

	This class aggregates lifecycle management, element interaction, navigation,
	and browser-specific features into a single usable driver instance.
	"""
	
	def __init__(
			self,
			webdriver_path: str,
			flags_manager_type: Type[YandexFlagsManager] = YandexFlagsManager,
			use_browser_exe: bool = True,
			browser_name_in_system: str = "Yandex",
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			flags: Optional[YandexFlags] = None,
			start_page_url: str = "about:blank",
			implicitly_wait: int = 5,
			page_load_timeout: int = 5,
			script_timeout: int = 5,
			window_rect: Optional[WindowRect] = None,
			devtools_settings: Optional[DevToolsSettings] = None,
			capacity_limiter: Optional[trio.CapacityLimiter] = None,
	):
		ChromeWebDriver.__init__(
				self,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				webdriver_path=webdriver_path,
				use_browser_exe=use_browser_exe,
				flags_manager_type=flags_manager_type,
				flags=flags,
				implicitly_wait=implicitly_wait,
				page_load_timeout=page_load_timeout,
				script_timeout=script_timeout,
				window_rect=window_rect,
				devtools_settings=devtools_settings,
				capacity_limiter=capacity_limiter,
		)
		
		YandexBaseMixin.__init__(
				self,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				webdriver_path=webdriver_path,
				architecture="trio_threads",
				flags_manager_type=flags_manager_type,
				flags=flags,
				start_page_url=start_page_url,
				implicitly_wait=implicitly_wait,
				page_load_timeout=page_load_timeout,
				script_timeout=script_timeout,
				window_rect=window_rect,
				capacity_limiter=capacity_limiter,
		)
