import pathlib
import warnings
from os import PathLike
from selenium import webdriver
from selenium.webdriver.common.by import By
from osn_selenium.instances.sync.fedcm import FedCM
from osn_selenium.instances.sync.dialog import Dialog
from osn_selenium.instances.sync.mobile import Mobile
from osn_selenium.instances.sync.script import Script
from osn_selenium.flags.utils.base import BrowserFlags
from selenium.webdriver.common.timeouts import Timeouts
from osn_selenium.executors.sync.cdp import CDPExecutor
from osn_selenium.flags.base import BrowserFlagsManager
from osn_selenium.instances.sync.browser import Browser
from osn_selenium.instances.sync.network import Network
from osn_selenium.instances.sync.storage import Storage
from osn_selenium.trio_base_mixin import requires_driver
from selenium.webdriver.remote.script_key import ScriptKey
from osn_selenium.instances.sync.switch_to import SwitchTo
from osn_selenium.webdrivers._utils import build_cdp_kwargs
from osn_selenium.executors.sync.javascript import JSExecutor
from osn_selenium.instances.sync.web_element import WebElement
from osn_selenium.instances.sync.permissions import Permissions
from selenium.webdriver.remote.file_detector import FileDetector
from osn_selenium.instances.sync.web_extension import WebExtension
from osn_selenium.abstract.webdriver.base import AbstractWebDriver
from selenium.webdriver.remote.bidi_connection import BidiConnection
from selenium.webdriver.common.print_page_options import PrintOptions
from osn_selenium.instances.sync.browsing_context import BrowsingContext
from contextlib import (
	AbstractAsyncContextManager,
	contextmanager
)
from selenium.webdriver.remote.remote_connection import RemoteConnection
from selenium.webdriver.remote.websocket_connection import WebSocketConnection
from selenium.webdriver.remote.webdriver import (
	WebDriver as legacyWebDriver
)
from osn_selenium.instances.sync.action_chains import (
	ActionChains,
	HumanLikeActionChains
)
from osn_selenium.types import (
	DEVICES_TYPEHINT,
	Position,
	Rectangle,
	Size,
	WindowRect
)
from selenium.webdriver.common.virtual_authenticator import (
	Credential,
	VirtualAuthenticatorOptions
)
from typing import (
	Any,
	AsyncGenerator,
	Dict,
	Generator,
	List,
	Literal,
	Optional,
	Tuple,
	Type,
	Union
)


class WebDriver(AbstractWebDriver):
	def __init__(
			self,
			webdriver_path: str,
			flags_manager_type: Type[BrowserFlagsManager] = BrowserFlagsManager,
			flags: Optional[BrowserFlags] = None,
			implicitly_wait: int = 5,
			page_load_timeout: int = 5,
			script_timeout: int = 5,
			window_rect: Optional[WindowRect] = None,
	):
		self._window_rect = window_rect
		self._webdriver_path = webdriver_path
		self._webdriver_flags_manager = flags_manager_type()
		self._driver: Optional[Union[webdriver.Chrome, webdriver.Edge, webdriver.Firefox]] = None
		self._base_implicitly_wait = implicitly_wait
		self._base_page_load_timeout = page_load_timeout
		self._base_script_timeout = script_timeout
		self._is_active = False
		self._js_executor = JSExecutor(self.execute_script)
		self._cdp_executor = CDPExecutor(self.execute_cdp_cmd)
		
		self.update_settings(flags=flags)
	
	@requires_driver
	def execute_cdp_cmd(self, cmd: str, cmd_args: Dict[str, Any]) -> Any:
		return self.driver.execute_cdp_cmd(cmd=cmd, cmd_args=build_cdp_kwargs(**cmd_args))
	
	@requires_driver
	def execute(self, driver_command: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
		return self.driver.execute(driver_command=driver_command, params=params)
	
	def _ensure_driver(self) -> None:
		if self.driver is None:
			raise RuntimeError("WebDriver is not started. Call start_webdriver() first.")

	@requires_driver
	def _session(self):
		return self.driver._session
	
	@requires_driver
	def action_chain(
			self,
			duration: int = 250,
			devices: Optional[List[DEVICES_TYPEHINT]] = None
	) -> ActionChains:
		return ActionChains(driver=self.driver, duration=duration, devices=devices)
	
	@requires_driver
	def add_cookie(self, cookie_dict: Dict[str, Any]):
		return self.driver.add_cookie(cookie_dict=cookie_dict)
	
	@requires_driver
	def add_credential(self, credential: Credential):
		self.driver.add_credential(credential=credential)
	
	@requires_driver
	def add_virtual_authenticator(self, options: VirtualAuthenticatorOptions):
		self.driver.add_virtual_authenticator(options=options)
	
	@requires_driver
	def back(self) -> None:
		self.driver.back()
	
	@requires_driver
	def bidi_connection(self) -> AbstractAsyncContextManager[AsyncGenerator[BidiConnection, Any]]:
		return self.driver.bidi_connection()

	@requires_driver
	def browser(self) -> Browser:
		return Browser(selenium_browser=self.driver.browser)

	@requires_driver
	def browsing_context(self) -> BrowsingContext:
		return BrowsingContext(selenium_browsing_context=self.driver.browsing_context)

	@requires_driver
	def capabilities(self) -> Dict[str, Any]:
		return self.driver.capabilities
	
	@property
	def cdp(self) -> CDPExecutor:
		return self._cdp_executor
	
	def close_all_windows(self) -> None:
		for window_handle in self.window_handles():
			self.close_window(window_handle)

	@requires_driver
	def command_executor(self) -> RemoteConnection:
		return self.driver.command_executor
	
	@requires_driver
	def create_web_element(self, element_id: str) -> WebElement:
		legacy = self.driver.create_web_element(element_id=element_id)
		
		return WebElement(selenium_web_element=legacy)

	@requires_driver
	def current_url(self) -> str:
		return self.driver.current_url
	
	@requires_driver
	def delete_all_cookies(self):
		self.driver.delete_all_cookies()
	
	@requires_driver
	def delete_cookie(self, name: str):
		self.driver.delete_cookie(name=name)
	
	@requires_driver
	def delete_downloadable_files(self):
		self.driver.delete_downloadable_files()

	@requires_driver
	def dialog(self) -> Dialog:
		return Dialog(selenium_dialog=self.driver.dialog)
	
	@requires_driver
	def download_file(self, file_name: str, target_directory: pathlib.Path):
		return self.driver.download_file(file_name=file_name, target_directory=str(target_directory.resolve()))
	
	@requires_driver
	def execute_async_script(self, script: str, *args) -> Any:
		args = [arg if not isinstance(arg, WebElement) else arg.legacy for arg in args]
		
		self.driver.execute_async_script(script, *args)

	@requires_driver
	def fedcm(self) -> FedCM:
		return FedCM(selenium_fedcm=self.driver.fedcm)
	
	@requires_driver
	def fedcm_dialog(
			self,
			timeout: int = 5,
			poll_frequency: float = 0.5,
			ignored_exceptions: Any = None,
	) -> Dialog:
		legacy = self.driver.fedcm_dialog(
				timeout=timeout,
				poll_frequency=poll_frequency,
				ignored_exceptions=ignored_exceptions,
		)
		
		return Dialog(selenium_dialog=legacy)

	@requires_driver
	def file_detector(self) -> FileDetector:
		return self.driver.file_detector

	@contextmanager
	@requires_driver
	def file_detector_context(self, capabilities: Dict[str, Any]) -> Generator[None, Any, None]:
		with self.driver.file_detector_context(capabilities=capabilities):
			yield
	
	@requires_driver
	def find_element(self, by: str = By.ID, value: Optional[str] = None,) -> WebElement:
		element = self.driver.find_element(by=by, value=value)
		
		return WebElement(selenium_web_element=element)
	
	@requires_driver
	def find_elements(self, by: str = By.ID, value: Optional[str] = None,) -> List[WebElement]:
		elements = self.driver.find_elements(by=by, value=value)
		
		return [WebElement(selenium_web_element=element) for element in elements]
	
	@requires_driver
	def forward(self) -> None:
		self.driver.forward()
	
	@requires_driver
	def fullscreen_window(self):
		self.driver.fullscreen_window()
	
	@requires_driver
	def get_cookie(self, name: str) -> Optional[Dict[str, Any]]:
		return self.driver.get_cookie(name=name)
	
	@requires_driver
	def get_cookies(self) -> List[Dict[str, Any]]:
		return self.driver.get_cookies()
	
	@requires_driver
	def get_credentials(self) -> List[Credential]:
		return self.driver.get_credentials()
	
	@requires_driver
	def get_downloadable_files(self) -> List[str]:
		return self.driver.get_downloadable_files()
	
	@requires_driver
	def get_pinned_scripts(self) -> List[str]:
		return self.driver.get_pinned_scripts()
	
	@requires_driver
	def get_screenshot_as_base64(self) -> str:
		return self.driver.get_screenshot_as_base64()
	
	@requires_driver
	def get_screenshot_as_file(self, filename: Union[str, PathLike[str]]) -> bool:
		return self.driver.get_screenshot_as_file(filename=filename)
	
	@requires_driver
	def get_screenshot_as_png(self) -> bytes:
		return self.driver.get_screenshot_as_png()
	
	@requires_driver
	def get_window_position(self, windowHandle: str = "current") -> Position:
		position = self.driver.get_window_position(windowHandle=windowHandle)
		
		return Position(x=position["x"], y=position["y"])
	
	@requires_driver
	def get_window_rect(self) -> Rectangle:
		rectangle = self.driver.get_window_rect()
		
		return Rectangle(
				x=rectangle["x"],
				y=rectangle["y"],
				width=rectangle["width"],
				height=rectangle["height"],
		)
	
	@requires_driver
	def get_window_size(self, windowHandle: str = "current") -> Size:
		size = self.driver.get_window_size(windowHandle=windowHandle)
		
		return Size(width=size["width"], height=size["height"])
	
	@requires_driver
	def hm_action_chain(
			self,
			duration: int = 250,
			devices: Optional[List[DEVICES_TYPEHINT]] = None
	) -> HumanLikeActionChains:
		return HumanLikeActionChains(driver=self.driver, duration=duration, devices=devices)
	
	@requires_driver
	def implicitly_wait(self, time_to_wait: float):
		self.driver.implicitly_wait(time_to_wait=time_to_wait)

	@property
	def javascript(self) -> JSExecutor:
		return self._js_executor
	
	@requires_driver
	def maximize_window(self):
		self.driver.maximize_window()
	
	@requires_driver
	def minimize_window(self):
		self.driver.minimize_window()

	@requires_driver
	def mobile(self) -> Mobile:
		return Mobile(selenium_mobile=self.driver.mobile)

	@requires_driver
	def name(self) -> str:
		return self.driver.name

	@requires_driver
	def network(self) -> Network:
		return Network(selenium_network=self.driver.network)

	@requires_driver
	def orientation(self) -> Literal["LANDSCAPE", "PORTRAIT"]:
		return self.driver.orientation

	@requires_driver
	def page_source(self) -> str:
		return self.driver.page_source

	@requires_driver
	def permissions(self) -> Permissions:
		return Permissions(selenium_permissions=self.driver.permissions)
	
	@requires_driver
	def pin_script(self, script: str, script_key: Optional[Any] = None) -> None:
		self.driver.pin_script(script=script, script_key=script_key)
	
	@requires_driver
	def print_page(self, print_options: Optional[PrintOptions] = None) -> str:
		return self.driver.print_page(print_options=print_options)
	
	@requires_driver
	def refresh(self) -> None:
		self.driver.refresh()

	@requires_driver
	def timeouts(self) -> Timeouts:
		return self.driver.timeouts

	@requires_driver
	def remote_connect_driver(self, command_executor: Union[str, RemoteConnection]):
		self._driver = webdriver.Remote(
				command_executor=command_executor,
				options=self._webdriver_flags_manager.options,
		)
		
		self.set_timeouts(
				timeouts=Timeouts(
						page_load=self._base_page_load_timeout,
						implicit_wait=self._base_implicitly_wait,
						script=self._base_script_timeout,
				)
		)
	
	@requires_driver
	def remove_all_credentials(self):
		self.driver.remove_all_credentials()
	
	@requires_driver
	def remove_credential(self, credential_id: Union[str, bytearray]):
		self.driver.remove_credential(credential_id=credential_id)
	
	@requires_driver
	def remove_virtual_authenticator(self):
		self.driver.remove_virtual_authenticator()
	
	@property
	def is_active(self) -> bool:
		return self._is_active
	
	def reset_settings(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	):
		if not self.is_active:
			if window_rect is None:
				window_rect = WindowRect()
		
			if flags is not None:
				self._webdriver_flags_manager.set_flags(flags)
			else:
				self._webdriver_flags_manager.clear_flags()
		
			self._window_rect = window_rect
		else:
			warnings.warn("Browser is already running.")
	
	def _create_driver(self):
		raise NotImplementedError("This function must be implemented in child classes.")
	
	def update_settings(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	):
		if flags is not None:
			self._webdriver_flags_manager.update_flags(flags)
		
		if window_rect is not None:
			self._window_rect = window_rect
	
	def start_webdriver(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	):
		if self.driver is None:
			self.update_settings(flags=flags, window_rect=window_rect)
		
			self._create_driver()
	
	def restart_webdriver(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	):
		self.close_webdriver()
		self.start_webdriver(flags=flags, window_rect=window_rect)
	
	@requires_driver
	def save_screenshot(self, filename: Union[str, PathLike[str]]) -> bool:
		return self.driver.save_screenshot(filename=filename)

	@requires_driver
	def script(self) -> Script:
		return Script(selenium_script=self.driver.script)
	
	@requires_driver
	def set_file_detector(self, detector: Any) -> None:
		self.driver.file_detector = detector
	
	@requires_driver
	def set_orientation(self, value: Literal["LANDSCAPE", "PORTRAIT"]) -> None:
		self.driver.orientation = value
	
	@requires_driver
	def set_page_load_timeout(self, time_to_wait: float):
		self.driver.set_page_load_timeout(time_to_wait=time_to_wait)
	
	@requires_driver
	def set_script_timeout(self, time_to_wait: float):
		self.driver.set_script_timeout(time_to_wait=time_to_wait)
	
	@requires_driver
	def set_timeouts(self, timeouts: Any) -> None:
		self.driver.timeouts = timeouts
	
	@requires_driver
	def set_user_verified(self, verified: bool):
		self.driver.set_user_verified(verified=verified)
	
	@requires_driver
	def set_window_position(self, x: int, y: int, windowHandle: str = "current") -> Rectangle:
		rectangle = self.driver.set_window_position(x=x, y=y, windowHandle=windowHandle)
		
		return Rectangle(
				x=rectangle["x"],
				y=rectangle["y"],
				width=rectangle["width"],
				height=rectangle["height"],
		)
	
	@requires_driver
	def set_window_rect(
			self,
			x: Optional[int] = None,
			y: Optional[int] = None,
			width: Optional[int] = None,
			height: Optional[int] = None,
	):
		self.driver.set_window_rect(x=x, y=y, width=width, height=height)
	
	@requires_driver
	def set_window_size(self, width: int, height: int, windowHandle: str = "current") -> None:
		self.driver.set_window_size(width=width, height=height, windowHandle=windowHandle)
	
	@requires_driver
	def start_client(self):
		self.driver.start_client()
	
	@requires_driver
	def start_devtools(self) -> Tuple[Any, WebSocketConnection]:
		return self.driver.start_devtools()
	
	@requires_driver
	def start_session(self, capabilities: Dict[str, Any]) -> None:
		self.driver.start_session(capabilities=capabilities)
	
	@requires_driver
	def stop_client(self):
		self.driver.stop_client()

	@requires_driver
	def storage(self) -> Storage:
		return Storage(selenium_storage=self.driver.storage)

	@requires_driver
	def supports_fedcm(self) -> bool:
		return self.driver.supports_fedcm

	@requires_driver
	def title(self) -> str:
		return self.driver.title
	
	@requires_driver
	def unpin(self, script_key: ScriptKey) -> None:
		self.driver.unpin(script_key=script_key)
	
	@requires_driver
	def set_driver_timeouts(
			self,
			page_load_timeout: float,
			implicit_wait_timeout: float,
			script_timeout: float,
	) -> None:
		self.driver.set_page_load_timeout(page_load_timeout)
		self.driver.implicitly_wait(implicit_wait_timeout)
		self.driver.set_script_timeout(script_timeout)
	
	def update_times(
			self,
			temp_implicitly_wait: Optional[float] = None,
			temp_page_load_timeout: Optional[float] = None,
			temp_script_timeout: Optional[float] = None,
	):
		implicitly_wait = temp_implicitly_wait if temp_implicitly_wait is not None else self._base_implicitly_wait
		page_load_timeout = temp_page_load_timeout if temp_page_load_timeout is not None else self._base_page_load_timeout
		script_timeout = temp_script_timeout if temp_script_timeout is not None else self._base_script_timeout
		
		self.set_driver_timeouts(
				page_load_timeout=page_load_timeout,
				implicit_wait_timeout=implicitly_wait,
				script_timeout=script_timeout,
		)

	@requires_driver
	def virtual_authenticator_id(self) -> Optional[str]:
		return self.driver.virtual_authenticator_id

	@requires_driver
	def webextension(self) -> WebExtension:
		return WebExtension(selenium_web_extension=self.driver.webextension)
	
	@requires_driver
	def quit(self):
		self.driver.quit()
	
	@property
	def driver(self) -> Optional[legacyWebDriver]:
		return self._driver
	
	def close_webdriver(self):
		if self.driver is not None:
			self.quit()
			self._driver = None

	@requires_driver
	def switch_to(self) -> SwitchTo:
		return SwitchTo(selenium_switch_to=self.driver.switch_to)

	@requires_driver
	def window_handles(self) -> List[str]:
		return self.driver.window_handles
	
	@requires_driver
	def close(self) -> None:
		self.driver.close()
	
	@requires_driver
	def get(self, url: str):
		self.driver.get(url=url)

	@requires_driver
	def current_window_handle(self) -> str:
		return self.driver.current_window_handle
	
	def close_window(self, window: Optional[Union[str, int]] = None):
		current = self.current_window_handle()
		target = self.get_window_handle(window)
		switch_to = self.switch_to()
		
		if target == current:
			self.close()
			remaining = self.window_handles()
		
			if remaining:
				switch_to.window(remaining[-1])
		else:
			switch_to.window(target)
			self.close()
			switch_to.window(current)
	
	@requires_driver
	def execute_script(self, script: str, *args) -> Any:
		args = [arg if not isinstance(arg, WebElement) else arg.legacy for arg in args]
		
		return self.driver.execute_script(script, *args)
	
	def get_window_handle(self, window: Optional[Union[str, int]] = None) -> str:
		if isinstance(window, str):
			return window
		
		if isinstance(window, int):
			handles = self.window_handles()
		
			if not handles:
				raise RuntimeError("No window handles available")
		
			idx = window if window >= 0 else len(handles) + window
		
			if idx < 0 or idx >= len(handles):
				raise IndexError(f"Window index {window} out of range [0, {len(handles) - 1}]")
		
			return handles[idx]
		
		return self.current_window_handle()
