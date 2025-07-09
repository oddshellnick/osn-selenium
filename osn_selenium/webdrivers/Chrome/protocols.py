import pathlib
from selenium import webdriver
from osn_selenium.types import WindowRect
from osn_selenium.webdrivers.types import _any_flags_mapping
from osn_selenium.webdrivers.Chrome.flags import ChromeFlagsManager
from typing import (
	Optional,
	Protocol,
	TYPE_CHECKING,
	Union,
	runtime_checkable
)
from osn_selenium.webdrivers.Blink.protocols import (
	TrioBlinkWebDriverWrapperProtocol
)


if TYPE_CHECKING:
	from osn_selenium.webdrivers.Chrome.webdriver import ChromeWebDriver, ChromeFlags


@runtime_checkable
class TrioChromeWebDriverWrapperProtocol(TrioBlinkWebDriverWrapperProtocol, Protocol):
	"""
	Wraps ChromeWebDriver methods for asynchronous execution using Trio.

	This class acts as a proxy to a `BrowserWebDriver` instance. It intercepts
	method calls and executes them in a separate thread using `trio.to_thread.run_sync`,
	allowing synchronous WebDriver operations to be called from asynchronous Trio code
	without blocking the event loop. Properties and non-callable attributes are accessed directly.

	Attributes:
		_webdriver (BrowserWebDriver): The underlying synchronous BrowserWebDriver instance.
		_excluding_functions (list[str]): A list of attribute names on the wrapped object
											  that should *not* be accessible through this wrapper,
											  typically because they are irrelevant or dangerous
											  in an async context handled by the wrapper.
	"""
	
	_webdriver: "ChromeWebDriver"
	_webdriver_flags_manager: "ChromeFlagsManager"
	_driver: Optional[webdriver.Chrome]
	
	@property
	def driver(self) -> Optional[webdriver.Chrome]:
		"""
		Gets the underlying Selenium WebDriver instance associated with this object.

		This property provides direct access to the WebDriver object (e.g., Chrome)
		that is being controlled, allowing for direct Selenium operations if needed.

		Returns:
			Optional[webdriver.Chrome]:
				The active WebDriver instance, or None if no driver is currently set or active.
		"""
		
		...
	
	def reset_settings(
			self,
			flags: Optional[Union["ChromeFlags", _any_flags_mapping]] = None,
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
			flags (Optional[Union[ChromeFlags, Mapping[str, Any]]]): New browser flags to apply.
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
		
		...
	
	def restart_webdriver(
			self,
			flags: Optional[Union["ChromeFlags", _any_flags_mapping]] = None,
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
			flags (Optional[Union[ChromeFlags, Mapping[str, Any]]]): Override flags for the new session.
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
		
		...
	
	def start_webdriver(
			self,
			flags: Optional[Union["ChromeFlags", _any_flags_mapping]] = None,
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
			flags (Optional[Union[ChromeFlags, Mapping[str, Any]]]): Override flags for this start.
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
		
		...
	
	def update_settings(
			self,
			flags: Optional[Union["ChromeFlags", _any_flags_mapping]] = None,
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
			flags (Optional[Union[ChromeFlags, Mapping[str, Any]]]): New browser flags to update.
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
		
		...
