from typing import Optional
from osn_selenium.models import WindowRect
from osn_selenium.trio_threads_mixin import TrioThreadMixin
from osn_selenium.flags.models.base import BrowserFlags
from osn_selenium.webdrivers.unified.core.settings import (
	UnifiedCoreSettingsMixin
)
from osn_selenium.abstract.webdriver.core.settings import (
	AbstractCoreSettingsMixin
)


__all__ = ["CoreSettingsMixin"]


class CoreSettingsMixin(UnifiedCoreSettingsMixin, TrioThreadMixin, AbstractCoreSettingsMixin):
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
		await self.sync_to_trio(sync_function=self._reset_settings_impl)(flags=flags, window_rect=window_rect)
	
	async def update_settings(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		await self.sync_to_trio(sync_function=self._update_settings_impl)(flags=flags, window_rect=window_rect)
