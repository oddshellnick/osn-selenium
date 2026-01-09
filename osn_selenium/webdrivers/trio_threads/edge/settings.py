import pathlib
from typing import Optional, Union
from osn_selenium.types import WindowRect
from osn_selenium.flags.models.edge import EdgeFlags
from osn_selenium.webdrivers.trio_threads.edge.base import EdgeBaseMixin
from osn_selenium.abstract.webdriver.edge.settings import (
	AbstractEdgeSettingsMixin
)


class EdgeSettingsMixin(EdgeBaseMixin, AbstractEdgeSettingsMixin):
	"""
	Mixin for configuring and updating settings of the Edge WebDriver.

	Provides methods to modify browser flags, window rectangles, and other
	configuration parameters either before startup or during a reset.
	"""
	
	async def reset_settings(
			self,
			flags: Optional[EdgeFlags] = None,
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
	
	async def update_settings(
			self,
			flags: Optional[EdgeFlags] = None,
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
