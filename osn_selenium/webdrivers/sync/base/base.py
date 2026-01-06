import trio
from osn_selenium.types import WindowRect
from osn_selenium.flags.base import BrowserFlagsManager
from osn_selenium.flags.models.base import BrowserFlags
from osn_selenium.trio_base_mixin import _TrioThreadMixin
from selenium.webdriver.common.bidi.session import Session
from osn_selenium.instances.types import WEB_ELEMENT_TYPEHINT
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.instances.sync.web_element import WebElement
from osn_selenium.abstract.webdriver.base.base import AbstractBaseMixin
from selenium.webdriver.remote.remote_connection import RemoteConnection
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


class BaseMixin(_TrioThreadMixin, AbstractBaseMixin):
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
	) -> None:
		super().__init__(
				lock=trio.Lock(),
				limiter=capacity_limiter
				if capacity_limiter is not None
				else trio.CapacityLimiter(100),
		)
		
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
			return arg.legacy
		
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
			return WebElement.from_legacy(selenium_web_element=result)
		
		if isinstance(result, list):
			return [self._wrap_result(item) for item in result]
		
		if isinstance(result, dict):
			return {k: self._wrap_result(v) for k, v in result.items()}
		
		if isinstance(result, tuple):
			return tuple(self._wrap_result(item) for item in result)
		
		if isinstance(result, set):
			return {self._wrap_result(item) for item in result}
		
		return result
	
	@requires_driver
	def command_executor(self) -> RemoteConnection:
		return self.driver.command_executor()
	
	@property
	def is_active(self) -> bool:
		return self._is_active
	
	@requires_driver
	def name(self) -> str:
		return self.driver.name
