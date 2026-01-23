import pathlib
from osn_selenium.types import WindowRect
from typing import (
	Optional,
	Type,
	Union
)
from osn_selenium.flags.edge import EdgeFlagsManager
from osn_selenium.flags.models.edge import EdgeFlags
from osn_selenium.webdrivers.sync.blink import BlinkWebDriver
from osn_selenium.webdrivers.sync.edge.base import EdgeBaseMixin
from osn_selenium.webdrivers.sync.edge.settings import EdgeSettingsMixin
from osn_selenium.webdrivers.sync.edge.lifecycle import EdgeLifecycleMixin
from osn_selenium.abstract.webdriver.edge import (
	AbstractEdgeWebDriver
)


class EdgeWebDriver(
		EdgeBaseMixin,
		EdgeLifecycleMixin,
		EdgeSettingsMixin,
		BlinkWebDriver,
		AbstractEdgeWebDriver,
):
	def __init__(
			self,
			browser_exe: Optional[Union[str, pathlib.Path]],
			browser_name_in_system: str,
			webdriver_path: str,
			use_browser_exe: bool = True,
			flags_manager_type: Type[EdgeFlagsManager] = EdgeFlagsManager,
			flags: Optional[EdgeFlags] = None,
			start_page_url: str = "",
			implicitly_wait: int = 5,
			page_load_timeout: int = 5,
			script_timeout: int = 5,
			window_rect: Optional[WindowRect] = None,
	):
		BlinkWebDriver.__init__(
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
		)
		
		EdgeBaseMixin.__init__(
				self,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				webdriver_path=webdriver_path,
				architecture="sync",
				flags_manager_type=flags_manager_type,
				flags=flags,
				start_page_url=start_page_url,
				implicitly_wait=implicitly_wait,
				page_load_timeout=page_load_timeout,
				script_timeout=script_timeout,
				window_rect=window_rect,
		)
