from osn_selenium.instances.sync.dialog import Dialog
from osn_selenium.instances.sync.mobile import Mobile
from osn_selenium.instances.sync.browser import Browser
from osn_selenium.webdrivers.sync.core.base import CoreBaseMixin
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.instances.sync.permissions import Permissions
from osn_selenium.instances.sync.web_extension import WebExtension
from osn_selenium.instances.sync.browsing_context import BrowsingContext
from osn_selenium.abstract.webdriver.core.components import (
	AbstractCoreComponentsMixin
)


class CoreComponentsMixin(CoreBaseMixin, AbstractCoreComponentsMixin):
	@requires_driver
	def browser(self) -> Browser:
		legacy = self.driver.browser
		
		return Browser(selenium_browser=legacy)
	
	@requires_driver
	def browsing_context(self) -> BrowsingContext:
		legacy = self.driver.browsing_context
		
		return BrowsingContext(selenium_browsing_context=legacy)
	
	@requires_driver
	def dialog(self) -> Dialog:
		legacy = self.driver.dialog
		
		return Dialog(legacy)
	
	@requires_driver
	def mobile(self) -> Mobile:
		legacy = self.driver.mobile
		
		return Mobile(selenium_mobile=legacy)
	
	@requires_driver
	def permissions(self) -> Permissions:
		legacy = self.driver.permissions
		
		return Permissions(selenium_permissions=legacy)
	
	@requires_driver
	def webextension(self) -> WebExtension:
		legacy = self.driver.webextension
		
		return WebExtension(selenium_web_extension=legacy)
