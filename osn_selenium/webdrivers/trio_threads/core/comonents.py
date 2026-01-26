from osn_selenium.trio_threads_mixin import TrioThreadMixin
from osn_selenium.instances.trio_threads.dialog import Dialog
from osn_selenium.instances.trio_threads.mobile import Mobile
from osn_selenium.instances.trio_threads.browser import Browser
from osn_selenium.instances.trio_threads.permissions import Permissions
from osn_selenium.instances.trio_threads.web_extension import WebExtension
from osn_selenium.instances.convert import (
	get_trio_thread_instance_wrapper
)
from osn_selenium.instances.trio_threads.browsing_context import BrowsingContext
from osn_selenium.webdrivers.unified.core.components import (
	UnifiedCoreComponentsMixin
)
from osn_selenium.abstract.webdriver.core.components import (
	AbstractCoreComponentsMixin
)


__all__ = ["CoreComponentsMixin"]


class CoreComponentsMixin(
		UnifiedCoreComponentsMixin,
		TrioThreadMixin,
		AbstractCoreComponentsMixin
):
	"""
	Mixin providing access to specialized browser components for Core WebDrivers.

	Exposes interfaces for interacting with specific browser domains such as
	permissions, mobile emulation, dialog handling, and web extensions.
	"""
	
	async def browser(self) -> Browser:
		legacy = await self.sync_to_trio(sync_function=self._browser_impl)()
		
		return get_trio_thread_instance_wrapper(
				wrapper_class=Browser,
				legacy_object=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	async def browsing_context(self) -> BrowsingContext:
		legacy = await self.sync_to_trio(sync_function=self._browsing_context_impl)()
		
		return get_trio_thread_instance_wrapper(
				wrapper_class=BrowsingContext,
				legacy_object=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	async def dialog(self) -> Dialog:
		legacy = await self.sync_to_trio(sync_function=self._dialog_impl)()
		
		return get_trio_thread_instance_wrapper(
				wrapper_class=Dialog,
				legacy_object=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	async def mobile(self) -> Mobile:
		legacy = await self.sync_to_trio(sync_function=self._mobile_impl)()
		
		return get_trio_thread_instance_wrapper(
				wrapper_class=Mobile,
				legacy_object=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	async def permissions(self) -> Permissions:
		legacy = await self.sync_to_trio(sync_function=self._permissions_impl)()
		
		return get_trio_thread_instance_wrapper(
				wrapper_class=Permissions,
				legacy_object=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	async def webextension(self) -> WebExtension:
		legacy = await self.sync_to_trio(sync_function=self._webextension_impl)()
		
		return get_trio_thread_instance_wrapper(
				wrapper_class=WebExtension,
				legacy_object=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
