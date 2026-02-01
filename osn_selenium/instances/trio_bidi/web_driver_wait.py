import math
import trio
from osn_selenium.trio_bidi.mixin import TrioBiDiMixin
from osn_selenium.instances.convert import get_legacy_instance
from typing import (
	Callable,
	Optional,
	Self,
	TypeVar,
	Union
)
from osn_selenium.exceptions.instance import (
	CannotConvertTypeError
)
from osn_selenium.instances._typehints import (
	WebDriverWaitInputType
)
from osn_selenium.instances.unified.web_driver_wait import UnifiedWebDriverWait
from selenium.webdriver.support.wait import (
	WebDriverWait as legacyWebDriverWait
)
from osn_selenium.abstract.instances.web_driver_wait import (
	AbstractWebDriverWait
)


__all__ = ["OUTPUT", "WebDriverWait"]

OUTPUT = TypeVar("OUTPUT")


class WebDriverWait(UnifiedWebDriverWait, TrioBiDiMixin, AbstractWebDriverWait):
	"""
	Wrapper for the legacy Selenium WebDriverWait instance.

	Provides conditional waiting functionality, pausing execution until
	specific conditions (expected conditions) are met or a timeout occurs.
	"""
	
	def __init__(
			self,
			selenium_webdriver_wait: legacyWebDriverWait,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
			trio_token: Optional[trio.lowlevel.TrioToken] = None,
			bidi_buffer_size: Union[int, float] = math.inf,
	) -> None:
		"""
		Initializes the WebDriverWait wrapper.

		Args:
			selenium_webdriver_wait (legacyWebDriverWait): The legacy Selenium WebDriverWait instance to wrap.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.
			trio_token (Optional[trio.lowlevel.TrioToken]): The Trio token for the current event loop.
			bidi_buffer_size (Union[int, float]): Buffer size for the BiDi task channel.
		"""
		
		UnifiedWebDriverWait.__init__(self, selenium_webdriver_wait=selenium_webdriver_wait)
		
		TrioBiDiMixin.__init__(
				self,
				lock=lock,
				limiter=limiter,
				token=trio_token,
				buffer_size=bidi_buffer_size
		)
	
	@classmethod
	def from_legacy(
			cls,
			legacy_object: legacyWebDriverWait,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
			trio_token: Optional[trio.lowlevel.TrioToken] = None,
			bidi_buffer_size: Union[int, float] = math.inf,
	) -> Self:
		"""
		Creates a WebDriverWait wrapper instance from a legacy Selenium object.

		Args:
			legacy_object (legacyWebDriverWait): The legacy object to convert.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.
			trio_token (Optional[trio.lowlevel.TrioToken]): The Trio token for the current event loop.
			bidi_buffer_size (Union[int, float]): Buffer size for the BiDi task channel.

		Returns:
			Self: An instance of the WebDriverWait wrapper.

		Raises:
			CannotConvertTypeError: If the provided object cannot be converted to legacyWebDriverWait.
		"""
		
		legacy_wait_obj = get_legacy_instance(instance=legacy_object)
		
		if not isinstance(legacy_wait_obj, legacyWebDriverWait):
			raise CannotConvertTypeError(from_=legacyWebDriverWait, to_=legacy_object)
		
		return cls(
				selenium_webdriver_wait=legacy_wait_obj,
				lock=lock,
				limiter=limiter,
				trio_token=trio_token,
				bidi_buffer_size=bidi_buffer_size,
		)
	
	@property
	def legacy(self) -> legacyWebDriverWait:
		return self._legacy_impl
	
	async def until(
			self,
			method: Callable[[WebDriverWaitInputType], OUTPUT],
			message: str = ""
	) -> OUTPUT:
		return await self.sync_to_trio(sync_function=self._until_impl)(method=method, message=message)
	
	async def until_not(
			self,
			method: Callable[[WebDriverWaitInputType], OUTPUT],
			message: str = ""
	) -> OUTPUT:
		return await self.sync_to_trio(sync_function=self._until_not_impl)(method=method, message=message)
