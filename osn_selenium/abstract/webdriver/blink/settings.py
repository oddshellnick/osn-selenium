from typing import Optional
from abc import abstractmethod
from osn_selenium.models import WindowRect
from osn_selenium._typehints import PATH_TYPEHINT
from osn_selenium.flags.models.blink import BlinkFlags
from osn_selenium.abstract.webdriver.core.settings import (
	AbstractCoreSettingsMixin
)


__all__ = ["AbstractBlinkSettingsMixin"]


class AbstractBlinkSettingsMixin(AbstractCoreSettingsMixin):
	"""
	Abstract mixin defining the interface for managing browser settings and configuration.

	Provides methods to update or reset the browser's runtime configuration, including
	flags, executable paths, and window geometry.
	"""
	
	@abstractmethod
	def reset_settings(
			self,
			flags: Optional[BlinkFlags] = None,
			browser_exe: Optional[PATH_TYPEHINT] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: str = "",
			window_rect: Optional[WindowRect] = None,
	) -> None:
		"""
		Resets the browser settings to their default or specified values.

		Args:
			flags (Optional[BlinkFlags]): Flags to set (overwriting previous configuration).
			browser_exe (Optional[PATH_TYPEHINT]): Path to the browser executable.
			browser_name_in_system (Optional[str]): System name for the browser.
			use_browser_exe (Optional[bool]): Flag to enable/disable executable management.
			start_page_url (str): The start page URL (defaults to empty string).
			window_rect (Optional[WindowRect]): Window dimensions.
		"""
		
		...
	
	@abstractmethod
	def update_settings(
			self,
			flags: Optional[BlinkFlags] = None,
			browser_exe: Optional[PATH_TYPEHINT] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		"""
		Updates the browser settings without performing a full reset.

		Args:
			flags (Optional[BlinkFlags]): New flags to merge or apply.
			browser_exe (Optional[PATH_TYPEHINT]): New path to the browser executable.
			browser_name_in_system (Optional[str]): New system name for the browser.
			use_browser_exe (Optional[bool]): Flag to enable/disable executable management.
			start_page_url (Optional[str]): New start page URL.
			window_rect (Optional[WindowRect]): New window dimensions.
		"""
		
		...
