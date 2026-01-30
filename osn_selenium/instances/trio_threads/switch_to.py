import trio
from typing import (
	Optional,
	Self,
	Union
)
from osn_selenium.trio_threads_mixin import TrioThreadMixin
from osn_selenium.instances.trio_threads.alert import Alert
from osn_selenium.instances.unified.switch_to import UnifiedSwitchTo
from osn_selenium.abstract.instances.switch_to import AbstractSwitchTo
from osn_selenium.instances.trio_threads.web_element import WebElement
from osn_selenium.exceptions.instance import (
	CannotConvertTypeError
)
from selenium.webdriver.remote.switch_to import (
	SwitchTo as legacySwitchTo
)
from osn_selenium.instances._typehints import (
	SWITCH_TO_TYPEHINT,
	WEB_ELEMENT_TYPEHINT
)
from osn_selenium.instances.convert import (
	get_legacy_instance,
	get_trio_thread_instance_wrapper
)


__all__ = ["SwitchTo"]


class SwitchTo(UnifiedSwitchTo, TrioThreadMixin, AbstractSwitchTo):
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
		
		UnifiedSwitchTo.__init__(self, selenium_switch_to=selenium_switch_to)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def active_element(self) -> WebElement:
		legacy_element = await self.sync_to_trio(sync_function=self._active_element_impl)()
		
		return get_trio_thread_instance_wrapper(
				wrapper_class=WebElement,
				legacy_object=legacy_element,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	async def alert(self) -> Alert:
		legacy_alert_instance = await self.sync_to_trio(sync_function=self._alert_impl)()
		
		return get_trio_thread_instance_wrapper(
				wrapper_class=Alert,
				legacy_object=legacy_alert_instance,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	async def default_content(self) -> None:
		await self.sync_to_trio(sync_function=self._default_content_impl)()
	
	async def frame(self, frame_reference: Union[str, int, WEB_ELEMENT_TYPEHINT]) -> None:
		await self.sync_to_trio(sync_function=self._frame_impl)(frame_reference=frame_reference)
	
	@classmethod
	def from_legacy(
			cls,
			legacy_object: SWITCH_TO_TYPEHINT,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> Self:
		"""
		Creates an instance from a legacy Selenium SwitchTo object.

		This factory method is used to wrap an existing Selenium SwitchTo
		instance into the new interface.

		Args:
			legacy_object (SWITCH_TO_TYPEHINT): The legacy Selenium SwitchTo instance or its wrapper.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.

		Returns:
			Self: A new instance of a class implementing SwitchTo.
		"""
		
		legacy_switch_to_obj = get_legacy_instance(instance=legacy_object)
		
		if not isinstance(legacy_switch_to_obj, legacySwitchTo):
			raise CannotConvertTypeError(from_=legacySwitchTo, to_=legacy_object)
		
		return cls(selenium_switch_to=legacy_switch_to_obj, lock=lock, limiter=limiter)
	
	@property
	def legacy(self) -> legacySwitchTo:
		return self._legacy_impl
	
	async def new_window(self, type_hint: Optional[str] = None) -> None:
		await self.sync_to_trio(sync_function=self._new_window_impl)(type_hint=type_hint)
	
	async def parent_frame(self) -> None:
		await self.sync_to_trio(sync_function=self._parent_frame_impl)()
	
	async def window(self, window_name: str) -> None:
		await self.sync_to_trio(sync_function=self._window_impl)(window_name=window_name)
