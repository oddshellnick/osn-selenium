import trio
import warnings
from selenium.webdriver.common.by import By
from osn_selenium.flags.models.base import BrowserFlags
from contextlib import (
	AbstractAsyncContextManager
)
from osn_selenium.flags.base import BrowserFlagsManager
from osn_selenium.trio_base_mixin import _TrioThreadMixin
from osn_selenium.instances.trio_threads.fedcm import FedCM
from osn_selenium.instances.trio_threads.dialog import Dialog
from osn_selenium.instances.trio_threads.mobile import Mobile
from osn_selenium.instances.trio_threads.script import Script
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.instances.trio_threads.browser import Browser
from osn_selenium.instances.trio_threads.network import Network
from osn_selenium.instances.trio_threads.storage import Storage
from osn_selenium.executors.trio_threads.cdp import CDPExecutor
from osn_selenium.webdrivers._functions import build_cdp_kwargs
from osn_selenium.abstract.webdriver.base import AbstractWebDriver
from osn_selenium.instances.trio_threads.switch_to import SwitchTo
from selenium.webdriver.remote.bidi_connection import BidiConnection
from osn_selenium.executors.trio_threads.javascript import JSExecutor
from selenium.webdriver import (
	ActionChains as legacyActionChains
)
from osn_selenium.instances.trio_threads.web_element import WebElement
from osn_selenium.instances.trio_threads.permissions import Permissions
from selenium.webdriver.remote.remote_connection import RemoteConnection
from osn_selenium.instances.trio_threads.web_extension import WebExtension
from osn_selenium.dev_tools.manager import (
	DevTools,
	DevToolsSettings
)
from selenium.webdriver.remote.websocket_connection import WebSocketConnection
from osn_selenium.instances.trio_threads.browsing_context import BrowsingContext
from selenium.webdriver.remote.webdriver import (
	WebDriver as legacyWebDriver
)
from selenium.webdriver.remote.webelement import (
	WebElement as legacyWebElement
)
from osn_selenium.types import (
	DEVICES_TYPEHINT,
	Position,
	Rectangle,
	Size,
	WindowRect
)
from osn_selenium.instances.trio_threads.action_chains import (
	ActionChains,
	HumanLikeActionChains
)
from selenium.webdriver.common.virtual_authenticator import (
	Credential,
	VirtualAuthenticatorOptions
)
from typing import (
	Any,
	AsyncGenerator,
	Dict,
	List,
	Literal,
	Optional,
	Set,
	Tuple,
	Type,
	Union
)


class WebDriver(_TrioThreadMixin, AbstractWebDriver):
	def __init__(
			self,
			webdriver_path: str,
			flags_manager_type: Type[BrowserFlagsManager] = BrowserFlagsManager,
			flags: Optional[BrowserFlags] = None,
			implicitly_wait: int = 5,
			page_load_timeout: int = 5,
			script_timeout: int = 5,
			window_rect: Optional[WindowRect] = None,
			devtools_settings: Optional[DevToolsSettings] = None,
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
		
		self._dev_tools = DevTools(self, devtools_settings)
		
		self._js_executor = JSExecutor(self.execute_script)
		self._cdp_executor = CDPExecutor(self.execute_cdp_cmd)
		
		if flags is not None:
			self._webdriver_flags_manager.update_flags(flags)
	
	@requires_driver
	async def execute_cdp_cmd(self, cmd: str, cmd_args: Dict[str, Any]) -> Dict[str, Any]:
		return await self._wrap_to_trio(
				self.driver.execute_cdp_cmd,
				cmd=cmd,
				cmd_args=build_cdp_kwargs(**cmd_args)
		)
	
	@requires_driver
	async def execute(self, driver_command: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
		return await self._wrap_to_trio(self.driver.execute, driver_command=driver_command, params=params)
	
	def _ensure_driver(self) -> None:
		if self.driver is None:
			raise RuntimeError("WebDriver is not started. Call start_webdriver() first.")
	
	@requires_driver
	async def _session(self) -> Any:
		return await self._wrap_to_trio(lambda: self.driver._session)
	
	@requires_driver
	async def action_chain(
			self,
			duration: int = 250,
			devices: Optional[List[DEVICES_TYPEHINT]] = None,
	) -> ActionChains:
		return ActionChains(
				legacyActionChains(driver=self.driver, duration=duration, devices=devices),
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	@requires_driver
	async def add_cookie(self, cookie_dict: Dict[str, Any]) -> None:
		await self._wrap_to_trio(self.driver.add_cookie, cookie_dict=cookie_dict)
	
	@requires_driver
	async def add_credential(self, credential: Credential) -> None:
		await self._wrap_to_trio(self.driver.add_credential, credential=credential)
	
	@requires_driver
	async def add_virtual_authenticator(self, options: VirtualAuthenticatorOptions) -> None:
		await self._wrap_to_trio(self.driver.add_virtual_authenticator, options=options)
	
	@requires_driver
	async def back(self) -> None:
		await self._wrap_to_trio(self.driver.back)
	
	@requires_driver
	async def bidi_connection(self) -> AbstractAsyncContextManager[AsyncGenerator[BidiConnection, Any]]:
		return await self._wrap_to_trio(lambda: self.driver.bidi_connection())
	
	@requires_driver
	async def browser(self) -> Browser:
		legacy = await self._wrap_to_trio(lambda: self.driver.browser)
		
		return Browser(
				selenium_browser=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter
		)
	
	@requires_driver
	async def browsing_context(self) -> BrowsingContext:
		legacy = await self._wrap_to_trio(lambda: self.driver.browsing_context)
		
		return BrowsingContext(
				selenium_browsing_context=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	@requires_driver
	async def capabilities(self) -> Dict[str, Any]:
		return await self._wrap_to_trio(lambda: self.driver.capabilities)
	
	@property
	def cdp(self) -> CDPExecutor:
		return self._cdp_executor
	
	async def close_all_windows(self) -> None:
		for window_handle in await self.window_handles():
			await self.close_window(window_handle)
	
	@requires_driver
	async def command_executor(self) -> RemoteConnection:
		return await self._wrap_to_trio(lambda: self.driver.command_executor)
	
	@requires_driver
	async def create_web_element(self, element_id: str) -> WebElement:
		legacy = await self._wrap_to_trio(self.driver.create_web_element, element_id=element_id)
		
		return WebElement(
				selenium_web_element=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	@requires_driver
	async def current_url(self) -> str:
		return await self._wrap_to_trio(lambda: self.driver.current_url)
	
	@requires_driver
	async def delete_all_cookies(self) -> None:
		await self._wrap_to_trio(self.driver.delete_all_cookies)
	
	@requires_driver
	async def delete_cookie(self, name: str) -> None:
		await self._wrap_to_trio(self.driver.delete_cookie, name=name)
	
	@requires_driver
	async def delete_downloadable_files(self) -> None:
		await self._wrap_to_trio(self.driver.delete_downloadable_files)
	
	@property
	def dev_tools(self) -> DevTools:
		return self._dev_tools
	
	@requires_driver
	async def dialog(self) -> Dialog:
		legacy = await self._wrap_to_trio(lambda: self.driver.dialog)
		
		return Dialog(legacy, lock=self._lock, limiter=self._capacity_limiter)
	
	@requires_driver
	async def download_file(self, file_name: str, target_directory: str) -> None:
		await self._wrap_to_trio(
				self.driver.download_file,
				file_name=file_name,
				target_directory=target_directory,
		)
	
	@requires_driver
	async def execute_async_script(self, script: str, *args: Any) -> Any:
		args = self._unwrap_args(args)
		
		return self._wrap_result(
				result=await self._wrap_to_trio(self.driver.execute_async_script, script, *args)
		)
	
	@requires_driver
	async def fedcm(self) -> FedCM:
		legacy = await self._wrap_to_trio(lambda: self.driver.fedcm)
		
		return FedCM(selenium_fedcm=legacy, lock=self._lock, limiter=self._capacity_limiter)
	
	@requires_driver
	async def fedcm_dialog(
			self,
			timeout: int = 5,
			poll_frequency: float = 0.5,
			ignored_exceptions: Any = None,
	) -> Dialog:
		legacy = await self._wrap_to_trio(
				self.driver.fedcm_dialog,
				timeout=timeout,
				poll_frequency=poll_frequency,
				ignored_exceptions=ignored_exceptions,
		)
		
		return Dialog(
				selenium_dialog=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	@requires_driver
	async def file_detector(self) -> Any:
		return await self._wrap_to_trio(lambda: self.driver.file_detector)
	
	@requires_driver
	async def find_element(self, by: str = By.ID, value: Optional[str] = None) -> WebElement:
		element = await self._wrap_to_trio(self.driver.find_element, by=by, value=value)
		
		return WebElement(
				selenium_web_element=element,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	@requires_driver
	async def find_elements(self, by: str = By.ID, value: Optional[str] = None) -> List[WebElement]:
		elements = await self._wrap_to_trio(self.driver.find_elements, by=by, value=value)
		
		return [
			WebElement(
					selenium_web_element=element,
					lock=self._lock,
					limiter=self._capacity_limiter,
			) for element in elements
		]
	
	@requires_driver
	async def forward(self) -> None:
		await self._wrap_to_trio(self.driver.forward)
	
	@requires_driver
	async def fullscreen_window(self) -> None:
		await self._wrap_to_trio(self.driver.fullscreen_window)
	
	@requires_driver
	async def get_cookie(self, name: str) -> Optional[Dict[str, Any]]:
		return await self._wrap_to_trio(self.driver.get_cookie, name=name)
	
	@requires_driver
	async def get_cookies(self) -> List[Dict[str, Any]]:
		return await self._wrap_to_trio(self.driver.get_cookies)
	
	@requires_driver
	async def get_credentials(self) -> List[Credential]:
		return await self._wrap_to_trio(self.driver.get_credentials)
	
	@requires_driver
	async def get_downloadable_files(self) -> List[str]:
		return await self._wrap_to_trio(self.driver.get_downloadable_files)
	
	@requires_driver
	async def get_pinned_scripts(self) -> List[str]:
		return await self._wrap_to_trio(self.driver.get_pinned_scripts)
	
	@requires_driver
	async def get_screenshot_as_base64(self) -> str:
		return await self._wrap_to_trio(self.driver.get_screenshot_as_base64)
	
	@requires_driver
	async def get_screenshot_as_file(self, filename: str) -> bool:
		return await self._wrap_to_trio(self.driver.get_screenshot_as_file, filename=filename)
	
	@requires_driver
	async def get_screenshot_as_png(self) -> bytes:
		return await self._wrap_to_trio(self.driver.get_screenshot_as_png)
	
	@requires_driver
	async def get_window_position(self, windowHandle: str = "current") -> Position:
		position = await self._wrap_to_trio(self.driver.get_window_position, windowHandle=windowHandle)
		
		return Position.model_validate(position)
	
	@requires_driver
	async def get_window_rect(self) -> Rectangle:
		rectangle = await self._wrap_to_trio(self.driver.get_window_rect)
		
		return Rectangle.model_validate(rectangle)
	
	@requires_driver
	async def get_window_size(self, windowHandle: str = "current") -> Size:
		size = await self._wrap_to_trio(self.driver.get_window_size, windowHandle=windowHandle)
		
		return Size.model_validate(size)
	
	@requires_driver
	async def hm_action_chain(
			self,
			duration: int = 250,
			devices: Optional[List[DEVICES_TYPEHINT]] = None,
	) -> HumanLikeActionChains:
		return HumanLikeActionChains(
				driver=self,
				selenium_action_chains=legacyActionChains(driver=self.driver, duration=duration, devices=devices),
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	@requires_driver
	async def implicitly_wait(self, time_to_wait: float) -> None:
		await self._wrap_to_trio(self.driver.implicitly_wait, time_to_wait=time_to_wait)
	
	@property
	def javascript(self) -> JSExecutor:
		return self._js_executor
	
	@requires_driver
	async def maximize_window(self) -> None:
		await self._wrap_to_trio(self.driver.maximize_window)
	
	@requires_driver
	async def minimize_window(self) -> None:
		await self._wrap_to_trio(self.driver.minimize_window)
	
	@requires_driver
	async def mobile(self) -> Mobile:
		legacy = await self._wrap_to_trio(lambda: self.driver.mobile)
		
		return Mobile(
				selenium_mobile=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	@requires_driver
	async def name(self) -> str:
		return await self._wrap_to_trio(lambda: self.driver.name)
	
	@requires_driver
	async def network(self) -> Network:
		legacy = await self._wrap_to_trio(lambda: self.driver.network)
		
		return Network(
				selenium_network=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	@requires_driver
	async def orientation(self) -> Literal["LANDSCAPE", "PORTRAIT"]:
		return await self._wrap_to_trio(lambda: self.driver.orientation)
	
	@requires_driver
	async def page_source(self) -> str:
		return await self._wrap_to_trio(lambda: self.driver.page_source)
	
	@requires_driver
	async def permissions(self) -> Permissions:
		legacy = await self._wrap_to_trio(lambda: self.driver.permissions)
		
		return Permissions(
				selenium_permissions=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	@requires_driver
	async def pin_script(self, script: str, script_key: Optional[Any] = None) -> Any:
		return await self._wrap_to_trio(self.driver.pin_script, script=script, script_key=script_key)
	
	@requires_driver
	async def print_page(self, print_options: Optional[Any] = None) -> str:
		return await self._wrap_to_trio(self.driver.print_page, print_options=print_options)
	
	@requires_driver
	async def refresh(self) -> None:
		await self._wrap_to_trio(self.driver.refresh)
	
	@requires_driver
	async def set_driver_timeouts(
			self,
			page_load_timeout: float,
			implicit_wait_timeout: float,
			script_timeout: float,
	) -> None:
		def _set() -> None:
			self.driver.set_page_load_timeout(page_load_timeout)
			self.driver.implicitly_wait(implicit_wait_timeout)
			self.driver.set_script_timeout(script_timeout)
		
		await self._wrap_to_trio(_set)
	
	async def remote_connect_driver(self, command_executor: Union[str, RemoteConnection]) -> None:
		def _make() -> legacyWebDriver:
			return legacyWebDriver(
					command_executor=command_executor,
					options=self._webdriver_flags_manager.options,
			)
		
		self._driver = await self._wrap_to_trio(_make)
		
		await self.set_driver_timeouts(
				page_load_timeout=self._base_page_load_timeout,
				implicit_wait_timeout=self._base_implicitly_wait,
				script_timeout=self._base_script_timeout,
		)
		
		self._is_active = True
	
	@requires_driver
	async def remove_all_credentials(self) -> None:
		await self._wrap_to_trio(self.driver.remove_all_credentials)
	
	@requires_driver
	async def remove_credential(self, credential_id: Union[str, bytearray]) -> None:
		await self._wrap_to_trio(self.driver.remove_credential, credential_id=credential_id)
	
	@requires_driver
	async def remove_virtual_authenticator(self) -> None:
		await self._wrap_to_trio(self.driver.remove_virtual_authenticator)
	
	@property
	def is_active(self) -> bool:
		return self._is_active
	
	async def reset_settings(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		if not self.is_active:
			if window_rect is None:
				window_rect = await self._wrap_to_trio(WindowRect)
		
			if flags is not None:
				await self._wrap_to_trio(self._webdriver_flags_manager.set_flags, flags=flags)
			else:
				await self._wrap_to_trio(self._webdriver_flags_manager.clear_flags)
		
			self._window_rect = window_rect
		else:
			warnings.warn("Browser is already running.")
	
	async def _create_driver(self):
		"""
		Abstract method to create a WebDriver instance. Must be implemented in child classes.

		This method is intended to be overridden in subclasses to provide browser-specific
		WebDriver instantiation logic (e.g., creating ChromeDriver, FirefoxDriver, etc.).

		Raises:
			NotImplementedError: If the method is not implemented in a subclass.
		"""
		
		raise NotImplementedError("This function must be implemented in child classes.")
	
	async def update_settings(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		if flags is not None:
			await self._wrap_to_trio(self._webdriver_flags_manager.update_flags, flags=flags)
		
		if window_rect is not None:
			self._window_rect = window_rect
	
	async def start_webdriver(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		if self.driver is None:
			await self.update_settings(flags=flags, window_rect=window_rect)
		
			await self._create_driver()
	
	async def restart_webdriver(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		await self.close_webdriver()
		await self.start_webdriver(flags=flags, window_rect=window_rect)
	
	@requires_driver
	async def save_screenshot(self, filename: str) -> bool:
		return await self._wrap_to_trio(self.driver.save_screenshot, filename=filename)
	
	@requires_driver
	async def script(self) -> Script:
		legacy = await self._wrap_to_trio(lambda: self.driver.script)
		
		return Script(
				selenium_script=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	@requires_driver
	async def set_file_detector(self, detector: Any) -> None:
		await self._wrap_to_trio(lambda: setattr(self.driver, "file_detector", detector))
	
	@requires_driver
	async def set_orientation(self, value: Literal["LANDSCAPE", "PORTRAIT"]) -> None:
		await self._wrap_to_trio(lambda: setattr(self.driver, "orientation", value))
	
	@requires_driver
	async def set_page_load_timeout(self, time_to_wait: float) -> None:
		await self._wrap_to_trio(self.driver.set_page_load_timeout, time_to_wait=time_to_wait)
	
	@requires_driver
	async def set_script_timeout(self, time_to_wait: float) -> None:
		await self._wrap_to_trio(self.driver.set_script_timeout, time_to_wait=time_to_wait)
	
	@requires_driver
	async def set_timeouts(self, timeouts: Any) -> None:
		await self._wrap_to_trio(lambda: setattr(self.driver, "timeouts", timeouts))
	
	@requires_driver
	async def set_user_verified(self, verified: bool) -> None:
		await self._wrap_to_trio(self.driver.set_user_verified, verified=verified)
	
	@requires_driver
	async def set_window_position(self, x: int, y: int, windowHandle: str = "current") -> Position:
		position = await self._wrap_to_trio(self.driver.set_window_position, x=x, y=y, windowHandle=windowHandle)
		
		return Position.model_validate(position)
	
	@requires_driver
	async def set_window_rect(
			self,
			x: Optional[int] = None,
			y: Optional[int] = None,
			width: Optional[int] = None,
			height: Optional[int] = None,
	) -> Rectangle:
		rectangle = await self._wrap_to_trio(self.driver.set_window_rect, x=x, y=y, width=width, height=height)
		
		return Rectangle.model_validate(rectangle)
	
	@requires_driver
	async def set_window_size(self, width: int, height: int, windowHandle: str = "current") -> None:
		await self._wrap_to_trio(
				self.driver.set_window_size,
				width=width,
				height=height,
				windowHandle=windowHandle,
		)
	
	@requires_driver
	async def start_client(self) -> None:
		await self._wrap_to_trio(self.driver.start_client)
	
	@requires_driver
	async def start_devtools(self) -> Tuple[Any, WebSocketConnection]:
		return await self._wrap_to_trio(self.driver.start_devtools)
	
	@requires_driver
	async def start_session(self, capabilities: Dict[str, Any]) -> None:
		await self._wrap_to_trio(self.driver.start_session, capabilities=capabilities)
	
	@requires_driver
	async def stop_client(self) -> None:
		await self._wrap_to_trio(self.driver.stop_client)
	
	@requires_driver
	async def storage(self) -> Storage:
		legacy = await self._wrap_to_trio(lambda: self.driver.storage)
		
		return Storage(
				selenium_storage=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	@requires_driver
	async def supports_fedcm(self) -> bool:
		return await self._wrap_to_trio(lambda: self.driver.supports_fedcm)
	
	@requires_driver
	async def timeouts(self) -> Any:
		return await self._wrap_to_trio(lambda: self.driver.timeouts)
	
	@requires_driver
	async def title(self) -> str:
		return await self._wrap_to_trio(lambda: self.driver.title)
	
	@requires_driver
	async def unpin(self, script_key: Any) -> None:
		await self._wrap_to_trio(self.driver.unpin, script_key=script_key)
	
	async def update_times(
			self,
			temp_implicitly_wait: Optional[float] = None,
			temp_page_load_timeout: Optional[float] = None,
			temp_script_timeout: Optional[float] = None,
	) -> None:
		implicitly_wait = temp_implicitly_wait if temp_implicitly_wait is not None else self._base_implicitly_wait
		page_load_timeout = temp_page_load_timeout if temp_page_load_timeout is not None else self._base_page_load_timeout
		script_timeout = temp_script_timeout if temp_script_timeout is not None else self._base_script_timeout
		
		await self.set_driver_timeouts(
				page_load_timeout=page_load_timeout,
				implicit_wait_timeout=implicitly_wait,
				script_timeout=script_timeout,
		)
	
	@requires_driver
	async def virtual_authenticator_id(self) -> Optional[str]:
		return await self._wrap_to_trio(lambda: self.driver.virtual_authenticator_id)
	
	@requires_driver
	async def webextension(self) -> WebExtension:
		legacy = await self._wrap_to_trio(lambda: self.driver.webextension)
		
		return WebExtension(
				selenium_web_extension=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	@requires_driver
	async def quit(self) -> None:
		await self._wrap_to_trio(self.driver.quit)
	
	@property
	def driver(self) -> Optional[legacyWebDriver]:
		return self._driver
	
	@requires_driver
	async def close_webdriver(self) -> None:
		if self.driver is not None:
			await self.quit()
			self._driver = None
	
	@requires_driver
	async def window_handles(self) -> List[str]:
		return await self._wrap_to_trio(lambda: self.driver.window_handles)
	
	@requires_driver
	async def close(self) -> None:
		await self._wrap_to_trio(self.driver.close)
	
	@requires_driver
	async def switch_to(self) -> SwitchTo:
		legacy = await self._wrap_to_trio(lambda: self.driver.switch_to)
		
		return SwitchTo(
				selenium_switch_to=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	@requires_driver
	async def get(self, url: str) -> None:
		await self._wrap_to_trio(self.driver.get, url=url)
	
	@requires_driver
	async def current_window_handle(self) -> str:
		return await self._wrap_to_trio(lambda: self.driver.current_window_handle)
	
	async def close_window(self, window: Optional[Union[str, int]] = None) -> None:
		current = await self.current_window_handle()
		target = await self.get_window_handle(window)
		switch_to = await self.switch_to()
		
		if target == current:
			await self.close()
			remaining = await self.window_handles()
		
			if remaining:
				await switch_to.window(remaining[-1])
		else:
			await switch_to.window(target)
			await self.close()
			await switch_to.window(current)
	
	def _wrap_result(self, result: Any) -> Union[
		WebElement,
		List[legacyWebElement],
		Dict[Any, legacyWebElement],
		Set[legacyWebElement],
		Tuple[legacyWebElement, ...],
		Any,
	]:
		if isinstance(result, legacyWebElement):
			return WebElement.from_legacy(
					selenium_web_element=result,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		if isinstance(result, list):
			return [self._wrap_result(item) for item in result]
		
		if isinstance(result, dict):
			return {k: self._wrap_result(v) for k, v in result.items()}
		
		if isinstance(result, tuple):
			return tuple(self._wrap_result(item) for item in result)
		
		if isinstance(result, set):
			return {self._wrap_result(item) for item in result}
		
		return result
	
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
	
	@requires_driver
	async def execute_script(self, script: str, *args: Any) -> Any:
		args = self._unwrap_args(args)
		
		return self._wrap_result(
				result=await self._wrap_to_trio(self.driver.execute_script, script, *args)
		)
	
	async def get_window_handle(self, window: Optional[Union[str, int]] = None) -> str:
		if isinstance(window, str):
			return window
		
		if isinstance(window, int):
			handles = await self.window_handles()
		
			if not handles:
				raise RuntimeError("No window handles available")
		
			idx = window if window >= 0 else len(handles) + window
		
			if idx < 0 or idx >= len(handles):
				raise IndexError(f"Window index {window} out of range [0, {len(handles) - 1}]")
		
			return handles[idx]
		
		return await self.current_window_handle()
