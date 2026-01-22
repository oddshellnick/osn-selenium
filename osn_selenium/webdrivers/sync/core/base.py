from osn_selenium.types import WindowRect
from osn_selenium.flags.base import BrowserFlagsManager
from osn_selenium.flags.models.base import BrowserFlags
from selenium.webdriver.common.bidi.session import Session
from osn_selenium.instances.types import WEB_ELEMENT_TYPEHINT
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.instances.sync.web_element import WebElement
from selenium.webdriver.remote.errorhandler import ErrorHandler
from selenium.webdriver.remote.locator_converter import LocatorConverter
from selenium.webdriver.remote.remote_connection import RemoteConnection
from osn_selenium.instances.convert import (
	get_sync_instance_wrapper
)
from osn_selenium.abstract.webdriver.core.base import (
	AbstractCoreBaseMixin
)
from typing import (
	Any,
	Dict,
	List,
	Optional,
	Set,
	Tuple,
	Type,
	Union
)
from selenium.webdriver.remote.webdriver import (
	WebDriver as legacyWebDriver
)
from selenium.webdriver.remote.webelement import (
	WebElement as legacyWebElement
)


class CoreBaseMixin(AbstractCoreBaseMixin):
	"""
	Base mixin for Core WebDrivers handling core initialization and state management.

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
	) -> None:
		"""
		Initializes the base mixin for synchronous WebDrivers.

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
		"""
		
		self._window_rect = window_rect
		self._webdriver_path = webdriver_path
		self._webdriver_flags_manager = flags_manager_type()
		self._driver: Optional[legacyWebDriver] = None
		self._base_implicitly_wait = float(implicitly_wait)
		self._base_page_load_timeout = float(page_load_timeout)
		self._base_script_timeout = float(script_timeout)
		self._is_active = False
		
		if flags is not None:
			self._webdriver_flags_manager.update_flags(flags)
	
	@property
	def driver(self) -> Optional[legacyWebDriver]:
		return self._driver
	
	def _ensure_driver(self) -> None:
		if self.driver is None:
			raise RuntimeError("WebDriver is not started. Call start_webdriver() first.")
	
	@requires_driver
	def _session(self) -> Session:
		return self.driver._session
	
	def _unwrap_args(self, arg: Any) -> Any:
		if isinstance(arg, WebElement):
			return arg._legacy_impl
		
		if isinstance(arg, list):
			return [self._unwrap_args(item) for item in arg]
		
		if isinstance(arg, dict):
			return {k: self._unwrap_args(v) for k, v in arg.items()}
		
		if isinstance(arg, tuple):
			return tuple(self._unwrap_args(item) for item in arg)
		
		if isinstance(arg, set):
			return {self._unwrap_args(item) for item in arg}
		
		return arg
	
	def _wrap_result(self, result: Any) -> Union[
		WEB_ELEMENT_TYPEHINT,
		List[WEB_ELEMENT_TYPEHINT],
		Dict[Any, WEB_ELEMENT_TYPEHINT],
		Set[WEB_ELEMENT_TYPEHINT],
		Tuple[WEB_ELEMENT_TYPEHINT, ...],
		Any,
	]:
		if isinstance(result, legacyWebElement):
			return get_sync_instance_wrapper(wrapper_class=WebElement, legacy_object=result)
		
		if isinstance(result, list):
			return [self._wrap_result(item) for item in result]
		
		if isinstance(result, dict):
			return {k: self._wrap_result(v) for k, v in result.items()}
		
		if isinstance(result, tuple):
			return tuple(self._wrap_result(item) for item in result)
		
		if isinstance(result, set):
			return {self._wrap_result(item) for item in result}
		
		return result
	
	@property
	@requires_driver
	def capabilities(self) -> Dict[str, Any]:
		return self.driver.capabilities
	
	@property
	@requires_driver
	def caps(self) -> Dict[str, Any]:
		return self.driver.caps
	
	@caps.setter
	@requires_driver
	def caps(self, value: Dict[str, Any]) -> None:
		self.driver.caps = value
	
	@property
	@requires_driver
	def command_executor(self) -> RemoteConnection:
		return self.driver.command_executor
	
	@command_executor.setter
	@requires_driver
	def command_executor(self, value: RemoteConnection) -> None:
		self.driver.command_executor = value
	
	@property
	@requires_driver
	def error_handler(self) -> ErrorHandler:
		return self.driver.error_handler
	
	@error_handler.setter
	@requires_driver
	def error_handler(self, value: ErrorHandler) -> None:
		self.driver.error_handler = value
	
	@requires_driver
	def execute(self, driver_command: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
		return self.driver.execute(driver_command=driver_command, params=params)
	
	@property
	def is_active(self) -> bool:
		return self._is_active
	
	@property
	@requires_driver
	def locator_converter(self) -> LocatorConverter:
		return self.driver.locator_converter
	
	@locator_converter.setter
	@requires_driver
	def locator_converter(self, value: LocatorConverter) -> None:
		self.driver.locator_converter = value
	
	@property
	@requires_driver
	def name(self) -> str:
		return self.driver.name
	
	@property
	@requires_driver
	def pinned_scripts(self) -> Dict[str, Any]:
		return self.driver.pinned_scripts
	
	@pinned_scripts.setter
	@requires_driver
	def pinned_scripts(self, value: Dict[str, Any]) -> None:
		self.driver.pinned_scripts = value
	
	@property
	@requires_driver
	def session_id(self) -> Optional[str]:
		return self.driver.session_id
	
	@session_id.setter
	@requires_driver
	def session_id(self, value: Optional[str]) -> None:
		self.driver.session_id = value
