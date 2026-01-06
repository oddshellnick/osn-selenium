import warnings
from typing import Optional
from osn_selenium.types import WindowRect
from osn_selenium.flags.models.base import BrowserFlags
from osn_selenium.webdrivers.sync.base.base import BaseMixin
from osn_selenium.abstract.webdriver.base.settings import (
	AbstractSettingsMixin
)


class SettingsMixin(BaseMixin, AbstractSettingsMixin):
	def reset_settings(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		if not self.is_active:
			if window_rect is None:
				window_rect = WindowRect()
		
			if flags is not None:
				self._webdriver_flags_manager.set_flags(flags=flags)
			else:
				self._webdriver_flags_manager.clear_flags()
		
			self._window_rect = window_rect
		else:
			warnings.warn("Browser is already running.")
	
	def update_settings(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		if flags is not None:
			self._webdriver_flags_manager.update_flags(flags=flags)
		
		if window_rect is not None:
			self._window_rect = window_rect
