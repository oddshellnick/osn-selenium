import pathlib
from selenium import webdriver
from osn_selenium.types import WindowRect
from selenium.webdriver.chrome.service import Service
from typing import (
	Optional,
	Type,
	Union,
	cast
)
from osn_selenium.dev_tools.manager import DevToolsSettings
from osn_selenium.webdrivers.types import _any_flags_mapping
from osn_selenium.captcha_workers import (
	CaptchaWorkerSettings
)
from osn_selenium.webdrivers.Blink.webdriver import BlinkWebDriver
from osn_selenium.webdrivers.Edge.flags import (
	EdgeFlags,
	EdgeFlagsManager
)
from osn_selenium.webdrivers.Edge.protocols import (
	TrioEdgeWebDriverWrapperProtocol
)
from osn_selenium.webdrivers.BaseDriver.trio_wrapper import (
	TrioBrowserWebDriverWrapper
)


class EdgeWebDriver(BlinkWebDriver):
	"""
	Manages a Edge Browser session using Selenium WebDriver.

	This class specializes BlinkWebDriver for Edge Browser. It sets up and manages
	the lifecycle of a Edge Browser instance controlled by Selenium WebDriver,
	including starting the browser with specific options, handling sessions, and managing browser processes.
	Edge Browser is based on Chromium, so it uses EdgeOptions and EdgeDriver.

	Attributes:
		_window_rect (Optional[WindowRect]): The window size and position settings.
		_js_scripts (dict[str, str]): A dictionary of pre-loaded JavaScript scripts.
		_webdriver_path (str): The file path to the WebDriver executable.
		_webdriver_flags_manager (EdgeFlagsManager): The manager for browser flags and options.
		_driver (Optional[webdriver.Edge]): The active Selenium WebDriver instance.
		_base_implicitly_wait (int): The default implicit wait time in seconds.
		_base_page_load_timeout (int): The default page load timeout in seconds.
		_base_script_timeout (int): The default script timeout in seconds.
		_captcha_workers (list[CaptchaWorkerSettings]): A list of configured captcha worker settings.
		_is_active (bool): A flag indicating if the browser process is active.
		trio_capacity_limiter (trio.CapacityLimiter): A capacity limiter for controlling concurrent async operations.
		dev_tools (DevTools): An interface for interacting with the browser's DevTools protocol.
		_console_encoding (str): The encoding of the system console.
		_ip_pattern (re.Pattern): A compiled regex pattern to match IP addresses and ports.
	"""
	
	def __init__(
			self,
			webdriver_path: str,
			flags_manager_type: Type[EdgeFlagsManager] = EdgeFlagsManager,
			use_browser_exe: bool = True,
			browser_name_in_system: str = "Microsoft Edge",
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			flags: Optional[EdgeFlags] = None,
			start_page_url: str = "https://www.chrome.com",
			implicitly_wait: int = 5,
			page_load_timeout: int = 5,
			script_timeout: int = 5,
			window_rect: Optional[WindowRect] = None,
			trio_tokens_limit: Union[int, float] = 40,
			captcha_workers: Optional[list[CaptchaWorkerSettings]] = None,
			devtools_settings: Optional[DevToolsSettings] = None,
	):
		"""
		Initializes a EdgeWebDriver instance.

		This constructor prepares the Edge Browser for automation by setting up
		its executable path, WebDriver path, browser flags, and other operational
		settings. It leverages the `BlinkWebDriver` base class for common Chromium-based
		browser functionalities.

		Args:
			webdriver_path (str): The file path to the EdgeDriver executable.
			flags_manager_type (Type[EdgeFlagsManager]): The type of flags manager
				to use for configuring Edge Browser-specific command-line arguments.
				Defaults to `EdgeFlagsManager`.
			use_browser_exe (bool): If True, the browser executable path will be
				automatically determined based on `browser_name_in_system` if `browser_exe`
				is not explicitly provided. If False, `browser_exe` must be None.
				Defaults to True.
			browser_name_in_system (str): The common name of the Edge Browser
				executable in the system (e.g., "Microsoft Edge"). Used to auto-detect `browser_exe`.
				Defaults to "Microsoft Edge".
			browser_exe (Optional[Union[str, pathlib.Path]]): The explicit path to the
				Edge Browser executable. If `use_browser_exe` is True and this is None,
				it will attempt to find the browser automatically. If `use_browser_exe`
				is False, this must be None.
			flags (Optional[EdgeFlags]): An object containing specific flags or options
				to pass to the Edge Browser process.
			start_page_url (str): The URL to load when the browser session starts.
				Defaults to "https://www.chrome.com".
			implicitly_wait (int): The default implicit wait time in seconds for the WebDriver.
				Defaults to 5 seconds.
			page_load_timeout (int): The default timeout in seconds for page loading.
				Defaults to 5 seconds.
			script_timeout (int): The default timeout in seconds for asynchronous JavaScript execution.
				Defaults to 5 seconds.
			window_rect (Optional[WindowRect]): An object specifying the initial window
				position and size.
			trio_tokens_limit (Union[int, float]): The maximum number of concurrent
				asynchronous operations allowed by the Trio capacity limiter. Defaults to 40.
			captcha_workers (Optional[Sequence[CaptchaWorkerSettings]]): A sequence of
				settings for captcha detection and solving functions.
			devtools_settings (Optional[DevToolsSettings]): Settings for configuring the
				Edge DevTools Protocol (CDP) interface.
		"""
		
		super().__init__(
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				webdriver_path=webdriver_path,
				flags_manager_type=flags_manager_type,
				flags=flags,
				start_page_url=start_page_url,
				implicitly_wait=implicitly_wait,
				page_load_timeout=page_load_timeout,
				script_timeout=script_timeout,
				window_rect=window_rect,
				trio_tokens_limit=trio_tokens_limit,
				captcha_workers=captcha_workers,
				devtools_settings=devtools_settings,
		)
	
	def _create_driver(self):
		"""
		Creates the Edge webdriver instance.

		This method initializes and sets up the Selenium Edge WebDriver using EdgeDriver with configured options and service.
		It also sets the window position, size, implicit wait time, and page load timeout.
		"""
		
		webdriver_options = self._webdriver_flags_manager.options
		webdriver_service = Service(
				executable_path=self._webdriver_path,
				port=self.debugging_port if self.browser_exe is None else 0,
				service_args=self._webdriver_flags_manager.start_args
				if self.browser_exe is None
				else None
		)
		
		self._driver = webdriver.Edge(options=webdriver_options, service=webdriver_service)
		
		if self._window_rect is not None:
			self.set_window_rect(self._window_rect)
		
		self.set_driver_timeouts(
				page_load_timeout=self._base_page_load_timeout,
				implicit_wait_timeout=self._base_implicitly_wait,
				script_timeout=self._base_implicitly_wait,
		)
	
	@property
	def driver(self) -> Optional[webdriver.Edge]:
		"""
		Gets the underlying Selenium WebDriver instance associated with this object.

		This property provides direct access to the WebDriver object (e.g., Edge)
		that is being controlled, allowing for direct Selenium operations if needed.

		Returns:
			Optional[webdriver.Edge]:
				The active WebDriver instance, or None if no driver is currently set or active.
		"""
		
		return super().driver
	
	def reset_settings(
			self,
			flags: Optional[Union[EdgeFlags, _any_flags_mapping]] = None,
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: str = "",
			window_rect: Optional[WindowRect] = None,
			trio_tokens_limit: Union[int, float] = 40,
	):
		"""
		Resets various configurable browser settings to their specified or default values.

		This method allows for reconfiguring the WebDriver's operational parameters,
		such as browser flags, executable path, start URL, window dimensions, and
		concurrency limits. It is crucial that the browser session is *not* active
		when this method is called; otherwise, a warning will be issued, and no changes
		will be applied.

		Args:
			flags (Optional[Union[EdgeFlags, Mapping[str, Any]]]): New browser flags to apply.
				If provided, existing flags are cleared and replaced with these.
				If `None`, all custom flags are cleared, and the browser will start with default flags.
			browser_exe (Optional[Union[str, pathlib.Path]]): The explicit path to the browser executable.
				If provided, this path will be used. If `None`, the executable path managed by the
				flags manager will be cleared, and then potentially re-detected based on
				`use_browser_exe` and `browser_name_in_system`.
			browser_name_in_system (Optional[str]): The common name of the browser (e.g., "Chrome", "Edge").
				Used in conjunction with `use_browser_exe` to automatically detect the browser executable path.
				This parameter only takes effect if `use_browser_exe` is explicitly `True` or `False`.
				If `None`, no automatic detection based on name will occur through this method call.
			use_browser_exe (Optional[bool]): Controls the automatic detection of the browser executable.
				If `True` (and `browser_name_in_system` is provided), the browser executable path
				will be automatically detected if `browser_exe` is `None`.
				If `False` (and `browser_name_in_system` is provided), any existing `browser_exe`
				path in the flags manager will be cleared.
				If `None`, the current `use_browser_exe` state is maintained for the `_detect_browser_exe` logic.
			start_page_url (str): The URL that the browser will attempt to navigate to
				immediately after starting. Defaults to an empty string.
			window_rect (Optional[WindowRect]): The initial window size and position settings.
				If `None`, it defaults to a new `WindowRect()` instance, effectively resetting
				to the browser's default window behavior.
			trio_tokens_limit (Union[int, float]): The maximum number of concurrent synchronous
				WebDriver operations allowed by the Trio capacity limiter. Defaults to 40.
		"""
		
		super().reset_settings(
				flags=flags,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				start_page_url=start_page_url,
				window_rect=window_rect,
				trio_tokens_limit=trio_tokens_limit,
		)
	
	def restart_webdriver(
			self,
			flags: Optional[Union[EdgeFlags, _any_flags_mapping]] = None,
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
			trio_tokens_limit: Optional[Union[int, float]] = None,
	):
		"""
		Restarts the WebDriver and browser session gracefully.

		Performs a clean restart by first closing the existing WebDriver session and browser
		(using `close_webdriver`), and then initiating a new session (using `start_webdriver`)
		with potentially updated settings. If settings arguments are provided, they override
		the existing settings for the new session; otherwise, the current settings are used.

		Args:
			flags (Optional[Union[EdgeFlags, Mapping[str, Any]]]): Override flags for the new session.
				If provided, these flags will be applied. If `None`, current settings are used.
			browser_exe (Optional[Union[str, pathlib.Path]]): Override browser executable for the new session.
				If provided, this path will be used. If `None`, current settings are used.
			browser_name_in_system (Optional[str]): Override browser name for auto-detection for the new session.
				Only takes effect if `use_browser_exe` is also provided. If `None`, current settings are used.
			use_browser_exe (Optional[bool]): Override auto-detection behavior for the new session.
				If provided, this boolean determines if the browser executable is auto-detected.
				If `None`, current settings are used.
			start_page_url (Optional[str]): Override start page URL for the new session.
				If provided, this URL will be used. If `None`, current setting is used.
			window_rect (Optional[WindowRect]): Override window rectangle for the new session.
				If provided, these dimensions will be used. If `None`, current settings are used.
			trio_tokens_limit (Optional[Union[int, float]]): Override Trio token limit for the new session.
				If provided, this limit will be used. If `None`, current setting is used.
		"""
		
		super().restart_webdriver(
				flags=flags,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				start_page_url=start_page_url,
				window_rect=window_rect,
				trio_tokens_limit=trio_tokens_limit,
		)
	
	def start_webdriver(
			self,
			flags: Optional[Union[EdgeFlags, _any_flags_mapping]] = None,
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
			trio_tokens_limit: Optional[Union[int, float]] = None,
	):
		"""
		Starts the WebDriver service and the browser session.

		Initializes and starts the WebDriver instance and the associated browser process.
		It first updates settings based on provided parameters (if the driver is not already running),
		checks if a browser process needs to be started, starts it if necessary using Popen,
		waits for it to become active, and then creates the WebDriver client instance (`self.driver`).

		Args:
			flags (Optional[Union[EdgeFlags, Mapping[str, Any]]]): Override flags for this start.
				If provided, these flags will be applied. If `None`, current settings are used.
			browser_exe (Optional[Union[str, pathlib.Path]]): Override browser executable path for this start.
				If provided, this path will be used. If `None`, current settings are used.
			browser_name_in_system (Optional[str]): Override browser name for auto-detection for this start.
				Only takes effect if `use_browser_exe` is also provided. If `None`, current settings are used.
			use_browser_exe (Optional[bool]): Override auto-detection behavior for this start.
				If provided, this boolean determines if the browser executable is auto-detected.
				If `None`, current settings are used.
			start_page_url (Optional[str]): Override start page URL for this start.
				If provided, this URL will be used. If `None`, current setting is used.
			window_rect (Optional[WindowRect]): Override window rectangle for this start.
				If provided, these dimensions will be used. If `None`, current settings are used.
			trio_tokens_limit (Optional[Union[int, float]]): Override Trio token limit for this start.
				If provided, this limit will be used. If `None`, current setting is used.
		"""
		
		super().start_webdriver(
				flags=flags,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				start_page_url=start_page_url,
				window_rect=window_rect,
				trio_tokens_limit=trio_tokens_limit,
		)
	
	def to_wrapper(self) -> TrioEdgeWebDriverWrapperProtocol:
		"""
		Creates a TrioBrowserWebDriverWrapper instance for asynchronous operations with Trio.

		Wraps the ...WebDriver instance in a TrioBrowserWebDriverWrapper, which allows for running WebDriver
		commands in a non-blocking manner within a Trio asynchronous context. This is essential for
		integrating Selenium WebDriver with asynchronous frameworks like Trio.

		Returns:
			TrioEdgeWebDriverWrapperProtocol: A TrioBrowserWebDriverWrapper instance wrapping this BrowserWebDriver.
		"""
		
		return cast(
				TrioEdgeWebDriverWrapperProtocol,
				TrioBrowserWebDriverWrapper(_webdriver=self)
		)
	
	def update_settings(
			self,
			flags: Optional[Union[EdgeFlags, _any_flags_mapping]] = None,
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
			trio_tokens_limit: Optional[Union[int, float]] = None,
	):
		"""
		Updates various browser settings selectively without resetting others.

		This method allows for dynamic updating of browser settings. Only the settings
		for which a non-None value is provided will be updated. Settings passed as `None`
		will retain their current values. This method can be called whether the browser
		is active or not, but some changes might only take effect after the browser is
		restarted.

		Args:
			flags (Optional[Union[EdgeFlags, Mapping[str, Any]]]): New browser flags to update.
				If provided, these flags will be merged with or overwrite existing flags
				within the flags manager. If `None`, existing flags remain unchanged.
			browser_exe (Optional[Union[str, pathlib.Path]]): The new path to the browser executable.
				If provided, this path will be set in the flags manager. If `None`, the
				current browser executable path remains unchanged.
			browser_name_in_system (Optional[str]): The common name of the browser (e.g., "Chrome", "Edge").
				Used in conjunction with `use_browser_exe` to automatically detect the browser executable path.
				This parameter only takes effect if `use_browser_exe` is explicitly provided.
				If `None`, no automatic detection based on name will occur through this method call.
			use_browser_exe (Optional[bool]): Controls the automatic detection of the browser executable.
				If `True` (and `browser_name_in_system` is provided), the browser executable path
				will be automatically detected if `browser_exe` is `None`.
				If `False` (and `browser_name_in_system` is provided), any existing `browser_exe`
				path in the flags manager will be cleared.
				If `None`, the current `use_browser_exe` state is maintained for the `_detect_browser_exe` logic.
			start_page_url (Optional[str]): The new URL that the browser will attempt to navigate to
				immediately after starting. If `None`, the current start page URL remains unchanged.
			window_rect (Optional[WindowRect]): The new window size and position settings.
				If `None`, the current window rectangle settings remain unchanged.
			trio_tokens_limit (Optional[Union[int, float]]): The new maximum number of concurrent
				asynchronous operations allowed by the Trio capacity limiter. If `None`, the
				current limit remains unchanged.
		"""
		
		super().update_settings(
				flags=flags,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				start_page_url=start_page_url,
				window_rect=window_rect,
				trio_tokens_limit=trio_tokens_limit,
		)
