from selenium.webdriver.remote.mobile import Mobile
from selenium.webdriver.common.fedcm.dialog import Dialog
from selenium.webdriver.common.bidi.browser import Browser
from osn_selenium.webdrivers._decorators import requires_driver
from selenium.webdriver.common.bidi.permissions import Permissions
from selenium.webdriver.common.bidi.webextension import WebExtension
from osn_selenium.webdrivers.unified.core.base import UnifiedCoreBaseMixin
from selenium.webdriver.common.bidi.browsing_context import BrowsingContext


__all__ = ["UnifiedCoreComponentsMixin"]


class UnifiedCoreComponentsMixin(UnifiedCoreBaseMixin):
	@requires_driver
	def _browser_impl(self) -> Browser:
		return self._driver_impl.browser
	
	@requires_driver
	def _browsing_context_impl(self) -> BrowsingContext:
		return self._driver_impl.browsing_context
	
	@requires_driver
	def _dialog_impl(self) -> Dialog:
		return self._driver_impl.dialog
	
	@requires_driver
	def _mobile_impl(self) -> Mobile:
		return self._driver_impl.mobile
	
	@requires_driver
	def _permissions_impl(self) -> Permissions:
		return self._driver_impl.permissions
	
	@requires_driver
	def _webextension_impl(self) -> WebExtension:
		return self._driver_impl.webextension
