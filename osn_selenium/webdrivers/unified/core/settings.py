from typing import Optional
from osn_selenium.models import WindowRect
from osn_selenium.flags.models.base import BrowserFlags
from osn_selenium.webdrivers.unified.core.base import UnifiedCoreBaseMixin
from osn_selenium.exceptions.webdriver import (
	WebDriverAlreadyRunningError
)


__all__ = ["UnifiedCoreSettingsMixin"]


class UnifiedCoreSettingsMixin(UnifiedCoreBaseMixin):
	def _reset_settings_impl(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		if not self._is_active_impl:
			if window_rect is None:
				window_rect = WindowRect()
		
			if flags is not None:
				self._webdriver_flags_manager.set_flags(flags=flags)
			else:
				self._webdriver_flags_manager.clear_flags()
		
			self._window_rect = window_rect
		else:
			raise WebDriverAlreadyRunningError()
	
	def _update_settings_impl(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		if not self._is_active_impl:
			if flags is not None:
				self._webdriver_flags_manager.update_flags(flags=flags)
		
			if window_rect is not None:
				self._window_rect = window_rect
		else:
			raise WebDriverAlreadyRunningError()
