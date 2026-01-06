from osn_selenium.webdrivers.sync.base.base import BaseMixin
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.abstract.webdriver.base.navigation import (
	AbstractNavigationMixin
)


class NavigationMixin(BaseMixin, AbstractNavigationMixin):
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
