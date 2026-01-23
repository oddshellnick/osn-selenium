from typing import Optional
from abc import abstractmethod
from osn_selenium.models import WindowRect
from osn_selenium._typehints import PATH_TYPEHINT
from osn_selenium.flags.models.edge import EdgeFlags
from osn_selenium.abstract.webdriver.blink.settings import (
	AbstractBlinkSettingsMixin
)


__all__ = ["AbstractEdgeSettingsMixin"]


class AbstractEdgeSettingsMixin(AbstractBlinkSettingsMixin):
	"""
	Abstract mixin for managing Edge browser settings.

	Provides methods to update or reset configuration parameters such as flags,
	executable paths, and window dimensions for the Edge WebDriver.
	"""
	
	@abstractmethod
	def reset_settings(
			self,
			flags: Optional[EdgeFlags] = None,
			browser_exe: Optional[PATH_TYPEHINT] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: str = "",
			window_rect: Optional[WindowRect] = None,
	):
		"""
		Resets various configurable browser settings to their specified or default values.

		This method allows for reconfiguring the WebDriver's operational parameters,
		such as browser flags, executable path, start URL, window dimensions, and
		concurrency limits. It is crucial that the browser session is *not* active
		when this method is called; otherwise, a warning will be issued, and no changes
		will be applied.

		Args:
			flags (Optional[EdgeFlags]): New browser flags to apply.
				If provided, existing flags are cleared and replaced with these.
				If `None`, all custom flags are cleared, and the browser will start with default flags.
			browser_exe (Optional[PATH_TYPEHINT]): The explicit path to the browser executable.
				If provided, this path will be used. If `None`, the executable path managed by the
				flags manager will be cleared, and then potentially re-detected based on
				`use_browser_exe` and `browser_name_in_system`.
			browser_name_in_system (Optional[str]): The common name of the browser (e.g., "Edge").
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
		"""
		
		...
	
	@abstractmethod
	def update_settings(
			self,
			flags: Optional[EdgeFlags] = None,
			browser_exe: Optional[PATH_TYPEHINT] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	):
		"""
		Updates various browser settings selectively without resetting others.

		This method allows for dynamic updating of browser settings. Only the settings
		for which a non-None value is provided will be updated. Settings passed as `None`
		will retain their current values. This method can be called whether the browser
		is active or not, but some changes might only take effect after the browser is
		restarted.

		Args:
			flags (Optional[EdgeFlags]): New browser flags to update.
				If provided, these flags will be merged with or overwrite existing flags
				within the flags manager. If `None`, existing flags remain unchanged.
			browser_exe (Optional[PATH_TYPEHINT]): The new path to the browser executable.
				If provided, this path will be set in the flags manager. If `None`, the
				current browser executable path remains unchanged.
			browser_name_in_system (Optional[str]): The common name of the browser (e.g., "Edge").
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
		"""
		
		...
