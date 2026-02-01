import trio
from typing import (
	Optional,
	Protocol,
	Self,
	TypeVar,
	Union,
	runtime_checkable
)


__all__ = [
	"AnyInstanceWrapper",
	"SyncInstanceWrapper",
	"TrioBiDiInstanceWrapper",
	"TrioThreadInstanceWrapper"
]

_LEGACY_OBJECT = TypeVar("_LEGACY_OBJECT")


@runtime_checkable
class TrioThreadInstanceWrapper(Protocol):
	"""
	Protocol for instances that wrap legacy objects and operate within Trio threads.
	"""
	
	@classmethod
	def from_legacy(
			cls,
			legacy_object: _LEGACY_OBJECT,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> Self:
		"""
		Creates an instance of the wrapper from a legacy object.

		Args:
			legacy_object (_LEGACY_OBJECT): The legacy Selenium object to wrap.
			lock (trio.Lock): Trio lock for synchronization.
			limiter (trio.CapacityLimiter): Trio capacity limiter.

		Returns:
			Self: An instance of the wrapper.
		"""
		
		...
	
	@property
	def legacy(self) -> _LEGACY_OBJECT:
		"""
		Returns the underlying legacy Selenium object.

		Returns:
			_LEGACY_OBJECT: The legacy Selenium instance.
		"""
		
		...


@runtime_checkable
class TrioBiDiInstanceWrapper(Protocol):
	"""
	Protocol for instances that wrap legacy objects and operate within Trio threads.
	"""
	
	@classmethod
	def from_legacy(
			cls,
			legacy_object: _LEGACY_OBJECT,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
			trio_token: Optional[trio.lowlevel.TrioToken],
			bidi_buffer_size: Union[int, float],
	) -> Self:
		"""
		Creates an instance of the wrapper from a legacy object.

		Args:
			legacy_object (_LEGACY_OBJECT): The legacy Selenium object to wrap.
			lock (trio.Lock): Trio lock for synchronization.
			limiter (trio.CapacityLimiter): Trio capacity limiter.
			trio_token (Optional[trio.lowlevel.TrioToken]): The Trio token for the current event loop.
			bidi_buffer_size (Union[int, float]): Buffer size for the BiDi task channel.

		Returns:
			Self: An instance of the wrapper.
		"""
		
		...
	
	@property
	def legacy(self) -> _LEGACY_OBJECT:
		"""
		Returns the underlying legacy Selenium object.

		Returns:
			_LEGACY_OBJECT: The legacy Selenium instance.
		"""
		
		...


@runtime_checkable
class SyncInstanceWrapper(Protocol):
	"""
	Protocol for instances that wrap legacy objects for synchronous use.
	"""
	
	@classmethod
	def from_legacy(cls, legacy_object: _LEGACY_OBJECT) -> Self:
		"""
		Creates an instance of the wrapper from a legacy object.

		Args:
			legacy_object (_LEGACY_OBJECT): The legacy Selenium object to wrap.

		Returns:
			Self: An instance of the wrapper.
		"""
		
		...
	
	@property
	def legacy(self) -> _LEGACY_OBJECT:
		"""
		Returns the underlying legacy Selenium object.

		Returns:
			_LEGACY_OBJECT: The legacy Selenium instance.
		"""
		
		...


@runtime_checkable
class AnyInstanceWrapper(Protocol):
	"""
	General protocol for any instance wrapper providing access to a legacy object.
	"""
	
	@property
	def legacy(self) -> _LEGACY_OBJECT:
		"""
		Returns the underlying legacy Selenium object.

		Returns:
			_LEGACY_OBJECT: The legacy Selenium instance.
		"""
		
		...
