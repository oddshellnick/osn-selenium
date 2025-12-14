import pathlib
from abc import abstractmethod
from typing import Optional, Union
from osn_selenium.types import WindowRect
from osn_selenium.flags.models.blink import BlinkFlags
from osn_selenium.abstract.webdriver.core.lifecycle import (
	AbstractCoreLifecycleMixin
)


class AbstractBlinkLifecycleMixin(AbstractCoreLifecycleMixin):
	"""
	Abstract mixin defining the lifecycle management interface for Blink-based WebDrivers.

	Handles creation, startup, shutdown, and restarting of the WebDriver instance
	and the associated browser process.
	"""
	
	@abstractmethod
	def _create_driver(self) -> None:
		"""
		Abstract method to create a WebDriver instance. Must be implemented in child classes.

		This method is intended to be overridden in subclasses to provide browser-specific
		WebDriver instantiation logic (e.g., creating ChromeDriver, FirefoxDriver, etc.).

		Raises:
			NotImplementedError: If the method is not implemented in a subclass.
		"""
		
		...
	
	@abstractmethod
	async def close_webdriver(self) -> None:
		"""
		Closes the WebDriver connection and terminates the browser process.
		"""
		
		...
	
	@abstractmethod
	async def restart_webdriver(
			self,
			flags: Optional[BlinkFlags] = None,
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		"""
		Restarts the WebDriver and browser, applying new settings if provided.

		Args:
			flags (Optional[BlinkFlags]): Configuration flags for the new session.
			browser_exe (Optional[Union[str, pathlib.Path]]): Path to the browser executable.
			browser_name_in_system (Optional[str]): Name of the browser in the system.
			use_browser_exe (Optional[bool]): Whether to manage the browser executable process.
			start_page_url (Optional[str]): URL to open after restart.
			window_rect (Optional[WindowRect]): Initial window dimensions.
		"""
		
		...
	
	@abstractmethod
	async def start_webdriver(
			self,
			flags: Optional[BlinkFlags] = None,
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		"""
		Starts the WebDriver and the browser instance.

		Args:
			flags (Optional[BlinkFlags]): Configuration flags for the browser.
			browser_exe (Optional[Union[str, pathlib.Path]]): Path to the browser executable.
			browser_name_in_system (Optional[str]): Name of the browser in the OS registry/system.
			use_browser_exe (Optional[bool]): Whether to manage the browser executable process.
			start_page_url (Optional[str]): URL to open immediately upon start.
			window_rect (Optional[WindowRect]): Initial dimensions and position of the window.
		"""
		
		...
