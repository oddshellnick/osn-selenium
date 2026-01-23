from osn_selenium.instances.sync.dialog import Dialog
from osn_selenium.instances.sync.mobile import Mobile
from osn_selenium.instances.sync.browser import Browser
from osn_selenium.instances.sync.permissions import Permissions
from osn_selenium.instances.sync.web_extension import WebExtension
from osn_selenium.instances.sync.browsing_context import BrowsingContext
from osn_selenium.instances.convert import (
	get_sync_instance_wrapper
)
from osn_selenium.webdrivers.unified.core.components import (
	UnifiedCoreComponentsMixin
)
from osn_selenium.abstract.webdriver.core.components import (
	AbstractCoreComponentsMixin
)


__all__ = ["CoreComponentsMixin"]


class CoreComponentsMixin(UnifiedCoreComponentsMixin, AbstractCoreComponentsMixin):
	"""
	Mixin providing access to specialized browser components for Core WebDrivers.

	Exposes interfaces for interacting with specific browser domains such as
	permissions, mobile emulation, dialog handling, and web extensions.
	"""
	
	def browser(self) -> Browser:
		legacy = self._browser_impl()
		
		return get_sync_instance_wrapper(wrapper_class=Browser, legacy_object=legacy)
	
	def browsing_context(self) -> BrowsingContext:
		legacy = self._browsing_context_impl()
		
		return get_sync_instance_wrapper(wrapper_class=BrowsingContext, legacy_object=legacy)
	
	def dialog(self) -> Dialog:
		legacy = self._dialog_impl()
		
		return get_sync_instance_wrapper(wrapper_class=Dialog, legacy_object=legacy)
	
	def mobile(self) -> Mobile:
		legacy = self._mobile_impl()
		
		return get_sync_instance_wrapper(wrapper_class=Mobile, legacy_object=legacy)
	
	def permissions(self) -> Permissions:
		legacy = self._permissions_impl()
		
		return get_sync_instance_wrapper(wrapper_class=Permissions, legacy_object=legacy)
	
	def webextension(self) -> WebExtension:
		legacy = self._webextension_impl()
		
		return get_sync_instance_wrapper(wrapper_class=WebExtension, legacy_object=legacy)
