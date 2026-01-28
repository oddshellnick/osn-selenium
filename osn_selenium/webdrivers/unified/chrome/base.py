from typing import Mapping, Optional, Type
from osn_selenium.models import WindowRect
from osn_selenium.flags.chrome import ChromeFlagsManager
from osn_selenium.flags.models.chrome import ChromeFlags
from selenium.webdriver import (
	Chrome as legacyChrome
)
from osn_selenium._typehints import (
	ARCHITECTURES_TYPEHINT,
	PATH_TYPEHINT
)
from osn_selenium.webdrivers.unified.blink.base import (
	UnifiedBlinkBaseMixin
)


__all__ = ["UnifiedChromeBaseMixin"]


class UnifiedChromeBaseMixin(UnifiedBlinkBaseMixin):
	def __init__(
			self,
			webdriver_path: str,
			architecture: ARCHITECTURES_TYPEHINT,
			flags_manager_type: Type[ChromeFlagsManager] = ChromeFlagsManager,
			use_browser_exe: bool = True,
			browser_name_in_system: str = "Google Chrome",
			browser_exe: Optional[PATH_TYPEHINT] = None,
			flags: Optional[ChromeFlags] = None,
			start_page_url: str = "about:blank",
			implicitly_wait: int = 5,
			page_load_timeout: int = 5,
			script_timeout: int = 5,
			window_rect: Optional[WindowRect] = None,
			cdp_versioned_packages_paths: Optional[Mapping[int, PATH_TYPEHINT]] = None,
			ignore_cdp_version_package_missing: bool = True,
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
				cdp_versioned_packages_paths=cdp_versioned_packages_paths,
				ignore_cdp_version_package_missing=ignore_cdp_version_package_missing,
		)
	
	@property
	def _driver_impl(self) -> Optional[legacyChrome]:
		return super()._driver_impl
