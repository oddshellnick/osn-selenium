import trio
from typing import Any, Optional, Self
from osn_selenium.abstract.instances.alert import AbstractAlert
from selenium.webdriver.common.alert import Alert as legacyAlert
from osn_selenium.instances.trio_threads.base_mixin import _TrioThreadMixin


class Alert(_TrioThreadMixin, AbstractAlert):
	def __init__(
			self,
			selenium_alert: legacyAlert,
			lock: trio.Lock,
			limiter: Optional[trio.CapacityLimiter] = None,
	) -> None:
		super().__init__(lock=lock, limiter=limiter)
		
		self._selenium_alert = selenium_alert
	
	async def accept(self) -> None:
		await self._wrap_to_trio(self._selenium_alert.accept)
	
	async def dismiss(self) -> None:
		await self._wrap_to_trio(self._selenium_alert.dismiss)
	
	@classmethod
	def from_legacy(
			cls,
			selenium_alert: legacyAlert,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> Self:
		"""
		Creates an instance from a legacy Selenium Alert object.

		This factory method is used to wrap an existing Selenium Alert
		instance into the new interface.

		Args:
			selenium_alert (legacyAlert): The legacy Selenium Alert instance.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.

		Returns:
			Self: A new instance of a class implementing Alert.
		"""
		
		return cls(selenium_alert=selenium_alert, lock=lock, limiter=limiter)
	
	@property
	def legacy(self) -> legacyAlert:
		return self._selenium_alert
	
	async def send_keys(self, keysToSend: str,) -> None:
		await self._wrap_to_trio(self._selenium_alert.send_keys, keysToSend=keysToSend)
	
	async def text(self) -> str:
		return await self._wrap_to_trio(lambda: self._selenium_alert.text)
