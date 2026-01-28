import trio
from osn_selenium.trio_threads_mixin import TrioThreadMixin
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.exceptions.instance import (
	CannotConvertTypeError
)
from osn_selenium.instances._typehints import (
	BROWSING_CONTEXT_TYPEHINT
)
from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Self,
	Union
)
from osn_selenium.instances.unified.browsing_context import (
	UnifiedBrowsingContext
)
from osn_selenium.abstract.instances.browsing_context import (
	AbstractBrowsingContext
)
from selenium.webdriver.common.bidi.browsing_context import (
	BrowsingContext as legacyBrowsingContext,
	BrowsingContextInfo
)


__all__ = ["BrowsingContext"]


class BrowsingContext(UnifiedBrowsingContext, TrioThreadMixin, AbstractBrowsingContext):
	"""
	Wrapper for the legacy Selenium BiDi BrowsingContext instance (Trio/Async).

	Controls browser tabs and windows (contexts), allowing navigation,
	reloading, closing, screenshotting, and DOM tree inspection.
	"""
	
	def __init__(
			self,
			selenium_browsing_context: legacyBrowsingContext,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> None:
		"""
		Initializes the BrowsingContext wrapper.

		Args:
			selenium_browsing_context (legacyBrowsingContext): The legacy Selenium instance to wrap.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.
		"""
		
		UnifiedBrowsingContext.__init__(self, selenium_browsing_context=selenium_browsing_context)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def activate(self, context: str) -> Any:
		return await self.sync_to_trio(sync_function=self._activate_impl)(context=context)
	
	async def add_event_handler(
			self,
			event: str,
			callback: Callable,
			contexts: Optional[List[str]] = None,
	) -> int:
		return await self.sync_to_trio(sync_function=self._add_event_handler_impl)(event=event, callback=callback, contexts=contexts)
	
	async def capture_screenshot(
			self,
			context: str,
			origin: str = "viewport",
			format: Optional[Dict] = None,
			clip: Optional[Dict] = None,
	) -> str:
		return await self.sync_to_trio(sync_function=self._capture_screenshot_impl)(context=context, origin=origin, format=format, clip=clip)
	
	async def clear_event_handlers(self) -> None:
		await self.sync_to_trio(sync_function=self._clear_event_handlers_impl)()
	
	async def close(self, context: str, prompt_unload: bool = False) -> None:
		await self.sync_to_trio(sync_function=self._close_impl)(context=context, prompt_unload=prompt_unload)
	
	async def create(
			self,
			type: str,
			reference_context: Optional[str] = None,
			background: bool = False,
			user_context: Optional[str] = None,
	) -> str:
		return await self.sync_to_trio(sync_function=self._create_impl)(
				type=type,
				reference_context=reference_context,
				background=background,
				user_context=user_context
		)
	
	@classmethod
	def from_legacy(
			cls,
			legacy_object: BROWSING_CONTEXT_TYPEHINT,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> Self:
		"""
		Creates an instance from a legacy Selenium BrowsingContext object.

		This factory method is used to wrap an existing Selenium BrowsingContext
		instance into the new interface.

		Args:
			legacy_object (BROWSING_CONTEXT_TYPEHINT): The legacy Selenium BrowsingContext instance or its wrapper.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.

		Returns:
			Self: A new instance of a class implementing BrowsingContext.
		"""
		
		legacy_browsing_context_obj = get_legacy_instance(instance=legacy_object)
		
		if not isinstance(legacy_browsing_context_obj, legacyBrowsingContext):
			raise CannotConvertTypeError(from_=legacyBrowsingContext, to_=legacy_object)
		
		return cls(
				selenium_browsing_context=legacy_browsing_context_obj,
				lock=lock,
				limiter=limiter
		)
	
	async def get_tree(self, max_depth: Optional[int] = None, root: Optional[str] = None) -> List[BrowsingContextInfo]:
		return await self.sync_to_trio(sync_function=self._get_tree_impl)(max_depth=max_depth, root=root)
	
	async def handle_user_prompt(
			self,
			context: str,
			accept: Optional[bool] = None,
			user_text: Optional[str] = None,
	) -> None:
		await self.sync_to_trio(sync_function=self._handle_user_prompt_impl)(context=context, accept=accept, user_text=user_text)
	
	@property
	def legacy(self) -> legacyBrowsingContext:
		return self._legacy_impl
	
	async def locate_nodes(
			self,
			context: str,
			locator: Dict,
			max_node_count: Optional[int] = None,
			serialization_options: Optional[Dict] = None,
			start_nodes: Optional[List[Dict]] = None,
	) -> List[Dict]:
		return await self.sync_to_trio(sync_function=self._locate_nodes_impl)(
				context=context,
				locator=locator,
				max_node_count=max_node_count,
				serialization_options=serialization_options,
				start_nodes=start_nodes
		)
	
	async def navigate(self, context: str, url: str, wait: Optional[str] = None) -> Dict:
		return await self.sync_to_trio(sync_function=self._navigate_impl)(context=context, url=url, wait=wait)
	
	async def print(
			self,
			context: str,
			background: bool = False,
			margin: Optional[Dict] = None,
			orientation: str = "portrait",
			page: Optional[Dict] = None,
			page_ranges: Optional[List[Union[int, str]]] = None,
			scale: float = 1.0,
			shrink_to_fit: bool = True,
	) -> str:
		return await self.sync_to_trio(sync_function=self._print_impl)(
				context=context,
				background=background,
				margin=margin,
				orientation=orientation,
				page=page,
				page_ranges=page_ranges,
				scale=scale,
				shrink_to_fit=shrink_to_fit
		)
	
	async def reload(
			self,
			context: str,
			ignore_cache: Optional[bool] = None,
			wait: Optional[str] = None,
	) -> Dict:
		return await self.sync_to_trio(sync_function=self._reload_impl)(context=context, ignore_cache=ignore_cache, wait=wait)
	
	async def remove_event_handler(self, event: str, callback_id: int) -> None:
		await self.sync_to_trio(sync_function=self._remove_event_handler_impl)(event=event, callback_id=callback_id)
	
	async def set_viewport(
			self,
			context: Optional[str] = None,
			viewport: Optional[Dict] = None,
			device_pixel_ratio: Optional[float] = None,
			user_contexts: Optional[List[str]] = None,
	) -> None:
		await self.sync_to_trio(sync_function=self._set_viewport_impl)(
				context=context,
				viewport=viewport,
				device_pixel_ratio=device_pixel_ratio,
				user_contexts=user_contexts
		)
	
	async def traverse_history(self, context: str, delta: int) -> Dict:
		return await self.sync_to_trio(sync_function=self._traverse_history_impl)(context=context, delta=delta)
