import trio
from typing import (
	Callable,
	Self,
	TypeVar
)
from osn_selenium.trio_base_mixin import _TrioThreadMixin
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.instances.types import (
	WebDriverWaitInputType
)
from osn_selenium.instances.errors import (
	ExpectedTypeError,
	TypesConvertError
)
from selenium.webdriver.support.wait import (
	WebDriverWait as legacyWebDriverWait
)
from osn_selenium.abstract.instances.web_driver_wait import (
	AbstractWebDriverWait
)


OUTPUT = TypeVar("OUTPUT")


class WebDriverWait(_TrioThreadMixin, AbstractWebDriverWait):
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
		
		super().__init__(lock=lock, limiter=limiter)
		
		if not isinstance(selenium_webdriver_wait, legacyWebDriverWait):
			raise ExpectedTypeError(
					expected_class=legacyWebDriverWait,
					received_instance=selenium_webdriver_wait
			)
		
		self._selenium_webdriver_wait = selenium_webdriver_wait
	
	@classmethod
	def from_legacy(
			cls,
			selenium_webdriver_wait: legacyWebDriverWait,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> Self:
		legacy_wait_obj = get_legacy_instance(selenium_webdriver_wait)
		
		if not isinstance(legacy_wait_obj, legacyWebDriverWait):
			raise TypesConvertError(from_=legacyWebDriverWait, to_=selenium_webdriver_wait)
		
		return cls(selenium_webdriver_wait=legacy_wait_obj, lock=lock, limiter=limiter)
	
	@property
	def legacy(self) -> legacyWebDriverWait:
		return self._selenium_webdriver_wait
	
	async def until(
			self,
			method: Callable[[WebDriverWaitInputType], OUTPUT],
			message: str = ""
	) -> OUTPUT:
		return await self._wrap_to_trio(self._selenium_webdriver_wait.until, method=method, message=message)
	
	async def until_not(
			self,
			method: Callable[[WebDriverWaitInputType], OUTPUT],
			message: str = ""
	) -> OUTPUT:
		return await self._wrap_to_trio(
				self._selenium_webdriver_wait.until_not,
				method=method,
				message=message
		)
