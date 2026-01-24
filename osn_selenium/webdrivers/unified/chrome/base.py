import pathlib
from osn_selenium.models import WindowRect
from typing import (
	Optional,
	Type,
	Union
)
from osn_selenium.flags.models.chrome import ChromeFlags
from osn_selenium.flags.chrome import ChromeFlagsManager
from selenium.webdriver import (
	Chrome as legacyChrome
)
from osn_selenium._typehints import (
	ARCHITECTURE_TYPEHINT
)
from osn_selenium.webdrivers.unified.blink.base import (
	UnifiedBlinkBaseMixin
)


__all__ = ["UnifiedChromeBaseMixin"]


class UnifiedChromeBaseMixin(UnifiedBlinkBaseMixin):
	def __init__(
			self,
			webdriver_path: str,
			architecture: ARCHITECTURE_TYPEHINT,
			flags_manager_type: Type[ChromeFlagsManager] = ChromeFlagsManager,
			use_browser_exe: bool = True,
			browser_name_in_system: str = "Google Chrome",
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			flags: Optional[ChromeFlags] = None,
			start_page_url: str = "about:blank",
			implicitly_wait: int = 5,
			page_load_timeout: int = 5,
			script_timeout: int = 5,
			window_rect: Optional[WindowRect] = None,
	):
		UnifiedBlinkBaseMixin.__init__(
				self,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				webdriver_path=webdriver_path,
				architecture=architecture,
				use_browser_exe=use_browser_exe,
				flags_manager_type=flags_manager_type,
				flags=flags,
				start_page_url=start_page_url,
				implicitly_wait=implicitly_wait,
				page_load_timeout=page_load_timeout,
				script_timeout=script_timeout,
				window_rect=window_rect,
		)
	
	@property
	def _driver_impl(self) -> Optional[legacyChrome]:
		return super()._driver_impl
