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
from selenium.webdriver.remote.webdriver import (
	WebDriver as legacyWebDriver
)
from contextlib import (
	AbstractAsyncContextManager,
	contextmanager
)
from selenium.webdriver.remote.remote_connection import RemoteConnection
from selenium.webdriver.remote.websocket_connection import WebSocketConnection
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
	
	def execute_cdp_cmd(self, cmd: str, cmd_args: Dict[str, Any]) -> Any:
		self._ensure_driver()
		
		return self.driver.execute_cdp_cmd(cmd=cmd, cmd_args=build_cdp_kwargs(**cmd_args))
	
	def execute(self, driver_command: str, params: Optional[Dict[str, Any]] = None,) -> Dict[str, Any]:
		self._ensure_driver()
		
		return self.driver.execute(driver_command=driver_command, params=params,)
	
	@property
	def _session(self):
		self._ensure_driver()
		
		return self.driver._session
	
	def action_chain(
			self,
			duration: int = 250,
			devices: Optional[List[DEVICES_TYPEHINT]] = None
	) -> ActionChains:
		self._ensure_driver()
		
		return ActionChains(driver=self.driver, duration=duration, devices=devices)
	
	def add_cookie(self, cookie_dict: Dict[str, Any]):
		self._ensure_driver()
		
		return self.driver.add_cookie(cookie_dict=cookie_dict)
	
	def add_credential(self, credential: Credential):
		self._ensure_driver()
		
		self.driver.add_credential(credential=credential)
	
	def add_virtual_authenticator(self, options: VirtualAuthenticatorOptions):
		self._ensure_driver()
		
		self.driver.add_virtual_authenticator(options=options)
	
	def back(self, temp_page_load_timeout: Optional[float] = None) -> None:
		self._ensure_driver()
		
		self.update_times(temp_page_load_timeout=temp_page_load_timeout)
		
		self.driver.back()
	
	def bidi_connection(self) -> AbstractAsyncContextManager[AsyncGenerator[BidiConnection, Any]]:
		self._ensure_driver()
		
		return self.driver.bidi_connection()
	
	@property
	def browser(self) -> Browser:
		self._ensure_driver()
		
		return Browser(selenium_browser=self.driver.browser)
	
	@property
	def browsing_context(self) -> BrowsingContext:
		self._ensure_driver()
		
		return BrowsingContext(selenium_browsing_context=self.driver.browsing_context)
	
	@property
	def capabilities(self) -> Dict[str, Any]:
		self._ensure_driver()
		
		return self.driver.capabilities
	
	@property
	def cdp(self) -> CDPExecutor:
		return self._cdp_executor
	
	def close_all_windows(self):
		for window in self.window_handles:
			self.close_window(window)
	
	def create_web_element(self, element_id: str) -> WebElement:
		self._ensure_driver()
		
		return WebElement(
				selenium_web_element=self.driver.create_web_element(element_id=element_id)
		)
	
	@property
	def current_url(self) -> str:
		self._ensure_driver()
		
		return self.driver.current_url
	
	def delete_all_cookies(self):
		self._ensure_driver()
		
		self.driver.delete_all_cookies()
	
	def delete_cookie(self, name: str):
		self._ensure_driver()
		
		self.driver.delete_cookie(name=name)
	
	def delete_downloadable_files(self):
		self._ensure_driver()
		
		self.driver.delete_downloadable_files()
	
	@property
	def dialog(self) -> Dialog:
		self._ensure_driver()
		
		return Dialog(selenium_dialog=self.driver.dialog)
	
	def download_file(self, file_name: str, target_directory: pathlib.Path):
		self._ensure_driver()
		
		return self.driver.download_file(file_name=file_name, target_directory=str(target_directory.resolve()))
	
	def execute_async_script(self, script: str, *args, temp_script_timeout: Optional[float] = None,) -> Any:
		self._ensure_driver()
		
		self.update_times(temp_script_timeout=temp_script_timeout)
		
		self.driver.execute_async_script(script, *args)
	
	@property
	def fedcm(self) -> FedCM:
		self._ensure_driver()
		
		return FedCM(selenium_fedcm=self.driver.fedcm)
	
	def fedcm_dialog(
			self,
			timeout: int = 5,
			poll_frequency: float = 0.5,
			ignored_exceptions: Any = None,
	) -> Dialog:
		self._ensure_driver()
		
		return Dialog(
				selenium_dialog=self.driver.fedcm_dialog(
						timeout=timeout,
						poll_frequency=poll_frequency,
						ignored_exceptions=ignored_exceptions
				)
		)
	
	@property
	def file_detector(self) -> FileDetector:
		self._ensure_driver()
		
		return self.driver.file_detector
	
	@file_detector.setter
	def file_detector(self, detector: FileDetector) -> None:
		self._ensure_driver()
		
		self.driver.file_detector = detector
	
	@contextmanager
	def file_detector_context(self, capabilities: Dict[str, Any]) -> Generator[None, Any, None]:
		self._ensure_driver()
		
		with self.driver.file_detector_context(capabilities=capabilities):
			yield
	
	def find_element(
			self,
			by: str = By.ID,
			value: Optional[str] = None,
			temp_implicitly_wait: Optional[float] = None,
	) -> WebElement:
		self._ensure_driver()
		
		self.update_times(temp_implicitly_wait=temp_implicitly_wait)
		
		return WebElement(selenium_web_element=self.driver.find_element(by=by, value=value))
	
	def find_elements(
			self,
			by: str = By.ID,
			value: Optional[str] = None,
			temp_implicitly_wait: Optional[float] = None,
	) -> List[WebElement]:
		self._ensure_driver()
		
		self.update_times(temp_implicitly_wait=temp_implicitly_wait)
		
		return [
			WebElement(selenium_web_element=e)
			for e in self.driver.find_elements(by=by, value=value)
		]
	
	def forward(self, temp_page_load_timeout: Optional[float] = None) -> None:
		self._ensure_driver()
		
		self.update_times(temp_page_load_timeout=temp_page_load_timeout)
		
		self.driver.forward()
	
	def fullscreen_window(self):
		self._ensure_driver()
		
		self.driver.fullscreen_window()
	
	def get_cookie(self, name: str) -> Optional[Dict[str, Any]]:
		self._ensure_driver()
		
		return self.driver.get_cookie(name=name)
	
	def get_cookies(self) -> List[Dict[str, Any]]:
		self._ensure_driver()
		
		return self.driver.get_cookies()
	
	def get_credentials(self) -> List[Credential]:
		self._ensure_driver()
		
		return self.driver.get_credentials()
	
	def get_downloadable_files(self) -> List[str]:
		self._ensure_driver()
		
		return self.driver.get_downloadable_files()
	
	def get_pinned_scripts(self) -> List[str]:
		self._ensure_driver()
		
		return self.driver.get_pinned_scripts()
	
	def get_screenshot_as_base64(self) -> str:
		self._ensure_driver()
		
		return self.driver.get_screenshot_as_base64()
	
	def get_screenshot_as_file(self, filename: Union[str, PathLike[str]]) -> bool:
		self._ensure_driver()
		
		return self.driver.get_screenshot_as_file(filename=filename)
	
	def get_screenshot_as_png(self) -> bytes:
		self._ensure_driver()
		
		return self.driver.get_screenshot_as_png()
	
	def get_vars_for_remote(self) -> RemoteConnection:
		self._ensure_driver()
		
		return self.driver.command_executor
	
	def get_window_position(self, windowHandle: str = "current") -> Position:
		self._ensure_driver()
		
		position = self.driver.get_window_position(windowHandle=windowHandle)
		
		return Position(x=position["x"], y=position["y"],)
	
	def get_window_rect(self) -> Rectangle:
		self._ensure_driver()
		
		rectangle = self.driver.get_window_rect()
		
		return Rectangle(
				x=rectangle["x"],
				y=rectangle["y"],
				width=rectangle["width"],
				height=rectangle["height"],
		)
	
	def get_window_size(self, windowHandle: str = "current") -> Size:
		self._ensure_driver()
		
		size = self.driver.get_window_size(windowHandle=windowHandle)
		
		return Size(width=size["width"], height=size["height"],)
	
	def hm_action_chain(
			self,
			duration: int = 250,
			devices: Optional[List[DEVICES_TYPEHINT]] = None
	) -> HumanLikeActionChains:
		self._ensure_driver()
		
		return HumanLikeActionChains(driver=self.driver, duration=duration, devices=devices)
	
	def implicitly_wait(self, time_to_wait: float):
		self._ensure_driver()
		
		self.driver.implicitly_wait(time_to_wait=time_to_wait)
	
	@property
	def javascript(self) -> JSExecutor:
		return self._js_executor
	
	def maximize_window(self):
		self._ensure_driver()
		
		self.driver.maximize_window()
	
	def minimize_window(self):
		self._ensure_driver()
		
		self.driver.minimize_window()
	
	@property
	def mobile(self) -> Mobile:
		self._ensure_driver()
		
		return Mobile(selenium_mobile=self.driver.mobile)
	
	@property
	def name(self) -> str:
		self._ensure_driver()
		
		return self.driver.name
	
	@property
	def network(self) -> Network:
		self._ensure_driver()
		
		return Network(selenium_network=self.driver.network)
	
	@property
	def orientation(self) -> Literal["LANDSCAPE", "PORTRAIT"]:
		self._ensure_driver()
		
		return self.driver.orientation
	
	@orientation.setter
	def orientation(self, value: Literal["LANDSCAPE", "PORTRAIT"]):
		self._ensure_driver()
		
		self.driver.orientation = value
	
	@property
	def page_source(self) -> str:
		self._ensure_driver()
		
		return self.driver.page_source
	
	@property
	def permissions(self) -> Permissions:
		self._ensure_driver()
		
		return Permissions(selenium_permissions=self.driver.permissions)
	
	def pin_script(self, script: str, script_key: Optional[Any] = None) -> None:
		self._ensure_driver()
		
		self.driver.pin_script(script=script, script_key=script_key)
	
	def print_page(self, print_options: Optional[PrintOptions] = None) -> str:
		self._ensure_driver()
		
		return self.driver.print_page(print_options=print_options)
	
	def refresh(self, temp_page_load_timeout: Optional[float] = None) -> None:
		self._ensure_driver()
		
		self.update_times(temp_page_load_timeout=temp_page_load_timeout)
		
		self.driver.refresh()
	
	@property
	def timeouts(self) -> Timeouts:
		self._ensure_driver()
		
		return self.driver.timeouts
	
	@timeouts.setter
	def timeouts(self, timeouts: Timeouts) -> None:
		self._ensure_driver()
		
		self.driver.timeouts = timeouts
	
	def remote_connect_driver(self, command_executor: Union[str, RemoteConnection]):
		self._ensure_driver()
		
		self._driver = webdriver.Remote(
				command_executor=command_executor,
				options=self._webdriver_flags_manager.options
		)
		
		self.timeouts = Timeouts(
				page_load=self._base_page_load_timeout,
				implicit_wait=self._base_implicitly_wait,
				script=self._base_script_timeout,
		)
	
	def remove_all_credentials(self):
		self._ensure_driver()
		
		self.driver.remove_all_credentials()
	
	def remove_credential(self, credential_id: Union[str, bytearray]):
		self._ensure_driver()
		
		self.driver.remove_credential(credential_id=credential_id)
	
	def remove_virtual_authenticator(self):
		self._ensure_driver()
		
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
			self.update_settings(flags=flags, window_rect=window_rect,)
		
			self._create_driver()
	
	def restart_webdriver(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	):
		self.close_webdriver()
		self.start_webdriver(flags=flags, window_rect=window_rect,)
	
	def save_screenshot(self, filename: Union[str, PathLike[str]]) -> bool:
		self._ensure_driver()
		
		return self.driver.save_screenshot(filename=filename)
	
	@property
	def script(self) -> Script:
		self._ensure_driver()
		
		return Script(selenium_script=self.driver.script)
	
	def set_page_load_timeout(self, time_to_wait: float):
		self._ensure_driver()
		
		self.driver.set_page_load_timeout(time_to_wait=time_to_wait)
	
	def set_script_timeout(self, time_to_wait: float):
		self._ensure_driver()
		
		self.driver.set_script_timeout(time_to_wait=time_to_wait)
	
	def set_user_verified(self, verified: bool):
		self._ensure_driver()
		
		self.driver.set_user_verified(verified=verified)
	
	def set_window_position(self, x: int, y: int, windowHandle: str = "current") -> Rectangle:
		self._ensure_driver()
		
		rectangle = self.driver.set_window_position(x=x, y=y, windowHandle=windowHandle,)
		
		return Rectangle(
				x=rectangle["x"],
				y=rectangle["y"],
				width=rectangle["width"],
				height=rectangle["height"],
		)
	
	def set_window_rect(
			self,
			x: Optional[int] = None,
			y: Optional[int] = None,
			width: Optional[int] = None,
			height: Optional[int] = None,
	):
		self._ensure_driver()
		
		self.driver.set_window_rect(x=x, y=y, width=width, height=height)
	
	def set_window_size(self, width: int, height: int, windowHandle: str = "current") -> None:
		self._ensure_driver()
		
		self.driver.set_window_size(width=width, height=height, windowHandle=windowHandle,)
	
	def start_client(self):
		self._ensure_driver()
		
		self.driver.start_client()
	
	def start_devtools(self) -> Tuple[Any, WebSocketConnection]:
		self._ensure_driver()
		
		return self.driver.start_devtools()
	
	def start_session(self, capabilities: Dict[str, Any]) -> None:
		self._ensure_driver()
		
		self.driver.start_session(capabilities=capabilities)
	
	def stop_client(self):
		self._ensure_driver()
		
		self.driver.stop_client()
	
	@property
	def storage(self) -> Storage:
		self._ensure_driver()
		
		return Storage(selenium_storage=self.driver.storage)
	
	@property
	def supports_fedcm(self) -> bool:
		self._ensure_driver()
		
		return self.driver.supports_fedcm
	
	@property
	def switch_to(self) -> SwitchTo:
		self._ensure_driver()
		
		return SwitchTo(selenium_switch_to=self.driver.switch_to)
	
	@property
	def title(self) -> str:
		self._ensure_driver()
		
		return self.driver.title
	
	def unpin(self, script_key: ScriptKey) -> None:
		self._ensure_driver()
		
		self.driver.unpin(script_key=script_key)
	
	@property
	def virtual_authenticator_id(self) -> Optional[str]:
		self._ensure_driver()
		
		return self.driver.virtual_authenticator_id
	
	@property
	def webextension(self) -> WebExtension:
		self._ensure_driver()
		
		return WebExtension(selenium_web_extension=self.driver.webextension)
	
	@property
	def driver(self) -> Optional[legacyWebDriver]:
		return self._driver
	
	def _ensure_driver(self) -> None:
		if self.driver is None:
			raise RuntimeError("WebDriver is not started. Call start_webdriver() first.")
	
	def quit(self):
		self._ensure_driver()
		
		self.driver.quit()
	
	def close_webdriver(self):
		if self.driver is not None:
			self.quit()
			self._driver = None
	
	@property
	def window_handles(self) -> List[str]:
		self._ensure_driver()
		
		return self.driver.window_handles
	
	def close(self) -> None:
		self._ensure_driver()
		
		self.driver.close()
	
	def set_driver_timeouts(
			self,
			page_load_timeout: float,
			implicit_wait_timeout: float,
			script_timeout: float,
	) -> None:
		self._ensure_driver()
		
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
	
	def get(self, url: str, temp_page_load_timeout: Optional[float] = None):
		self._ensure_driver()
		
		self.update_times(temp_page_load_timeout=temp_page_load_timeout)
		
		self.driver.get(url=url)
	
	@property
	def current_window_handle(self) -> str:
		self._ensure_driver()
		
		return self.driver.current_window_handle
	
	def close_window(self, window: Optional[Union[str, int]] = None):
		self._ensure_driver()
		
		start_window_handle = self.current_window_handle
		close_window_handle = self.get_window_handle(window)
		
		is_current_closing = close_window_handle == start_window_handle
		
		if not is_current_closing:
			self.switch_to.window(close_window_handle)
		
		self.close()
		
		if len(self.window_handles) > 0:
			if is_current_closing:
				self.switch_to.window(self.get_window_handle(-1))
			else:
				self.switch_to.window(start_window_handle)
	
	def execute_script(self, script: str, *args, temp_script_timeout: Optional[float] = None,) -> Any:
		self._ensure_driver()
		
		self.update_times(temp_script_timeout=temp_script_timeout)
		
		return self.driver.execute_script(script, *args)
	
	def get_window_handle(self, window: Optional[Union[str, int]] = None) -> str:
		if isinstance(window, str):
			return window
		
		if isinstance(window, int):
			return self.window_handles[window]
		
		return self.current_window_handle

	async def set_file_detector(self, detector: Any) -> None:
		self._ensure_driver()

		self.driver.file_detector = detector

	async def set_orientation(self, value: Literal["LANDSCAPE", "PORTRAIT"]) -> None:
		self._ensure_driver()

		self.driver.orientation = value

	async def set_timeouts(self, timeouts: Any) -> None:
		self._ensure_driver()

		self.driver.timeouts = timeouts
