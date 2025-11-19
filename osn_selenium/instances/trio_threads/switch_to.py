import trio
from typing import (
	Optional,
	Self,
	Union
)
from osn_selenium.instances.trio_threads.alert import Alert
from osn_selenium.abstract.instances.switch_to import AbstractSwitchTo
from osn_selenium.instances.trio_threads.web_element import WebElement
from osn_selenium.abstract.instances.web_element import AbstractWebElement
from osn_selenium.instances.trio_threads.base_mixin import _TrioThreadMixin
from selenium.webdriver.remote.switch_to import (
	SwitchTo as legacySwitchTo
)


class SwitchTo(_TrioThreadMixin, AbstractSwitchTo):
	def __init__(
			self,
			selenium_switch_to: legacySwitchTo,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> None:
		super().__init__(lock=lock, limiter=limiter)
		
		self._selenium_switch_to = selenium_switch_to
	
	async def active_element(self) -> WebElement:
		return WebElement.from_legacy(
				await self._wrap_to_trio(lambda: self.legacy.active_element),
				lock=self._lock,
				limiter=self._capacity_limiter
		)
	
	async def alert(self) -> Alert:
		return Alert(self.legacy.alert, lock=self._lock, limiter=self._capacity_limiter)
	
	async def default_content(self) -> None:
		await self._wrap_to_trio(self.legacy.default_content)
	
	async def frame(self, frame_reference: Union[str, int, AbstractWebElement],) -> None:
		await self._wrap_to_trio(
				self.legacy.frame,
				frame_reference=frame_reference.legacy
				if isinstance(frame_reference, AbstractWebElement)
				else frame_reference
		)
	
	@classmethod
	def from_legacy(
			cls,
			selenium_switch_to: legacySwitchTo,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> Self:
		"""
		Creates an instance from a legacy Selenium SwitchTo object.

		This factory method is used to wrap an existing Selenium SwitchTo
		instance into the new interface.

		Args:
			selenium_switch_to (legacySwitchTo): The legacy Selenium SwitchTo instance.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.

		Returns:
			Self: A new instance of a class implementing SwitchTo.
		"""
		
		return cls(selenium_switch_to=selenium_switch_to, lock=lock, limiter=limiter)
	
	@property
	def legacy(self) -> legacySwitchTo:
		return self._selenium_switch_to
	
	async def new_window(self, type_hint: Optional[str] = None,) -> None:
		await self._wrap_to_trio(self.legacy.new_window, type_hint)
	
	async def parent_frame(self) -> None:
		await self._wrap_to_trio(self.legacy.parent_frame)
	
	async def window(self, window_name: str,) -> None:
		await self._wrap_to_trio(self.legacy.window, window_name)
