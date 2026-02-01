import trio
from typing import (
	Optional,
	Protocol,
	Union,
	runtime_checkable
)
from selenium.webdriver.remote.webdriver import (
	WebDriver as legacyWebDriver
)


__all__ = ["SyncWebDriver", "TrioBiDiWebDriver", "TrioThreadWebDriver"]


@runtime_checkable
class TrioThreadWebDriver(Protocol):
	"""
	Protocol for a WebDriver that operates within a Trio thread pool.
	"""
	
	@property
	def architecture(self) -> str:
		"""
		Returns the driver architecture.
		"""
		
		...
	
	@property
	def capacity_limiter(self) -> trio.CapacityLimiter:
		"""
		Returns the Trio capacity limiter.
		"""
		
		...
	
	@property
	def driver(self) -> Optional[legacyWebDriver]:
		"""
		Returns the underlying legacy driver.
		"""
		
		...
	
	@property
	def lock(self) -> trio.Lock:
		"""
		Returns the Trio lock.
		"""
		
		...


@runtime_checkable
class TrioBiDiWebDriver(Protocol):
	"""
	Protocol for a WebDriver that supports BiDi and Trio thread pool operations.
	"""
	
	@property
	def architecture(self) -> str:
		"""
		Returns the driver architecture.
		"""
		
		...
	
	@property
	def capacity_limiter(self) -> trio.CapacityLimiter:
		"""
		Returns the Trio capacity limiter.
		"""
		
		...
	
	@property
	def driver(self) -> Optional[legacyWebDriver]:
		"""
		Returns the underlying legacy driver.
		"""
		
		...
	
	@property
	def lock(self) -> trio.Lock:
		"""
		Returns the Trio lock.
		"""
		
		...
	
	@property
	def trio_bidi_buffer_size(self) -> Union[int, float]:
		"""
		Returns the BiDi task buffer size.
		"""
		
		...
	
	@property
	def trio_token(self) -> trio.lowlevel.TrioToken:
		"""
		Returns the Trio event loop token.
		"""
		
		...


@runtime_checkable
class SyncWebDriver(Protocol):
	"""
	Protocol for a synchronous WebDriver.
	"""
	
	@property
	def architecture(self) -> str:
		"""
		Returns the driver architecture.
		"""
		
		...
	
	@property
	def driver(self) -> Optional[legacyWebDriver]:
		"""
		Returns the underlying legacy driver.
		"""
		
		...
