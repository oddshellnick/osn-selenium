import trio
from typing import Optional, Self
from osn_selenium.base_mixin import TrioThreadMixin
from osn_selenium.instances.types import ALERT_TYPEHINT
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.abstract.instances.alert import AbstractAlert
from selenium.webdriver.common.alert import Alert as legacyAlert
from osn_selenium.instances.errors import (
	ExpectedTypeError,
	TypesConvertError
)


class Alert(TrioThreadMixin, AbstractAlert):
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
		
		super().__init__(lock=lock, limiter=limiter)
		
		if not isinstance(selenium_alert, legacyAlert):
			raise ExpectedTypeError(expected_class=legacyAlert, received_instance=selenium_alert)
		
		self._selenium_alert = selenium_alert
	
	async def accept(self) -> None:
		await self._sync_to_trio(self._selenium_alert.accept)
	
	async def dismiss(self) -> None:
		await self._sync_to_trio(self._selenium_alert.dismiss)
	
	@classmethod
	def from_legacy(
			cls,
			selenium_alert: ALERT_TYPEHINT,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> Self:
		"""
		Creates an instance from a legacy Selenium Alert object.

		This factory method is used to wrap an existing Selenium Alert
		instance into the new interface.

		Args:
			selenium_alert (ALERT_TYPEHINT): The legacy Selenium Alert instance or its wrapper.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.

		Returns:
			Self: A new instance of a class implementing Alert.
		"""
		
		legacy_alert_obj = get_legacy_instance(selenium_alert)
		
		if not isinstance(legacy_alert_obj, legacyAlert):
			raise TypesConvertError(from_=legacyAlert, to_=selenium_alert)
		
		return cls(selenium_alert=legacy_alert_obj, lock=lock, limiter=limiter)
	
	@property
	def legacy(self) -> legacyAlert:
		return self._selenium_alert
	
	async def send_keys(self, keysToSend: str) -> None:
		await self._sync_to_trio(self._selenium_alert.send_keys, keysToSend=keysToSend)
	
	async def text(self) -> str:
		return await self._sync_to_trio(lambda: self._selenium_alert.text)
