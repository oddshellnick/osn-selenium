import math
import trio
from typing_extensions import deprecated
from typing import (
	Optional,
	Self,
	Union
)
from osn_selenium.trio_bidi.mixin import TrioBiDiMixin
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.instances.trio_bidi.web_element import WebElement
from osn_selenium.instances.unified.switch_to import UnifiedSwitchTo
from osn_selenium.abstract.instances.switch_to import AbstractSwitchTo
from osn_selenium.exceptions.instance import (
	CannotConvertTypeError
)
from selenium.webdriver.remote.switch_to import (
	SwitchTo as legacySwitchTo
)
from osn_selenium.exceptions.experimental import (
	NotImplementedExperimentalFeatureError
)
from osn_selenium.instances._typehints import (
	SWITCH_TO_TYPEHINT,
	WEB_ELEMENT_TYPEHINT
)


__all__ = ["SwitchTo"]


class SwitchTo(UnifiedSwitchTo, TrioBiDiMixin, AbstractSwitchTo):
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
			trio_token: Optional[trio.lowlevel.TrioToken] = None,
			bidi_buffer_size: Union[int, float] = math.inf,
	) -> None:
		"""
		Initializes the SwitchTo wrapper.

		Args:
			selenium_switch_to (legacySwitchTo): The legacy Selenium SwitchTo instance to wrap.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.
			trio_token (Optional[trio.lowlevel.TrioToken]): The Trio token for the current event loop.
			bidi_buffer_size (Union[int, float]): Buffer size for the BiDi task channel.
		"""
		
		UnifiedSwitchTo.__init__(self, selenium_switch_to=selenium_switch_to)
		
		TrioBiDiMixin.__init__(
				self,
				lock=lock,
				limiter=limiter,
				token=trio_token,
				buffer_size=bidi_buffer_size
		)
	
	@deprecated(
			"This method is currently not supported. It will raise 'NotImplementedExperimentalFeatureError' on call."
	)
	async def active_element(self) -> WebElement:
		raise NotImplementedExperimentalFeatureError(name="SwitchTo.active_element")
	
	@deprecated(
			"This method is currently not supported. It will raise 'NotImplementedExperimentalFeatureError' on call."
	)
	async def alert(self):
		raise NotImplementedExperimentalFeatureError(name="SwitchTo.alert")
	
	@deprecated(
			"This method is currently not supported. It will raise 'NotImplementedExperimentalFeatureError' on call."
	)
	async def default_content(self) -> None:
		raise NotImplementedExperimentalFeatureError(name="SwitchTo.default_content")
	
	@deprecated(
			"This method is currently not supported. It will raise 'NotImplementedExperimentalFeatureError' on call."
	)
	async def frame(self, frame_reference: Union[str, int, WEB_ELEMENT_TYPEHINT]) -> None:
		raise NotImplementedExperimentalFeatureError(name="SwitchTo.frame")
	
	@classmethod
	def from_legacy(
			cls,
			legacy_object: SWITCH_TO_TYPEHINT,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
			trio_token: Optional[trio.lowlevel.TrioToken] = None,
			bidi_buffer_size: Union[int, float] = math.inf,
	) -> Self:
		"""
		Creates an instance from a legacy Selenium SwitchTo object.

		This factory method is used to wrap an existing Selenium SwitchTo
		instance into the new interface.

		Args:
			legacy_object (SWITCH_TO_TYPEHINT): The legacy Selenium SwitchTo instance or its wrapper.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.
			trio_token (Optional[trio.lowlevel.TrioToken]): The Trio token for the current event loop.
			bidi_buffer_size (Union[int, float]): Buffer size for the BiDi task channel.

		Returns:
			Self: A new instance of a class implementing SwitchTo.
		"""
		
		legacy_switch_to_obj = get_legacy_instance(instance=legacy_object)
		
		if not isinstance(legacy_switch_to_obj, legacySwitchTo):
			raise CannotConvertTypeError(from_=legacySwitchTo, to_=legacy_object)
		
		return cls(
				selenium_switch_to=legacy_switch_to_obj,
				lock=lock,
				limiter=limiter,
				trio_token=trio_token,
				bidi_buffer_size=bidi_buffer_size,
		)
	
	@property
	def legacy(self) -> legacySwitchTo:
		return self._legacy_impl
	
	async def new_window(self, type_hint: Optional[str] = None) -> None:
		await self.sync_to_trio(sync_function=self._new_window_impl)(type_hint=type_hint)
	
	async def parent_frame(self) -> None:
		raise NotImplementedExperimentalFeatureError(name="SwitchTo.parent_frame")
	
	async def window(self, window_name: str) -> None:
		await self.sync_to_trio(sync_function=self._window_impl)(window_name=window_name)
