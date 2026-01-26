import trio
from typing import (
	Callable,
	Self,
	TypeVar
)
from osn_selenium.trio_threads_mixin import TrioThreadMixin
from osn_selenium.instances.convert import get_legacy_instance
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


class WebDriverWait(UnifiedWebDriverWait, TrioThreadMixin, AbstractWebDriverWait):
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
	) -> None:
		"""
		Initializes the WebDriverWait wrapper.

		Args:
			selenium_webdriver_wait (legacyWebDriverWait): The legacy Selenium WebDriverWait instance to wrap.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.
		"""
		
		UnifiedWebDriverWait.__init__(self, selenium_webdriver_wait=selenium_webdriver_wait)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	@classmethod
	def from_legacy(
			cls,
			legacy_object: legacyWebDriverWait,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> Self:
		"""
		Creates a WebDriverWait wrapper instance from a legacy Selenium object.

		Args:
			legacy_object (legacyWebDriverWait): The legacy object to convert.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.

		Returns:
			Self: An instance of the WebDriverWait wrapper.

		Raises:
			CannotConvertTypeError: If the provided object cannot be converted to legacyWebDriverWait.
		"""
		
		legacy_wait_obj = get_legacy_instance(instance=legacy_object)
		
		if not isinstance(legacy_wait_obj, legacyWebDriverWait):
			raise CannotConvertTypeError(from_=legacyWebDriverWait, to_=legacy_object)
		
		return cls(selenium_webdriver_wait=legacy_wait_obj, lock=lock, limiter=limiter)
	
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
