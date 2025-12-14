from selenium import webdriver
from abc import ABC, abstractmethod
from selenium.webdriver.common.by import By
from trio_websocket import WebSocketConnection
from osn_selenium.flags.models.base import BrowserFlags
from contextlib import (
	AbstractAsyncContextManager
)
from osn_selenium.abstract.instances.fedcm import AbstractFedCM
from osn_selenium.abstract.instances.script import AbstractScript
from osn_selenium.abstract.instances.dialog import AbstractDialog
from osn_selenium.abstract.instances.mobile import AbstractMobile
from osn_selenium.abstract.executors.cdp import AbstractCDPExecutor
from osn_selenium.abstract.instances.browser import AbstractBrowser
from osn_selenium.abstract.instances.network import AbstractNetwork
from osn_selenium.abstract.instances.storage import AbstractStorage
from selenium.webdriver.remote.bidi_connection import BidiConnection
from osn_selenium.abstract.instances.switch_to import AbstractSwitchTo
from selenium.webdriver.remote.remote_connection import RemoteConnection
from osn_selenium.abstract.executors.javascript import AbstractJSExecutor
from osn_selenium.abstract.instances.web_element import AbstractWebElement
from osn_selenium.abstract.instances.permissions import AbstractPermissions
from osn_selenium.abstract.instances.web_extension import AbstractWebExtension
from selenium.webdriver.chromium.webdriver import (
	ChromiumDriver as legacyWebDriver
)
from osn_selenium.abstract.instances.browsing_context import (
	AbstractBrowsingContext
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
from osn_selenium.abstract.instances.action_chains import (
	AbstractActionChains,
	AbstractHumanLikeActionChains
)
from typing import (
	Any,
	AsyncGenerator,
	Dict,
	List,
	Literal,
	Mapping,
	Optional,
	Sequence,
	Set,
	Tuple,
	Union
)


class AbstractWebDriver(ABC):
	"""
	Abstract base class for a WebDriver.

	This class defines the interface that all WebDriver implementations must adhere to.
	It includes methods for browser navigation, element interaction, script execution,
	and managing various browser features.
	"""
	
	@abstractmethod
	def _create_driver(self) -> None:
		"""
		Internal method to create the WebDriver instance. Must be implemented by subclasses.
		"""
		
		...
	
	@abstractmethod
	def _ensure_driver(self) -> Optional[legacyWebDriver]:
		"""
		Internal method to ensure the WebDriver instance is running before an operation.

		Returns:
			Optional[legacyWebDriver]: The driver instance if verified, otherwise None.

		Raises:
			RuntimeError: If the driver is not started.
		"""
		
		...
	
	@abstractmethod
	def _session(self) -> Any:
		"""
		Internal method to access the current session object.

		Returns:
			Any: The session object.
		"""
		
		...
	
	def _unwrap_args(self, arg: Any) -> Any:
		...
	
	def _wrap_result(self, result: Any) -> Union[
		AbstractWebElement,
		List[AbstractWebElement],
		Dict[Any, AbstractWebElement],
		Set[AbstractWebElement],
		Tuple[AbstractWebElement, ...],
		Any,
	]:
		...
	
	@abstractmethod
	def action_chain(
			self,
			duration: int = 250,
			devices: Optional[Sequence[DEVICES_TYPEHINT]] = None
	) -> AbstractActionChains:
		"""
		Creates a new ActionChains instance for building complex user interactions.

		Args:
			duration (int): The default duration for pointer actions in milliseconds.
			devices (Optional[Sequence[DEVICES_TYPEHINT]]): A sequence of input devices to use.

		Returns:
			AbstractActionChains: A new ActionChains instance.
		"""
		
		...
	
	@abstractmethod
	def add_cookie(self, cookie_dict: Mapping[str, Any]) -> None:
		"""
		Adds a cookie to the current session.

		Args:
			cookie_dict (Mapping[str, Any]): A dictionary representing the cookie to add.
		"""
		
		...
	
	@abstractmethod
	def add_credential(self, credential: Credential) -> None:
		"""
		Adds a credential to the virtual authenticator.

		Args:
			credential (Credential): The credential to add.
		"""
		
		...
	
	@abstractmethod
	def add_virtual_authenticator(self, options: VirtualAuthenticatorOptions) -> None:
		"""
		Adds a virtual authenticator for testing web authentication.

		Args:
			options (VirtualAuthenticatorOptions): Configuration for the virtual authenticator.
		"""
		
		...
	
	@abstractmethod
	def back(self) -> None:
		"""
		Goes one step backward in the browser history.
		"""
		
		...
	
	@abstractmethod
	def bidi_connection(self) -> AbstractAsyncContextManager[AsyncGenerator[BidiConnection, Any]]:
		"""
		Returns an async context manager for a BiDi (WebDriver Bi-Directional) connection.

		Returns:
			AbstractAsyncContextManager[AsyncGenerator[BidiConnection, Any]]: The BiDi connection context manager.
		"""
		
		...
	
	@abstractmethod
	def browser(self) -> AbstractBrowser:
		"""
		Provides access to browser-level actions.

		Returns:
			AbstractBrowser: An object for controlling browser-level features.
		"""
		
		...
	
	@abstractmethod
	def browsing_context(self) -> AbstractBrowsingContext:
		"""
		Provides access to the browsing context interface (e.g., tabs, windows).

		Returns:
			AbstractBrowsingContext: An object for managing browsing contexts.
		"""
		
		...
	
	@abstractmethod
	def capabilities(self) -> Mapping[str, Any]:
		"""
		Returns the capabilities of the current session.

		Returns:
			Mapping[str, Any]: A dictionary of session capabilities.
		"""
		
		...
	
	@abstractmethod
	def cdp(self) -> AbstractCDPExecutor:
		"""
		Returns the CDP (Chrome DevTools Protocol) executor.

		Returns:
			AbstractCDPExecutor: The CDP executor instance.
		"""
		
		...
	
	@abstractmethod
	def close(self) -> None:
		"""
		Closes the current window.
		"""
		
		...
	
	@abstractmethod
	def close_all_windows(self) -> None:
		"""
		Closes all open windows in the current session.
		"""
		
		...
	
	@abstractmethod
	async def close_webdriver(self) -> None:
		"""
		Closes the WebDriver instance and all associated windows.
		"""
		
		...
	
	@abstractmethod
	def close_window(self, window: Optional[Union[str, int]] = None) -> None:
		"""
		Closes a specific window by handle or index, or the current window if not specified.
		If the closed window was the current one, attempts to switch to the last remaining window.

		Args:
			window (Optional[Union[str, int]]): The window handle (str) or index (int) to close.
		"""
		
		...
	
	@abstractmethod
	def command_executor(self) -> RemoteConnection:
		"""
		Gets the remote connection manager used for executing commands.

		Returns:
			RemoteConnection: The remote connection instance.
		"""
		
		...
	
	@abstractmethod
	def create_web_element(self, element_id: str) -> AbstractWebElement:
		"""
		Creates a WebElement from an element ID.

		Args:
			element_id (str): The ID of the element.

		Returns:
			AbstractWebElement: The created WebElement instance.
		"""
		
		...
	
	@abstractmethod
	def current_url(self) -> str:
		"""
		Gets the URL of the current page.

		Returns:
			str: The URL of the current page.
		"""
		
		...
	
	@abstractmethod
	def current_window_handle(self) -> str:
		"""
		Returns the handle of the current window.

		Returns:
			str: The handle of the current window.
		"""
		
		...
	
	@abstractmethod
	def delete_all_cookies(self) -> None:
		"""
		Deletes all cookies for the current session.
		"""
		
		...
	
	@abstractmethod
	def delete_cookie(self, name: str) -> None:
		"""
		Deletes a single cookie with the given name.

		Args:
			name (str): The name of the cookie to delete.
		"""
		
		...
	
	@abstractmethod
	def delete_downloadable_files(self) -> None:
		"""
		Deletes all files currently available for download.
		"""
		
		...
	
	@abstractmethod
	def dialog(self) -> AbstractDialog:
		"""
		Provides access to the dialog (alert, prompt, confirm) interface.

		Returns:
			AbstractDialog: An object for interacting with browser dialogs.
		"""
		
		...
	
	@abstractmethod
	def download_file(self, file_name: str, target_directory: str) -> None:
		"""
		Downloads a specified file to a target directory.

		Args:
			file_name (str): The name of the file to download.
			target_directory (str): The directory to save the file in.
		"""
		
		...
	
	@abstractmethod
	def driver(self) -> Optional[Union[webdriver.Chrome, webdriver.Edge, webdriver.Firefox]]:
		"""
		Returns the underlying Selenium WebDriver instance.

		Returns:
			Optional[Union[webdriver.Chrome, webdriver.Edge, webdriver.Firefox]]: The driver instance, or None if not started.
		"""
		
		...
	
	@abstractmethod
	def execute(self, driver_command: str, params: Optional[Mapping[str, Any]] = None) -> Mapping[str, Any]:
		"""
		Sends a command to be executed by the remote driver.

		Args:
			driver_command (str): The name of the command to execute.
			params (Optional[Mapping[str, Any]]): A dictionary of parameters for the command.

		Returns:
			Mapping[str, Any]: The response from the driver.
		"""
		
		...
	
	@abstractmethod
	def execute_async_script(self, script: str, *args: Any) -> Any:
		"""
		Asynchronously executes JavaScript in the current window/frame.

		Args:
			script (str): The JavaScript to execute.
			*args (Any): Any arguments to pass to the script.

		Returns:
			Any: The value returned by the script's callback.
		"""
		
		...
	
	@abstractmethod
	def execute_cdp_cmd(self, cmd: str, cmd_args: Mapping[str, Any]) -> Mapping[str, Any]:
		"""
		Executes a Chrome DevTools Protocol command.

		Args:
			cmd (str): The CDP command to execute.
			cmd_args (Mapping[str, Any]): The arguments for the command.

		Returns:
			Mapping[str, Any]: The result of the command execution.
		"""
		
		...
	
	@abstractmethod
	def execute_script(self, script: str, *args: Any) -> Any:
		"""
		Synchronously executes JavaScript in the current window/frame.

		Args:
			script (str): The JavaScript to execute.
			*args (Any): Any arguments to pass to the script.

		Returns:
			Any: The value returned by the script.
		"""
		
		...
	
	@abstractmethod
	def fedcm(self) -> AbstractFedCM:
		"""
		Provides access to the FedCM (Federated Credential Management) interface.

		Returns:
			AbstractFedCM: An object for interacting with FedCM.
		"""
		
		...
	
	@abstractmethod
	def fedcm_dialog(
			self,
			timeout: int = 5,
			poll_frequency: float = 0.5,
			ignored_exceptions: Optional[Any] = None,
	) -> AbstractDialog:
		"""
		Waits for and returns a FedCM (Federated Credential Management) dialog.

		Args:
			timeout (int): The maximum time to wait for the dialog.
			poll_frequency (float): The frequency to check for the dialog's presence.
			ignored_exceptions (Optional[Any]): Exceptions to ignore during polling.

		Returns:
			AbstractDialog: The FedCM dialog object.
		"""
		
		...
	
	@abstractmethod
	def file_detector(self) -> Any:
		"""
		Gets the file detector for the current session.

		Returns:
			Any: The file detector instance.
		"""
		
		...
	
	@abstractmethod
	def find_element(self, by: By = By.ID, value: Optional[str] = None) -> AbstractWebElement:
		"""
		Finds an element within the current context using the given mechanism.

		Args:
			by (By): The strategy to use for finding the element (e.g., By.ID).
			value (Optional[str]): The value to search for.

		Returns:
			AbstractWebElement: The found WebElement.
		"""
		
		...
	
	@abstractmethod
	def find_elements(self, by: By = By.ID, value: Optional[str] = None) -> Sequence[AbstractWebElement]:
		"""
		Finds all elements within the current context using the given mechanism.

		Args:
			by (By): The strategy to use for finding elements (e.g., By.ID).
			value (Optional[str]): The value to search for.

		Returns:
			Sequence[AbstractWebElement]: A sequence of found WebElements.
		"""
		
		...
	
	@abstractmethod
	def forward(self) -> None:
		"""
		Goes one step forward in the browser history.
		"""
		
		...
	
	@abstractmethod
	def fullscreen_window(self) -> None:
		"""
		Invokes the window manager-specific "full screen" operation.
		"""
		
		...
	
	@abstractmethod
	def get(self, url: str) -> None:
		"""
		Loads a web page in the current browser session.

		Args:
			url (str): The URL to load.
		"""
		
		...
	
	@abstractmethod
	def get_cookie(self, name: str) -> Optional[Mapping[str, Any]]:
		"""
		Gets a single cookie with the given name.

		Args:
			name (str): The name of the cookie.

		Returns:
			Optional[Mapping[str, Any]]: The cookie dictionary, or None if not found.
		"""
		
		...
	
	@abstractmethod
	def get_cookies(self) -> Sequence[Mapping[str, Any]]:
		"""
		Returns all cookies for the current session.

		Returns:
			Sequence[Mapping[str, Any]]: A sequence of dictionaries, each representing a cookie.
		"""
		
		...
	
	@abstractmethod
	def get_credentials(self) -> Sequence[Credential]:
		"""
		Gets all credentials from the virtual authenticator.

		Returns:
			Sequence[Credential]: A sequence of Credential objects.
		"""
		
		...
	
	@abstractmethod
	def get_downloadable_files(self) -> Sequence[str]:
		"""
		Gets a list of files available for download from the browser.

		Returns:
			Sequence[str]: A sequence of downloadable file names.
		"""
		
		...
	
	@abstractmethod
	def get_pinned_scripts(self) -> Sequence[str]:
		"""
		Gets a list of all currently pinned scripts.

		Returns:
			Sequence[str]: A sequence of pinned scripts.
		"""
		
		...
	
	@abstractmethod
	def get_screenshot_as_base64(self) -> str:
		"""
		Gets a screenshot of the current window as a base64-encoded string.

		Returns:
			str: The base64-encoded screenshot image.
		"""
		
		...
	
	@abstractmethod
	def get_screenshot_as_file(self, filename: str) -> bool:
		"""
		Saves a screenshot to a file. This is an alias for save_screenshot.

		Args:
			filename (str): The full path of the file to save to.

		Returns:
			bool: True if successful, False otherwise.
		"""
		
		...
	
	@abstractmethod
	def get_screenshot_as_png(self) -> bytes:
		"""
		Gets a screenshot of the current window as binary data.

		Returns:
			bytes: The screenshot image in PNG format.
		"""
		
		...
	
	@abstractmethod
	def get_window_handle(self, window: Optional[Union[str, int]] = None) -> str:
		"""
		Gets the handle of a specific window by handle or index.

		Args:
			window (Optional[Union[str, int]]): The specific window handle (str) or index (int).
				If None, defaults to the current window.

		Returns:
			str: The window handle.

		Raises:
			IndexError: If the numeric window index is out of range.
			RuntimeError: If no window handles are available.
		"""
		
		...
	
	@abstractmethod
	def get_window_position(self, window_handle: str = "current") -> Position:
		"""
		Gets the position of a window.

		Args:
			window_handle (str): The handle of the window.

		Returns:
			Position: An object containing the 'x' and 'y' coordinates of the window.
		"""
		
		...
	
	@abstractmethod
	def get_window_rect(self) -> Rectangle:
		"""
		Gets the position and size of the current window.

		Returns:
			Rectangle: An object with 'x', 'y', 'width', and 'height' properties.
		"""
		
		...
	
	@abstractmethod
	def get_window_size(self, window_handle: str = "current") -> Size:
		"""
		Gets the size of a window.

		Args:
			window_handle (str): The handle of the window.

		Returns:
			Size: An object containing the 'width' and 'height' of the window.
		"""
		
		...
	
	@abstractmethod
	def hm_action_chain(
			self,
			duration: int = 250,
			devices: Optional[Sequence[DEVICES_TYPEHINT]] = None,
	) -> AbstractHumanLikeActionChains:
		"""
		Creates a new HumanLikeActionChains instance for building complex user interactions.

		Args:
			duration (int): The default duration for pointer actions in milliseconds.
			devices (Optional[Sequence[DEVICES_TYPEHINT]]): A sequence of input devices to use.

		Returns:
			AbstractHumanLikeActionChains: A new HumanLikeActionChains instance.
		"""
		
		...
	
	@abstractmethod
	def implicitly_wait(self, time_to_wait: float) -> None:
		"""
		Sets an implicit wait time.

		Args:
			time_to_wait (float): The amount of time to wait in seconds.
		"""
		
		...
	
	@abstractmethod
	def is_active(self) -> bool:
		"""
		Checks if the WebDriver instance is currently running.

		Returns:
			bool: True if the driver is active, False otherwise.
		"""
		
		...
	
	@abstractmethod
	def javascript(self) -> AbstractJSExecutor:
		"""
		Returns the JavaScript executor for this WebDriver instance.

		Returns:
			AbstractJSExecutor: The JavaScript executor instance.
		"""
		
		...
	
	@abstractmethod
	def maximize_window(self) -> None:
		"""
		Maximizes the current window.
		"""
		
		...
	
	@abstractmethod
	def minimize_window(self) -> None:
		"""
		Minimizes the current window.
		"""
		
		...
	
	@abstractmethod
	def mobile(self) -> AbstractMobile:
		"""
		Provides access to mobile-specific functionality.

		Returns:
			AbstractMobile: An object for mobile-specific interactions.
		"""
		
		...
	
	@abstractmethod
	def name(self) -> str:
		"""
		Returns the name of the underlying browser (e.g., 'chrome', 'firefox').

		Returns:
			str: The name of the browser.
		"""
		
		...
	
	@abstractmethod
	def network(self) -> AbstractNetwork:
		"""
		Provides access to the network interception and monitoring interface.

		Returns:
			AbstractNetwork: An object for interacting with network events.
		"""
		
		...
	
	@abstractmethod
	def orientation(self) -> Literal["LANDSCAPE", "PORTRAIT"]:
		"""
		Gets the current orientation of the browser.

		Returns:
			Literal["LANDSCAPE", "PORTRAIT"]: The current orientation.
		"""
		
		...
	
	@abstractmethod
	def page_source(self) -> str:
		"""
		Gets the source of the current page.

		Returns:
			str: The source code of the current page.
		"""
		
		...
	
	@abstractmethod
	def permissions(self) -> AbstractPermissions:
		"""
		Provides access to the permissions management interface.

		Returns:
			AbstractPermissions: An object for managing browser permissions.
		"""
		
		...
	
	@abstractmethod
	def pin_script(self, script: str, script_key: Optional[Any] = None) -> Any:
		"""
		Pins a script to the browser for faster execution.

		Args:
			script (str): The JavaScript to pin.
			script_key (Optional[Any]): An optional key to identify the script.

		Returns:
			Any: The key associated with the pinned script.
		"""
		
		...
	
	@abstractmethod
	def print_page(self, print_options: Optional[Any] = None) -> str:
		"""
		Prints the current page to a PDF.

		Args:
			print_options (Optional[Any]): Options for printing the page.

		Returns:
			str: A base64-encoded string of the PDF.
		"""
		
		...
	
	@abstractmethod
	def quit(self) -> None:
		"""
		Quits the driver and closes every associated window.
		"""
		
		...
	
	@abstractmethod
	def refresh(self) -> None:
		"""
		Refreshes the current page.
		"""
		
		...
	
	@abstractmethod
	async def remote_connect_driver(self, command_executor: Union[str, RemoteConnection]) -> None:
		"""
		Connects to a remote WebDriver server.

		Args:
			command_executor (Union[str, RemoteConnection]): The URL of the remote server or a RemoteConnection object.
		"""
		
		...
	
	@abstractmethod
	def remove_all_credentials(self) -> None:
		"""
		Removes all credentials from the virtual authenticator.
		"""
		
		...
	
	@abstractmethod
	def remove_credential(self, credential_id: Union[str, bytearray]) -> None:
		"""
		Removes a credential from the virtual authenticator.

		Args:
			credential_id (Union[str, bytearray]): The ID of the credential to remove.
		"""
		
		...
	
	@abstractmethod
	def remove_virtual_authenticator(self) -> None:
		"""
		Removes the currently active virtual authenticator.
		"""
		
		...
	
	@abstractmethod
	def reset_settings(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		"""
		Resets the WebDriver settings to a default or specified state.

		Args:
			flags (Optional[BrowserFlags]): Browser flags to reset to.
			window_rect (Optional[WindowRect]): Window dimensions to reset to.
		"""
		
		...
	
	@abstractmethod
	async def restart_webdriver(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		"""
		Closes the current WebDriver instance and starts a new one.

		Args:
			flags (Optional[BrowserFlags]): Browser flags for the new instance.
			window_rect (Optional[WindowRect]): Window dimensions for the new instance.
		"""
		
		...
	
	@abstractmethod
	def save_screenshot(self, filename: str) -> bool:
		"""
		Saves a screenshot of the current window to a file.

		Args:
			filename (str): The full path of the file to save the screenshot to.

		Returns:
			bool: True if successful, False otherwise.
		"""
		
		...
	
	@abstractmethod
	def script(self) -> AbstractScript:
		"""
		Provides access to the script execution interface.

		Returns:
			AbstractScript: An object for managing and executing scripts.
		"""
		
		...
	
	@abstractmethod
	async def set_driver_timeouts(
			self,
			page_load_timeout: float,
			implicit_wait_timeout: float,
			script_timeout: float,
	) -> None:
		"""
		Sets all main driver timeouts.

		Args:
			page_load_timeout (float): Timeout for page loads in seconds.
			implicit_wait_timeout (float): Timeout for implicit waits in seconds.
			script_timeout (float): Timeout for asynchronous scripts in seconds.
		"""
		
		...
	
	@abstractmethod
	def set_file_detector(self, detector: Any) -> None:
		"""
		Sets the file detector for the driver.

		Args:
			detector (Any): The file detector to use.
		"""
		
		...
	
	@abstractmethod
	def set_orientation(self, value: Literal["LANDSCAPE", "PORTRAIT"]) -> None:
		"""
		Sets the browser orientation.

		Args:
			value (Literal["LANDSCAPE", "PORTRAIT"]): The new orientation.
		"""
		
		...
	
	@abstractmethod
	def set_page_load_timeout(self, time_to_wait: float) -> None:
		"""
		Sets the timeout for a page load to complete.

		Args:
			time_to_wait (float): The timeout in seconds.
		"""
		
		...
	
	@abstractmethod
	def set_script_timeout(self, time_to_wait: float) -> None:
		"""
		Sets the timeout for asynchronous script execution.

		Args:
			time_to_wait (float): The timeout in seconds.
		"""
		
		...
	
	@abstractmethod
	def set_timeouts(self, timeouts: Any) -> None:
		"""
		Sets the timeouts for the driver.

		Args:
			timeouts (Any): The timeouts configuration object.
		"""
		
		...
	
	@abstractmethod
	def set_user_verified(self, verified: bool) -> None:
		"""
		Sets the user-verified status for a virtual authenticator.

		Args:
			verified (bool): The new verification status.
		"""
		
		...
	
	@abstractmethod
	def set_window_position(self, x: int, y: int, window_handle: str = "current") -> Position:
		"""
		Sets the position of a window.

		Args:
			x (int): The x-coordinate of the top-left corner.
			y (int): The y-coordinate of the top-left corner.
			window_handle (str): The handle of the window to move.

		Returns:
			Position: An object representing the new window position.
		"""
		
		...
	
	@abstractmethod
	def set_window_rect(
			self,
			x: Optional[int] = None,
			y: Optional[int] = None,
			width: Optional[int] = None,
			height: Optional[int] = None,
	) -> Rectangle:
		"""
		Sets the position and size of the current window.

		Args:
			x (Optional[int]): The x-coordinate of the top-left corner.
			y (Optional[int]): The y-coordinate of the top-left corner.
			width (Optional[int]): The new width of the window.
			height (Optional[int]): The new height of the window.

		Returns:
			Rectangle: An object representing the new window rectangle.
		"""
		
		...
	
	@abstractmethod
	def set_window_size(self, width: int, height: int, window_handle: str = "current") -> None:
		"""
		Sets the size of a window.

		Args:
			width (int): The new width in pixels.
			height (int): The new height in pixels.
			window_handle (str): The handle of the window to resize.
		"""
		
		...
	
	@abstractmethod
	def start_client(self) -> None:
		"""
		Starts the underlying webdriver client.
		"""
		
		...
	
	@abstractmethod
	def start_devtools(self) -> Tuple[Any, WebSocketConnection]:
		"""
		Starts a connection to the browser's developer tools.

		Returns:
			Tuple[Any, WebSocketConnection]: A tuple containing the DevTools session info and WebSocket connection.
		"""
		
		...
	
	@abstractmethod
	def start_session(self, capabilities: Mapping[str, Any]) -> None:
		"""
		Starts a new WebDriver session with the given capabilities.

		Args:
			capabilities (Mapping[str, Any]): A dictionary of desired capabilities.
		"""
		
		...
	
	@abstractmethod
	async def start_webdriver(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		"""
		Starts the WebDriver instance.

		Args:
			flags (Optional[BrowserFlags]): Browser flags to apply on startup.
			window_rect (Optional[WindowRect]): Initial window dimensions and position.
		"""
		
		...
	
	@abstractmethod
	def stop_client(self) -> None:
		"""
		Stops the underlying webdriver client.
		"""
		
		...
	
	@abstractmethod
	def storage(self) -> AbstractStorage:
		"""
		Provides access to the browser's storage mechanisms (e.g., cookies, local storage).

		Returns:
			AbstractStorage: An object for interacting with browser storage.
		"""
		
		...
	
	@abstractmethod
	def supports_fedcm(self) -> bool:
		"""
		Checks if the browser supports Federated Credential Management (FedCM).

		Returns:
			bool: True if FedCM is supported, False otherwise.
		"""
		
		...
	
	@abstractmethod
	def switch_to(self) -> AbstractSwitchTo:
		"""
		Returns an object to switch context to another frame, window, or alert.

		Returns:
			AbstractSwitchTo: The SwitchTo instance for context switching.
		"""
		
		...
	
	@abstractmethod
	def timeouts(self) -> Any:
		"""
		Gets the timeouts object for the current session.

		Returns:
			Any: An object for managing driver timeouts.
		"""
		
		...
	
	@abstractmethod
	def title(self) -> str:
		"""
		Gets the title of the current page.

		Returns:
			str: The title of the current page.
		"""
		
		...
	
	@abstractmethod
	def unpin(self, script_key: Any) -> None:
		"""
		Unpins a previously pinned script.

		Args:
			script_key (Any): The key of the script to unpin.
		"""
		
		...
	
	@abstractmethod
	def update_settings(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		"""
		Updates the WebDriver settings with new flags or window dimensions.

		Args:
			flags (Optional[BrowserFlags]): Browser flags to add or update.
			window_rect (Optional[WindowRect]): New window dimensions and position.
		"""
		
		...
	
	@abstractmethod
	async def update_times(
			self,
			temp_implicitly_wait: Optional[float] = None,
			temp_page_load_timeout: Optional[float] = None,
			temp_script_timeout: Optional[float] = None,
	) -> None:
		"""
		Temporarily updates driver timeouts for a single operation.

		Args:
			temp_implicitly_wait (Optional[float]): Temporary implicit wait timeout in seconds.
			temp_page_load_timeout (Optional[float]): Temporary page load timeout in seconds.
			temp_script_timeout (Optional[float]): Temporary script timeout in seconds.
		"""
		
		...
	
	@abstractmethod
	def virtual_authenticator_id(self) -> Optional[str]:
		"""
		Returns the ID of the currently active virtual authenticator.

		Returns:
			Optional[str]: The ID of the virtual authenticator, or None if not set.
		"""
		
		...
	
	@abstractmethod
	def webextension(self) -> AbstractWebExtension:
		"""
		Provides access to the web extension management interface.

		Returns:
			AbstractWebExtension: An object to manage browser extensions.
		"""
		
		...
	
	@abstractmethod
	def window_handles(self) -> Sequence[str]:
		"""
		Returns the handles of all windows within the current session.

		Returns:
			Sequence[str]: A sequence of window handles.
		"""
		
		...
