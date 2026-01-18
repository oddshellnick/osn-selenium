import warnings
from typing import Optional
from osn_selenium.types import WindowRect
from osn_selenium.flags.models.base import BrowserFlags
from osn_selenium.webdrivers.trio_threads.core.base import CoreBaseMixin
from osn_selenium.abstract.webdriver.core.settings import (
	AbstractCoreSettingsMixin
)


class CoreSettingsMixin(CoreBaseMixin, AbstractCoreSettingsMixin):
	"""
	Mixin for configuring and updating settings of the Core WebDriver.

	Provides methods to modify browser flags, window rectangles, and other
	configuration parameters either before startup or during a reset.
	"""
	
	async def reset_settings(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		if not self.is_active:
			if window_rect is None:
				window_rect = await self._sync_to_trio(WindowRect)
		
			if flags is not None:
				await self._sync_to_trio(self._webdriver_flags_manager.set_flags, flags=flags)
			else:
				await self._sync_to_trio(self._webdriver_flags_manager.clear_flags)
		
			self._window_rect = window_rect
		else:
			warnings.warn("Browser is already running.")
	
	async def update_settings(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		if flags is not None:
			await self._sync_to_trio(self._webdriver_flags_manager.update_flags, flags=flags)
		
		if window_rect is not None:
			self._window_rect = window_rect
