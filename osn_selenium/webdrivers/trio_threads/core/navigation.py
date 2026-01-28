from osn_selenium.trio_threads_mixin import TrioThreadMixin
from osn_selenium.webdrivers.unified.core.navigation import (
	UnifiedCoreNavigationMixin
)
from osn_selenium.abstract.webdriver.core.navigation import (
	AbstractCoreNavigationMixin
)


__all__ = ["CoreNavigationMixin"]


class CoreNavigationMixin(
		UnifiedCoreNavigationMixin,
		TrioThreadMixin,
		AbstractCoreNavigationMixin
):
	"""
	Mixin controlling browser navigation for Core WebDrivers.

	Includes standard navigation commands such as visiting URLs, history
	traversal (back/forward), and page refreshing.
	"""
	
	async def back(self) -> None:
		await self.sync_to_trio(sync_function=self._back_impl)()
	
	async def current_url(self) -> str:
		return await self.sync_to_trio(sync_function=self._current_url_impl)()
	
	async def forward(self) -> None:
		await self.sync_to_trio(sync_function=self._forward_impl)()
	
	async def get(self, url: str) -> None:
		await self.sync_to_trio(sync_function=self._get_impl)(url=url)
	
	async def refresh(self) -> None:
		await self.sync_to_trio(sync_function=self._refresh_impl)()
	
	async def title(self) -> str:
		return await self.sync_to_trio(sync_function=self._title_impl)()
