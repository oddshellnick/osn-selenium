from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.webdrivers.trio_threads.core.base import CoreBaseMixin
from osn_selenium.abstract.webdriver.core.navigation import (
	AbstractCoreNavigationMixin
)


class CoreNavigationMixin(CoreBaseMixin, AbstractCoreNavigationMixin):
	@requires_driver
	async def back(self) -> None:
		await self._wrap_to_trio(self.driver.back)
	
	@requires_driver
	async def current_url(self) -> str:
		return await self._wrap_to_trio(lambda: self.driver.current_url)
	
	@requires_driver
	async def forward(self) -> None:
		await self._wrap_to_trio(self.driver.forward)
	
	@requires_driver
	async def get(self, url: str) -> None:
		await self._wrap_to_trio(self.driver.get, url=url)
	
	@requires_driver
	async def refresh(self) -> None:
		await self._wrap_to_trio(self.driver.refresh)
	
	@requires_driver
	async def title(self) -> str:
		return await self._wrap_to_trio(lambda: self.driver.title)
