import trio
from osn_selenium.models import WindowRect
from osn_selenium.trio_threads_mixin import TrioThreadMixin
from osn_selenium.flags.base import BrowserFlagsManager
from osn_selenium.flags.models.base import BrowserFlags
from selenium.webdriver.common.bidi.session import Session
from typing import (
	Any,
	Dict,
	Mapping,
	Optional,
	Type
)
from selenium.webdriver.remote.errorhandler import ErrorHandler
from osn_selenium.executors.trio_threads.cdp import CDPExecutor
from osn_selenium.executors.trio_threads.javascript import JSExecutor
from selenium.webdriver.remote.locator_converter import LocatorConverter
from selenium.webdriver.remote.remote_connection import RemoteConnection
from osn_selenium.webdrivers.unified.core.base import UnifiedCoreBaseMixin
from osn_selenium._typehints import (
	ARCHITECTURES_TYPEHINT,
	PATH_TYPEHINT
)
from osn_selenium.abstract.webdriver.core.base import (
	AbstractCoreBaseMixin
)
from selenium.webdriver.remote.webdriver import (
	WebDriver as legacyWebDriver
)
from osn_selenium.webdrivers._bridges import (
	get_cdp_executor_bridge,
	get_js_executor_bridge
)


__all__ = ["CoreBaseMixin"]


class CoreBaseMixin(UnifiedCoreBaseMixin, TrioThreadMixin, AbstractCoreBaseMixin):
	"""
	This class serves as the foundation for browser-specific implementations, managing
	the WebDriver executable path, configuration flags, timeouts, and the active
	driver instance.
	"""
	
	def __init__(
			self,
			webdriver_path: str,
			flags_manager_type: Type[BrowserFlagsManager] = BrowserFlagsManager,
			flags: Optional[BrowserFlags] = None,
			implicitly_wait: int = 5,
			page_load_timeout: int = 5,
			script_timeout: int = 5,
			window_rect: Optional[WindowRect] = None,
			capacity_limiter: Optional[trio.CapacityLimiter] = None,
			cdp_versioned_packages_paths: Optional[Mapping[int, PATH_TYPEHINT]] = None,
			ignore_cdp_version_package_missing: bool = True,
	) -> None:
		"""
		Initializes the base mixin for Trio-based WebDrivers.

		Sets up the core synchronization primitives, default timeouts,
		and the browser flag manager.

		Args:
			webdriver_path (str): The file path to the WebDriver executable.
			flags_manager_type (Type[BrowserFlagsManager]): The class type used to manage
				browser-specific configuration flags. Defaults to BrowserFlagsManager.
			flags (Optional[BrowserFlags]): Initial set of browser flags or options
				to apply upon startup. Defaults to None.
			implicitly_wait (int): The amount of time (in seconds) that the driver should
				wait when searching for elements. Defaults to 5.
			page_load_timeout (int): The amount of time (in seconds) to wait for a page
				load to complete. Defaults to 5.
			script_timeout (int): The amount of time (in seconds) to wait for an
				asynchronous script to finish execution. Defaults to 5.
			window_rect (Optional[WindowRect]): The initial size and position of the
				browser window. Defaults to None.
			capacity_limiter (Optional[trio.CapacityLimiter]): A Trio capacity limiter used to
				throttle concurrent thread-based operations. Defaults to None.
			cdp_versioned_packages_paths (Optional[Mapping[int, PATH_TYPEHINT]]): Custom local paths for specific CDP versions packages.
			ignore_cdp_version_package_missing (bool): Whether to ignore missing CDP package errors.
		"""
		
		UnifiedCoreBaseMixin.__init__(
				self,
				webdriver_path=webdriver_path,
				architecture="trio_threads",
				flags_manager_type=flags_manager_type,
				flags=flags,
				implicitly_wait=implicitly_wait,
				page_load_timeout=page_load_timeout,
				script_timeout=script_timeout,
				window_rect=window_rect,
				cdp_versioned_packages_paths=cdp_versioned_packages_paths,
				ignore_cdp_version_package_missing=ignore_cdp_version_package_missing,
		)
		
		TrioThreadMixin.__init__(
				self,
				lock=trio.Lock(),
				limiter=capacity_limiter
				if capacity_limiter is not None
				else trio.CapacityLimiter(100),
		)
		
		self._cdp_executor = CDPExecutor(
				execute_function=get_cdp_executor_bridge(self),
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
		
		self._js_executor = JSExecutor(
				execute_function=get_js_executor_bridge(self),
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	@property
	def architecture(self) -> ARCHITECTURES_TYPEHINT:
		return self._architecture_impl
	
	@property
	def capabilities(self) -> Dict[str, Any]:
		return self._capabilities_impl()
	
	@property
	def caps(self) -> Dict[str, Any]:
		return self._caps_get_impl()
	
	@caps.setter
	def caps(self, value: Dict[str, Any]) -> None:
		self._caps_set_impl(value=value)
	
	@property
	def cdp(self) -> CDPExecutor:
		return self._cdp_executor
	
	@property
	def command_executor(self) -> RemoteConnection:
		return self._command_executor_get_impl()
	
	@command_executor.setter
	def command_executor(self, value: RemoteConnection) -> None:
		self._command_executor_set_impl(value=value)
	
	@property
	def driver(self) -> Optional[legacyWebDriver]:
		return self._driver_impl
	
	@property
	def error_handler(self) -> ErrorHandler:
		return self._error_handler_get_impl()
	
	@error_handler.setter
	def error_handler(self, value: ErrorHandler) -> None:
		self._error_handler_set_impl(value=value)
	
	async def execute(self, driver_command: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
		return await self.sync_to_trio(sync_function=self._execute_impl)(driver_command=driver_command, params=params)
	
	@property
	def is_active(self) -> bool:
		return self._is_active_impl
	
	@property
	def javascript(self) -> JSExecutor:
		return self._js_executor
	
	@property
	def locator_converter(self) -> LocatorConverter:
		return self._locator_converter_get_impl()
	
	@locator_converter.setter
	def locator_converter(self, value: LocatorConverter) -> None:
		self._locator_converter_set_impl(value=value)
	
	@property
	def name(self) -> str:
		return self._name_impl()
	
	@property
	def pinned_scripts(self) -> Dict[str, Any]:
		return self._pinned_scripts_get_impl()
	
	@pinned_scripts.setter
	def pinned_scripts(self, value: Dict[str, Any]) -> None:
		self._pinned_scripts_set_impl(value=value)
	
	async def session(self) -> Session:
		return await self.sync_to_trio(sync_function=self._session_impl)()
	
	@property
	def session_id(self) -> Optional[str]:
		return self._session_id_get_impl()
	
	@session_id.setter
	def session_id(self, value: Optional[str]) -> None:
		self._session_id_set_impl(value=value)
