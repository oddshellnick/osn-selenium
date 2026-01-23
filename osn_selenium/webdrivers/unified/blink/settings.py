from typing import Optional
from osn_selenium.models import WindowRect
from osn_selenium._typehints import PATH_TYPEHINT
from osn_selenium.flags.models.blink import BlinkFlags
from osn_selenium.exceptions.webdriver import (
	WebDriverAlreadyRunningError
)
from osn_selenium.webdrivers.unified.blink.base import (
	UnifiedBlinkBaseMixin
)


__all__ = ["UnifiedBlinkSettingsMixin"]


class UnifiedBlinkSettingsMixin(UnifiedBlinkBaseMixin):
	def _reset_settings_impl(
			self,
			flags: Optional[BlinkFlags] = None,
			browser_exe: Optional[PATH_TYPEHINT] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: str = "",
			window_rect: Optional[WindowRect] = None,
	) -> None:
		if not self._is_active:
			if flags is not None:
				self._webdriver_flags_manager.set_flags(flags)
			else:
				self._webdriver_flags_manager.clear_flags()
		
			self._webdriver_flags_manager.browser_exe = browser_exe
			self._webdriver_flags_manager.start_page_url = start_page_url
			self._window_rect = window_rect
		
			if use_browser_exe is not None and browser_name_in_system is not None:
				self._detect_browser_exe_impl(
						browser_name_in_system=browser_name_in_system,
						use_browser_exe=use_browser_exe
				)
		
			if self._browser_exe_impl is not None and (
					self._debugging_port_impl is not None
					or self._debugging_ip_impl is not None
			):
				self._set_debugging_port_impl(
						self._find_debugging_port_impl(self._debugging_port_impl),
						self._debugging_ip_impl
				)
		else:
			raise WebDriverAlreadyRunningError()
	
	def _update_settings_impl(
			self,
			flags: Optional[BlinkFlags] = None,
			browser_exe: Optional[PATH_TYPEHINT] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		if not self._is_active:
			if flags is not None:
				self._webdriver_flags_manager.update_flags(flags)
		
			if browser_exe is not None:
				self._webdriver_flags_manager.browser_exe = browser_exe
		
			if start_page_url is not None:
				self._webdriver_flags_manager.start_page_url = start_page_url
		
			if window_rect is not None:
				self._window_rect = window_rect
		
			if use_browser_exe is not None and browser_name_in_system is not None:
				self._detect_browser_exe_impl(
						browser_name_in_system=browser_name_in_system,
						use_browser_exe=use_browser_exe
				)
		
			self._set_debugging_port_impl(
					self._find_debugging_port_impl(self._debugging_port_impl),
					self._debugging_ip_impl
			)
		else:
			raise WebDriverAlreadyRunningError()
