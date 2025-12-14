from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.webdrivers.sync.core.base import CoreBaseMixin
from osn_selenium.abstract.webdriver.core.navigation import (
	AbstractCoreNavigationMixin
)


class CoreNavigationMixin(CoreBaseMixin, AbstractCoreNavigationMixin):
	"""
	Mixin controlling browser navigation for Core WebDrivers.

	Includes standard navigation commands such as visiting URLs, history
	traversal (back/forward), and page refreshing.
	"""
	
	@requires_driver
	def back(self) -> None:
		self.driver.back()
	
	@requires_driver
	def current_url(self) -> str:
		return self.driver.current_url
	
	@requires_driver
	def forward(self) -> None:
		self.driver.forward()
	
	@requires_driver
	def get(self, url: str) -> None:
		self.driver.get(url=url)
	
	@requires_driver
	def refresh(self) -> None:
		self.driver.refresh()
	
	@requires_driver
	def title(self) -> str:
		return self.driver.title
