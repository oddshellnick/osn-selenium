from osn_selenium.instances.sync.dialog import Dialog
from osn_selenium.instances.sync.mobile import Mobile
from osn_selenium.instances.sync.browser import Browser
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.instances.sync.permissions import Permissions
from osn_selenium.webdrivers.sync.core.base import CoreBaseMixin
from osn_selenium.instances.sync.web_extension import WebExtension
from osn_selenium.instances.sync.browsing_context import BrowsingContext
from osn_selenium.instances.convert import (
	get_sync_instance_wrapper
)
from osn_selenium.abstract.webdriver.core.components import (
	AbstractCoreComponentsMixin
)


class CoreComponentsMixin(CoreBaseMixin, AbstractCoreComponentsMixin):
	"""
	Mixin providing access to specialized browser components for Core WebDrivers.

	Exposes interfaces for interacting with specific browser domains such as
	permissions, mobile emulation, dialog handling, and web extensions.
	"""
	
	@requires_driver
	def browser(self) -> Browser:
		legacy = self.driver.browser
		
		return get_sync_instance_wrapper(wrapper_class=Browser, legacy_object=legacy)
	
	@requires_driver
	def browsing_context(self) -> BrowsingContext:
		legacy = self.driver.browsing_context
		
		return get_sync_instance_wrapper(wrapper_class=BrowsingContext, legacy_object=legacy)
	
	@requires_driver
	def dialog(self) -> Dialog:
		legacy = self.driver.dialog
		
		return get_sync_instance_wrapper(wrapper_class=Dialog, legacy_object=legacy)
	
	@requires_driver
	def mobile(self) -> Mobile:
		legacy = self.driver.mobile
		
		return get_sync_instance_wrapper(wrapper_class=Mobile, legacy_object=legacy)
	
	@requires_driver
	def permissions(self) -> Permissions:
		legacy = self.driver.permissions
		
		return get_sync_instance_wrapper(wrapper_class=Permissions, legacy_object=legacy)
	
	@requires_driver
	def webextension(self) -> WebExtension:
		legacy = self.driver.webextension
		
		return get_sync_instance_wrapper(wrapper_class=WebExtension, legacy_object=legacy)
