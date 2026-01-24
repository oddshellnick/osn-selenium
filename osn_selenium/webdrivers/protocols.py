import trio
from typing import (
	Optional,
	Protocol,
	runtime_checkable
)
from selenium.webdriver.remote.webdriver import (
	WebDriver as legacyWebDriver
)


__all__ = ["SyncWebDriver", "TrioThreadWebDriver"]


@runtime_checkable
class TrioThreadWebDriver(Protocol):
	"""
	Protocol for a WebDriver that operates within a Trio thread pool.
	"""
	
	@property
	def architecture(self) -> str:
		...
	
	@property
	def capacity_limiter(self) -> trio.CapacityLimiter:
		...
	
	@property
	def driver(self) -> Optional[legacyWebDriver]:
		...
	
	@property
	def lock(self) -> trio.Lock:
		...


@runtime_checkable
class SyncWebDriver(Protocol):
	"""
	Protocol for a synchronous WebDriver.
	"""
	
	@property
	def architecture(self) -> str:
		...
	
	@property
	def driver(self) -> Optional[legacyWebDriver]:
		...
