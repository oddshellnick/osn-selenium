import trio
from typing import Optional, Self
from osn_selenium.trio_threads_mixin import TrioThreadMixin
from osn_selenium.instances._typehints import ALERT_TYPEHINT
from osn_selenium.instances.unified.alert import UnifiedAlert
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.abstract.instances.alert import AbstractAlert
from selenium.webdriver.common.alert import Alert as legacyAlert
from osn_selenium.exceptions.instance import (
	CannotConvertTypeError
)


__all__ = ["Alert"]


class Alert(UnifiedAlert, TrioThreadMixin, AbstractAlert):
	"""
	Wrapper for the legacy Selenium Alert instance.

	Manages browser alerts, prompts, and confirmation dialogs, allowing
	acceptance, dismissal, text retrieval, and input.
	"""
	
	def __init__(
			self,
			selenium_alert: legacyAlert,
			lock: trio.Lock,
			limiter: Optional[trio.CapacityLimiter] = None,
	) -> None:
		"""
		Initializes the Alert wrapper.

		Args:
			selenium_alert (legacyAlert): The legacy Selenium Alert instance to wrap.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.
		"""
		
		UnifiedAlert.__init__(self, selenium_alert=selenium_alert)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def accept(self) -> None:
		await self.sync_to_trio(sync_function=self._accept_impl)()
	
	async def dismiss(self) -> None:
		await self.sync_to_trio(sync_function=self._dismiss_impl)()
	
	@classmethod
	def from_legacy(
			cls,
			legacy_object: ALERT_TYPEHINT,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> Self:
		"""
		Creates an instance from a legacy Selenium Alert object.

		This factory method is used to wrap an existing Selenium Alert
		instance into the new interface.

		Args:
			legacy_object (ALERT_TYPEHINT): The legacy Selenium Alert instance or its wrapper.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.

		Returns:
			Self: A new instance of a class implementing Alert.
		"""
		
		legacy_alert_obj = get_legacy_instance(instance=legacy_object)
		
		if not isinstance(legacy_alert_obj, legacyAlert):
			raise CannotConvertTypeError(from_=legacyAlert, to_=legacy_object)
		
		return cls(selenium_alert=legacy_alert_obj, lock=lock, limiter=limiter)
	
	@property
	def legacy(self) -> legacyAlert:
		return self._legacy_impl
	
	async def send_keys(self, keysToSend: str) -> None:
		await self.sync_to_trio(sync_function=self._send_keys_impl)(keysToSend=keysToSend)
	
	async def text(self) -> str:
		return await self.sync_to_trio(sync_function=self._text_impl)()
