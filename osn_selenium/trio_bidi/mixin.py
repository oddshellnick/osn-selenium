import trio
from contextlib import asynccontextmanager
from osn_selenium.trio_threads_mixin import TrioThreadMixin
from osn_selenium.trio_bidi.connection_pool import BiDiConnectionPool
from osn_selenium.trio_bidi._context_vars import (
	CURRENT_BROWSING_CONTEXT
)
from osn_selenium.trio_bidi.remote_connection import (
	BiDiBridgeRemoteConnection
)
from osn_selenium.trio_bidi._typehints import (
	CURRENT_BROWSING_CONTEXT_TYPEHINT
)
from osn_selenium._trio_threads_helpers import (
	sync_to_trio,
	sync_to_trio_context
)
from typing import (
	Any,
	AsyncContextManager,
	AsyncGenerator,
	Callable,
	ContextManager,
	Coroutine,
	Optional,
	ParamSpec,
	TypeVar,
	Union
)


__all__ = ["TrioBiDiMixin"]

_METHOD_INPUT = ParamSpec("_METHOD_INPUT")
_METHOD_OUTPUT = TypeVar("_METHOD_OUTPUT")


class TrioBiDiMixin(TrioThreadMixin):
	"""
	Mixin that provides WebDriver with Trio-based BiDi context switching capabilities.
	"""
	
	def __init__(
			self,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
			token: Optional[trio.lowlevel.TrioToken],
			buffer_size: Union[int, float],
	) -> None:
		"""
		Initializes the TrioBiDiMixin.

		Args:
			lock (trio.Lock): Trio lock for synchronization.
			limiter (trio.CapacityLimiter): Limiter for concurrent operations.
			token (Optional[trio.lowlevel.TrioToken]): The Trio token for the current event loop.
			buffer_size (Union[int, float]): Buffer size for the BiDi task channel.
		"""
		
		super().__init__(lock=lock, limiter=limiter)
		
		self._trio_token = token if token is not None else trio.lowlevel.current_trio_token()
		
		self._trio_bidi_buffer_size = buffer_size
		self._bidi_bridge_connection_pool: Optional[BiDiConnectionPool] = None
		self._bidi_bridge_remote_connection: Optional[BiDiBridgeRemoteConnection] = None
	
	@property
	def current_context_id(self) -> CURRENT_BROWSING_CONTEXT_TYPEHINT:
		"""
		Returns the browsing context ID (tab ID) associated with the current Trio task.
		This operation is instant and does not require a driver call.

		Returns:
			CURRENT_BROWSING_CONTEXT_TYPEHINT: The current context ID.
		"""
		
		return CURRENT_BROWSING_CONTEXT.get()
	
	@staticmethod
	def switch_context(context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT) -> None:
		"""
		Updates the target context for the CURRENT task only.
		Equivalent to `driver.switch_to.window` but strictly local to the coroutine.

		Args:
			context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The ID of the browsing context to switch to.
		"""
		
		CURRENT_BROWSING_CONTEXT.set(context_id)
	
	def sync_to_trio(
			self,
			sync_function: Callable[_METHOD_INPUT, _METHOD_OUTPUT],
			lock: bool = False,
			exchange_context:bool = True,
	) -> Callable[_METHOD_INPUT, Coroutine[Any, Any, _METHOD_OUTPUT]]:
		"""
		Wraps a synchronous function to run within a Trio thread pool using a lock and limiter.

		Args:
			sync_function (Callable[_METHOD_INPUT, _METHOD_OUTPUT]): The synchronous function to wrap.
			lock (bool): Whether to use the internal lock for synchronization.
			exchange_context (bool): Whether to synchronize context variables between threads.

		Returns:
			Callable[_METHOD_INPUT, Coroutine[Any, Any, _METHOD_OUTPUT]]: An async wrapper for the sync function.
		"""
		
		return sync_to_trio(
				sync_function=sync_function,
				lock_object=self._lock,
				capacity_limiter_object=self._capacity_limiter,
				lock=lock,
				exchange_context=exchange_context,
		)
	
	def sync_to_trio_context(
			self,
			context_manager_factory: Callable[_METHOD_INPUT, ContextManager[_METHOD_OUTPUT]],
			lock: bool = False,
			exchange_context: bool = True,
	) -> Callable[_METHOD_INPUT, AsyncContextManager[_METHOD_OUTPUT]]:
		"""
		Converts a synchronous context manager factory to an asynchronous Trio-compatible context manager.

		Args:
			context_manager_factory (Callable[_METHOD_INPUT, ContextManager[_METHOD_OUTPUT]]): Factory function returning a context manager.
			lock (bool): Whether to use the internal lock for synchronization.
			exchange_context (bool): Whether to synchronize context variables between threads.

		Returns:
			Callable[_METHOD_INPUT, AsyncContextManager[_METHOD_OUTPUT]]: An async function returning an async context manager.
		"""
		
		return sync_to_trio_context(
				context_manager_factory=context_manager_factory,
				lock_object=self._lock,
				capacity_limiter_object=self._capacity_limiter,
				lock=lock,
				exchange_context=exchange_context,
		)
	
	@property
	def trio_bidi_buffer_size(self) -> Union[int, float]:
		"""
		Returns the configured buffer size for BiDi operations.

		Returns:
			Union[int, float]: The buffer size.
		"""
		
		return self._trio_bidi_buffer_size
	
	@property
	def trio_token(self) -> trio.lowlevel.TrioToken:
		"""
		Returns the Trio token associated with this driver.

		Returns:
			trio.lowlevel.TrioToken: The event loop token.
		"""
		
		return self._trio_token
	
	@asynccontextmanager
	async def use_context(self, context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT) -> AsyncGenerator[None, Any]:
		"""
		Context manager for temporary context switching.

		Args:
			context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The ID of the browsing context to switch to.

		EXAMPLES
		________
		>>> async with driver.use_context(tab_id):
		...	 await driver.get("https://example.com")
		... # Context automatically reverts here
		"""
		
		token = CURRENT_BROWSING_CONTEXT.set(context_id)
		
		try:
			yield
		finally:
			CURRENT_BROWSING_CONTEXT.reset(token)
