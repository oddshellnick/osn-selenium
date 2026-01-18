import trio
from typing import (
	Optional,
	Self,
	Union
)
from osn_selenium.base_mixin import TrioThreadMixin
from osn_selenium.instances.trio_threads.alert import Alert
from osn_selenium.abstract.instances.switch_to import AbstractSwitchTo
from osn_selenium.instances.trio_threads.web_element import WebElement
from selenium.webdriver.remote.switch_to import (
	SwitchTo as legacySwitchTo
)
from osn_selenium.instances.errors import (
	ExpectedTypeError,
	TypesConvertError
)
from osn_selenium.instances.types import (
	SWITCH_TO_TYPEHINT,
	WEB_ELEMENT_TYPEHINT
)
from osn_selenium.instances.convert import (
	get_legacy_frame_reference,
	get_legacy_instance
)


class SwitchTo(TrioThreadMixin, AbstractSwitchTo):
	"""
	Wrapper for the legacy Selenium SwitchTo instance.

	Provides mechanisms to change the driver's focus to different frames,
	windows, or alerts.
	"""
	
	def __init__(
			self,
			selenium_switch_to: legacySwitchTo,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> None:
		"""
		Initializes the SwitchTo wrapper.

		Args:
			selenium_switch_to (legacySwitchTo): The legacy Selenium SwitchTo instance to wrap.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.
		"""
		
		super().__init__(lock=lock, limiter=limiter)
		
		if not isinstance(selenium_switch_to, legacySwitchTo):
			raise ExpectedTypeError(expected_class=legacySwitchTo, received_instance=selenium_switch_to)
		
		self._selenium_switch_to = selenium_switch_to
	
	async def active_element(self) -> WebElement:
		return WebElement.from_legacy(
				await self._sync_to_trio(lambda: self.legacy.active_element),
				lock=self._lock,
				limiter=self._capacity_limiter
		)
	
	async def alert(self) -> Alert:
		legacy_alert_instance = await self._sync_to_trio(lambda: self.legacy.alert)
		
		return Alert(
				selenium_alert=legacy_alert_instance,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	async def default_content(self) -> None:
		await self._sync_to_trio(self.legacy.default_content)
	
	async def frame(self, frame_reference: Union[str, int, WEB_ELEMENT_TYPEHINT]) -> None:
		await self._sync_to_trio(
				self.legacy.frame,
				frame_reference=get_legacy_frame_reference(frame_reference)
		)
	
	@classmethod
	def from_legacy(
			cls,
			selenium_switch_to: SWITCH_TO_TYPEHINT,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> Self:
		"""
		Creates an instance from a legacy Selenium SwitchTo object.

		This factory method is used to wrap an existing Selenium SwitchTo
		instance into the new interface.

		Args:
			selenium_switch_to (SWITCH_TO_TYPEHINT): The legacy Selenium SwitchTo instance or its wrapper.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.

		Returns:
			Self: A new instance of a class implementing SwitchTo.
		"""
		
		legacy_switch_to_obj = get_legacy_instance(selenium_switch_to)
		if not isinstance(legacy_switch_to_obj, legacySwitchTo):
			raise TypesConvertError(from_=legacySwitchTo, to_=selenium_switch_to)
		
		return cls(selenium_switch_to=legacy_switch_to_obj, lock=lock, limiter=limiter)
	
	@property
	def legacy(self) -> legacySwitchTo:
		return self._selenium_switch_to
	
	async def new_window(self, type_hint: Optional[str] = None) -> None:
		await self._sync_to_trio(self.legacy.new_window, type_hint)
	
	async def parent_frame(self) -> None:
		await self._sync_to_trio(self.legacy.parent_frame)
	
	async def window(self, window_name: str) -> None:
		await self._sync_to_trio(self.legacy.window, window_name)
