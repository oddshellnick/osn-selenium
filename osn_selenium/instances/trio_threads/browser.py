import trio
from typing import List, Self
from osn_selenium.trio_threads_mixin import TrioThreadMixin
from osn_selenium.instances._typehints import BROWSER_TYPEHINT
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.instances.unified.browser import UnifiedBrowser
from osn_selenium.abstract.instances.browser import AbstractBrowser
from osn_selenium.exceptions.instance import (
	CannotConvertTypeError
)
from selenium.webdriver.common.bidi.browser import (
	Browser as legacyBrowser,
	ClientWindowInfo
)


__all__ = ["Browser"]


class Browser(UnifiedBrowser, TrioThreadMixin, AbstractBrowser):
	"""
	Wrapper for the legacy Selenium BiDi Browser instance.

	Provides methods to manage user contexts (profiles) and inspect client
	window information via the WebDriver BiDi protocol.
	"""
	
	def __init__(
			self,
			selenium_browser: legacyBrowser,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> None:
		"""
		Initializes the Browser wrapper.

		Args:
			selenium_browser (legacyBrowser): The legacy Selenium Browser instance to wrap.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.
		"""
		
		UnifiedBrowser.__init__(self, selenium_browser=selenium_browser)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def create_user_context(self) -> str:
		return await self.sync_to_trio(sync_function=self._create_user_context_impl)()
	
	@classmethod
	def from_legacy(
			cls,
			legacy_object: BROWSER_TYPEHINT,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> Self:
		"""
		Creates an instance from a legacy Selenium Browser object.

		This factory method is used to wrap an existing Selenium Browser
		instance into the new interface.

		Args:
			legacy_object (BROWSER_TYPEHINT): The legacy Selenium Browser instance or its wrapper.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.

		Returns:
			Self: A new instance of a class implementing Browser.
		"""
		
		legacy_browser_obj = get_legacy_instance(instance=legacy_object)
		
		if not isinstance(legacy_browser_obj, legacyBrowser):
			raise CannotConvertTypeError(from_=legacyBrowser, to_=legacy_object)
		
		return cls(selenium_browser=legacy_browser_obj, limiter=limiter, lock=lock)
	
	async def get_client_windows(self) -> List[ClientWindowInfo]:
		return await self.sync_to_trio(sync_function=self._get_client_windows_impl)()
	
	async def get_user_contexts(self) -> List[str]:
		return await self.sync_to_trio(sync_function=self._get_user_contexts_impl)()
	
	@property
	def legacy(self) -> legacyBrowser:
		return self._legacy_impl
	
	async def remove_user_context(self, user_context_id: str) -> None:
		await self.sync_to_trio(sync_function=self._remove_user_context_impl)(user_context_id=user_context_id)
