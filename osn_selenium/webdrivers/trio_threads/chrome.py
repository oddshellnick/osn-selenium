import trio
import pathlib
from osn_selenium.types import WindowRect
from typing import (
	Optional,
	Type,
	Union
)
from selenium.webdriver.chrome.service import Service
from osn_selenium.flags.models.chrome import ChromeFlags
from osn_selenium.flags.chrome import ChromeFlagsManager
from osn_selenium.dev_tools.settings import DevToolsSettings
from osn_selenium.webdrivers.trio_threads.blink import BlinkWebDriver
from osn_selenium.abstract.webdriver.chrome import (
	AbstractChromeWebDriver
)
from selenium.webdriver.chrome.webdriver import (
	WebDriver as legacyWebDriver
)


class ChromeWebDriver(BlinkWebDriver, AbstractChromeWebDriver):
	def __init__(
			self,
			webdriver_path: str,
			flags_manager_type: Type[ChromeFlagsManager] = ChromeFlagsManager,
			use_browser_exe: bool = True,
			browser_name_in_system: str = "Google Chrome",
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			flags: Optional[ChromeFlags] = None,
			start_page_url: str = "https://www.chrome.com",
			implicitly_wait: int = 5,
			page_load_timeout: int = 5,
			script_timeout: int = 5,
			window_rect: Optional[WindowRect] = None,
			devtools_settings: Optional[DevToolsSettings] = None,
			capacity_limiter: Optional[trio.CapacityLimiter] = None,
	) -> None:
		super().__init__(
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				webdriver_path=webdriver_path,
				flags_manager_type=flags_manager_type,
				flags=flags,
				start_page_url=start_page_url,
				implicitly_wait=implicitly_wait,
				page_load_timeout=page_load_timeout,
				script_timeout=script_timeout,
				window_rect=window_rect,
				devtools_settings=devtools_settings,
				capacity_limiter=capacity_limiter,
		)
	
	async def _create_driver(self) -> None:
		def _create() -> legacyWebDriver:
			webdriver_options = self._webdriver_flags_manager.options
			webdriver_service = Service(
					executable_path=self._webdriver_path,
					port=self.debugging_port if self.browser_exe is None else 0,
					service_args=self._webdriver_flags_manager.start_args
					if self.browser_exe is None
					else None,
			)
			
			return legacyWebDriver(options=webdriver_options, service=webdriver_service,)
		
		self._driver = await self._wrap_to_trio(_create)
		
		if self._window_rect is not None:
			await self.set_window_rect(
					x=self._window_rect.x,
					y=self._window_rect.y,
					width=self._window_rect.width,
					height=self._window_rect.height,
			)
		
		await self.set_driver_timeouts(
				page_load_timeout=self._base_page_load_timeout,
				implicit_wait_timeout=self._base_implicitly_wait,
				script_timeout=self._base_script_timeout,
		)
	
	@property
	def driver(self) -> Optional[legacyWebDriver]:
		return super().driver
	
	async def reset_settings(
			self,
			flags: Optional[ChromeFlags] = None,
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: str = "",
			window_rect: Optional[WindowRect] = None,
	) -> None:
		await super().reset_settings(
				flags=flags,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				start_page_url=start_page_url,
				window_rect=window_rect,
		)
	
	async def restart_webdriver(
			self,
			flags: Optional[ChromeFlags] = None,
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		await super().restart_webdriver(
				flags=flags,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				start_page_url=start_page_url,
				window_rect=window_rect,
		)
	
	async def start_webdriver(
			self,
			flags: Optional[ChromeFlags] = None,
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		await super().start_webdriver(
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
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		await super().update_settings(
				flags=flags,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				start_page_url=start_page_url,
				window_rect=window_rect,
		)
