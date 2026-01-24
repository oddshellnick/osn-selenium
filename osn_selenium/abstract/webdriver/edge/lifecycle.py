from typing import Optional
from abc import abstractmethod
from osn_selenium.models import WindowRect
from osn_selenium._typehints import PATH_TYPEHINT
from osn_selenium.flags.models.edge import EdgeFlags
from osn_selenium.abstract.webdriver.blink.lifecycle import (
	AbstractBlinkLifecycleMixin
)


__all__ = ["AbstractEdgeLifecycleMixin"]


class AbstractEdgeLifecycleMixin(AbstractBlinkLifecycleMixin):
	"""
	Abstract mixin managing the lifecycle of a Edge WebDriver session.

	Defines the contract for creating, starting, and restarting the Edge browser
	and its associated WebDriver service.
	"""
	
	@abstractmethod
	def restart_webdriver(
			self,
			flags: Optional[EdgeFlags] = None,
			browser_exe: Optional[PATH_TYPEHINT] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	):
		"""
		Restarts the WebDriver and browser session gracefully.

		Performs a clean restart by first closing the existing WebDriver session and browser
		(using `close_webdriver`), and then initiating a new session (using `start_webdriver`)
		with potentially updated settings. If settings arguments are provided, they override
		the existing settings for the new session; otherwise, the current settings are used.

		Args:
			flags (Optional[EdgeFlags]): Override flags for the new session.
				If provided, these flags will be applied. If `None`, current settings are used.
			browser_exe (Optional[PATH_TYPEHINT]): Override browser executable for the new session.
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
		"""
		
		...
	
	@abstractmethod
	def start_webdriver(
			self,
			flags: Optional[EdgeFlags] = None,
			browser_exe: Optional[PATH_TYPEHINT] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	):
		"""
		Starts the WebDriver service and the browser session.

		Initializes and starts the WebDriver instance and the associated browser process.
		It first updates settings based on provided parameters (if the driver is not already running),
		checks if a browser process needs to be started, starts it if necessary using Popen,
		waits for it to become active, and then creates the WebDriver client instance (`self.driver`).

		Args:
			flags (Optional[EdgeFlags]): Override flags for this start.
				If provided, these flags will be applied. If `None`, current settings are used.
			browser_exe (Optional[PATH_TYPEHINT]): Override browser executable path for this start.
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
		"""
		
		...
