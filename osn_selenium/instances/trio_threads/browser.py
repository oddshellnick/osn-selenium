import trio
from typing import List, Self
from osn_selenium.abstract.instances.browser import AbstractBrowser
from osn_selenium.instances.trio_threads.base_mixin import _TrioThreadMixin
from selenium.webdriver.common.bidi.browser import (
	Browser as legacyBrowser,
	ClientWindowInfo
)


class Browser(_TrioThreadMixin, AbstractBrowser):
	def __init__(
			self,
			selenium_browser: legacyBrowser,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> None:
		super().__init__(lock=lock, limiter=limiter)
		
		self._selenium_browser = selenium_browser
	
	async def create_user_context(self) -> str:
		return await self._wrap_to_trio(self._selenium_browser.create_user_context)
	
	@classmethod
	def from_legacy(
			cls,
			selenium_browser: legacyBrowser,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> Self:
		"""
		Creates an instance from a legacy Selenium Browser object.

		This factory method is used to wrap an existing Selenium Browser
		instance into the new interface.

		Args:
			selenium_browser (legacyBrowser): The legacy Selenium Browser instance.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.

		Returns:
			Self: A new instance of a class implementing Browser.
		"""
		
		return cls(selenium_browser=selenium_browser, limiter=limiter, lock=lock)
	
	async def get_client_windows(self) -> List[ClientWindowInfo]:
		return await self._wrap_to_trio(self._selenium_browser.get_client_windows)
	
	async def get_user_contexts(self) -> List[str]:
		return await self._wrap_to_trio(self._selenium_browser.get_user_contexts)
	
	@property
	def legacy(self) -> legacyBrowser:
		return self._selenium_browser
	
	async def remove_user_context(self, user_context_id: str) -> None:
		await self._wrap_to_trio(
				self._selenium_browser.remove_user_context,
				user_context_id=user_context_id
		)
