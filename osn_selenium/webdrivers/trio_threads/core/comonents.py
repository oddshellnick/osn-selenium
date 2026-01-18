from osn_selenium.instances.trio_threads.dialog import Dialog
from osn_selenium.instances.trio_threads.mobile import Mobile
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.instances.trio_threads.browser import Browser
from osn_selenium.instances.trio_threads.permissions import Permissions
from osn_selenium.webdrivers.trio_threads.core.base import CoreBaseMixin
from osn_selenium.instances.trio_threads.web_extension import WebExtension
from osn_selenium.instances.trio_threads.browsing_context import BrowsingContext
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
	async def browser(self) -> Browser:
		legacy = await self._sync_to_trio(lambda: self.driver.browser)
		
		return Browser(
				selenium_browser=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter
		)
	
	@requires_driver
	async def browsing_context(self) -> BrowsingContext:
		legacy = await self._sync_to_trio(lambda: self.driver.browsing_context)
		
		return BrowsingContext(
				selenium_browsing_context=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	@requires_driver
	async def dialog(self) -> Dialog:
		legacy = await self._sync_to_trio(lambda: self.driver.dialog)
		
		return Dialog(legacy, lock=self._lock, limiter=self._capacity_limiter)
	
	@requires_driver
	async def mobile(self) -> Mobile:
		legacy = await self._sync_to_trio(lambda: self.driver.mobile)
		
		return Mobile(
				selenium_mobile=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter
		)
	
	@requires_driver
	async def permissions(self) -> Permissions:
		legacy = await self._sync_to_trio(lambda: self.driver.permissions)
		
		return Permissions(
				selenium_permissions=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter
		)
	
	@requires_driver
	async def webextension(self) -> WebExtension:
		legacy = await self._sync_to_trio(lambda: self.driver.webextension)
		
		return WebExtension(
				selenium_web_extension=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter
		)
