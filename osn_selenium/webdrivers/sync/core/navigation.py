from osn_selenium.webdrivers.unified.core.navigation import (
	UnifiedCoreNavigationMixin
)
from osn_selenium.abstract.webdriver.core.navigation import (
	AbstractCoreNavigationMixin
)


__all__ = ["CoreNavigationMixin"]


class CoreNavigationMixin(UnifiedCoreNavigationMixin, AbstractCoreNavigationMixin):
	"""
	Mixin controlling browser navigation for Core WebDrivers.

	Includes standard navigation commands such as visiting URLs, history
	traversal (back/forward), and page refreshing.
	"""
	
	def back(self) -> None:
		self._back_impl()
	
	def current_url(self) -> str:
		return self._current_url_impl()
	
	def forward(self) -> None:
		self._forward_impl()
	
	def get(self, url: str) -> None:
		self._get_impl(url=url)
	
	def refresh(self) -> None:
		self._refresh_impl()
	
	def title(self) -> str:
		return self._title_impl()
