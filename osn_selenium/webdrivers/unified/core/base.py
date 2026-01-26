from osn_selenium._cdp_import import install_cdp_hook
from osn_selenium.models import WindowRect
from typing import (
	Any,
	Dict,
	Mapping, Optional,
	Type
)
from osn_selenium.flags.base import BrowserFlagsManager
from osn_selenium.flags.models.base import BrowserFlags
from selenium.webdriver.common.bidi.session import Session
from osn_selenium._typehints import (
	ARCHITECTURES_TYPEHINT, PATH_TYPEHINT
)
from selenium.webdriver.remote.errorhandler import ErrorHandler
from osn_selenium.webdrivers._decorators import requires_driver
from selenium.webdriver.remote.locator_converter import LocatorConverter
from selenium.webdriver.remote.remote_connection import RemoteConnection
from osn_selenium.exceptions.webdriver import (
	WebDriverNotStartedError
)
from selenium.webdriver.remote.webdriver import (
	WebDriver as legacyWebDriver
)


__all__ = ["UnifiedCoreBaseMixin"]


class UnifiedCoreBaseMixin:
	def __init__(
			self,
			webdriver_path: str,
			architecture: ARCHITECTURES_TYPEHINT,
			flags_manager_type: Type[BrowserFlagsManager] = BrowserFlagsManager,
			flags: Optional[BrowserFlags] = None,
			implicitly_wait: int = 5,
			page_load_timeout: int = 5,
			script_timeout: int = 5,
			window_rect: Optional[WindowRect] = None,
			cdp_versioned_packages_paths: Optional[Mapping[int, PATH_TYPEHINT]] = None,
			ignore_cdp_version_package_missing: bool = True,
	) -> None:
		self._window_rect = window_rect
		self._webdriver_path = webdriver_path
		self._webdriver_flags_manager = flags_manager_type()
		self._driver: Optional[legacyWebDriver] = None
		self._architecture = architecture
		self._base_implicitly_wait = float(implicitly_wait)
		self._base_page_load_timeout = float(page_load_timeout)
		self._base_script_timeout = float(script_timeout)
		self._is_active = False
		
		if flags is not None:
			self._webdriver_flags_manager.update_flags(flags)

		if not getattr(self, "cdp_hook_installed", False):
			install_cdp_hook(cdp_paths=cdp_versioned_packages_paths, ignore_package_missing=ignore_cdp_version_package_missing)
			setattr(self, "cdp_hook_installed", True)
	
	@property
	def _architecture_impl(self) -> ARCHITECTURES_TYPEHINT:
		return self._architecture
	
	@requires_driver
	def _capabilities_impl(self) -> Dict[str, Any]:
		return self._driver_impl.capabilities
	
	@requires_driver
	def _caps_get_impl(self) -> Dict[str, Any]:
		return self._driver_impl.caps
	
	@requires_driver
	def _caps_set_impl(self, value: Dict[str, Any]) -> None:
		self._driver_impl.caps = value
	
	@requires_driver
	def _command_executor_get_impl(self) -> RemoteConnection:
		return self._driver_impl.command_executor
	
	@requires_driver
	def _command_executor_set_impl(self, value: RemoteConnection) -> None:
		self._driver_impl.command_executor = value
	
	@property
	def _driver_impl(self) -> Optional[legacyWebDriver]:
		return self._driver
	
	def _ensure_driver(self) -> None:
		if self._driver is None:
			raise WebDriverNotStartedError()
	
	@requires_driver
	def _error_handler_get_impl(self) -> ErrorHandler:
		return self._driver_impl.error_handler
	
	@requires_driver
	def _error_handler_set_impl(self, value: ErrorHandler) -> None:
		self._driver_impl.error_handler = value
	
	@requires_driver
	def _execute_impl(self, driver_command: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
		return self._driver_impl.execute(driver_command=driver_command, params=params)
	
	@property
	def _is_active_impl(self) -> bool:
		return self._is_active
	
	@requires_driver
	def _locator_converter_get_impl(self) -> LocatorConverter:
		return self._driver_impl.locator_converter
	
	@requires_driver
	def _locator_converter_set_impl(self, value: LocatorConverter) -> None:
		self._driver_impl.locator_converter = value
	
	@requires_driver
	def _name_impl(self) -> str:
		return self._driver_impl.name
	
	@requires_driver
	def _pinned_scripts_get_impl(self) -> Dict[str, Any]:
		return self._driver_impl.pinned_scripts
	
	@requires_driver
	def _pinned_scripts_set_impl(self, value: Dict[str, Any]) -> None:
		self._driver_impl.pinned_scripts = value
	
	@requires_driver
	def _session_id_get_impl(self) -> Optional[str]:
		return self._driver_impl.session_id
	
	@requires_driver
	def _session_id_set_impl(self, value: Optional[str]) -> None:
		self._driver_impl.session_id = value
	
	@requires_driver
	def _session_impl(self) -> Session:
		return self._driver_impl._session
