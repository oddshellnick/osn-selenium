import trio
from osn_selenium.trio_base_mixin import _TrioThreadMixin
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.instances.types import (
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
from osn_selenium.instances.errors import (
	ExpectedTypeError,
	TypesConvertError
)
from osn_selenium.abstract.instances.browsing_context import (
	AbstractBrowsingContext
)
from selenium.webdriver.common.bidi.browsing_context import (
	BrowsingContext as legacyBrowsingContext,
	BrowsingContextInfo
)


class BrowsingContext(_TrioThreadMixin, AbstractBrowsingContext):
	def __init__(
			self,
			selenium_browsing_context: legacyBrowsingContext,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> None:
		super().__init__(lock=lock, limiter=limiter)
		
		if not isinstance(selenium_browsing_context, legacyBrowsingContext):
			raise ExpectedTypeError(
					expected_class=legacyBrowsingContext,
					received_instance=selenium_browsing_context
			)
		
		self._selenium_browsing_context = selenium_browsing_context
	
	async def activate(self, context: str) -> Any:
		return await self._wrap_to_trio(self.legacy.activate, context)
	
	async def add_event_handler(
			self,
			event: str,
			callback: Callable,
			contexts: Optional[List[str]] = None,
	) -> int:
		return await self._wrap_to_trio(
				self.legacy.add_event_handler,
				event=event,
				callback=callback,
				contexts=contexts
		)
	
	async def capture_screenshot(
			self,
			context: str,
			origin: str = 'viewport',
			format: Optional[Dict] = None,
			clip: Optional[Dict] = None,
	) -> str:
		return await self._wrap_to_trio(
				self.legacy.capture_screenshot,
				context=context,
				origin=origin,
				format=format,
				clip=clip
		)
	
	async def clear_event_handlers(self) -> None:
		await self._wrap_to_trio(self.legacy.clear_event_handlers)
	
	async def close(self, context: str, prompt_unload: bool = False) -> None:
		await self._wrap_to_trio(self.legacy.close, context=context, prompt_unload=prompt_unload)
	
	async def create(
			self,
			type: str,
			reference_context: Optional[str] = None,
			background: bool = False,
			user_context: Optional[str] = None,
	) -> str:
		return await self._wrap_to_trio(
				self.legacy.create,
				type=type,
				reference_context=reference_context,
				background=background,
				user_context=user_context
		)
	
	@classmethod
	def from_legacy(
			cls,
			selenium_browsing_context: BROWSING_CONTEXT_TYPEHINT,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> Self:
		"""
		Creates an instance from a legacy Selenium BrowsingContext object.

		This factory method is used to wrap an existing Selenium BrowsingContext
		instance into the new interface.

		Args:
			selenium_browsing_context (BROWSING_CONTEXT_TYPEHINT): The legacy Selenium BrowsingContext instance or its wrapper.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.

		Returns:
			Self: A new instance of a class implementing BrowsingContext.
		"""
		
		legacy_browsing_context_obj = get_legacy_instance(selenium_browsing_context)
		
		if not isinstance(legacy_browsing_context_obj, legacyBrowsingContext):
			raise TypesConvertError(from_=legacyBrowsingContext, to_=selenium_browsing_context)
		
		return cls(
				selenium_browsing_context=legacy_browsing_context_obj,
				lock=lock,
				limiter=limiter
		)
	
	async def get_tree(self, max_depth: Optional[int] = None, root: Optional[str] = None) -> List[BrowsingContextInfo]:
		return await self._wrap_to_trio(self.legacy.get_tree, max_depth=max_depth, root=root)
	
	async def handle_user_prompt(
			self,
			context: str,
			accept: Optional[bool] = None,
			user_text: Optional[str] = None,
	) -> None:
		await self._wrap_to_trio(
				self.legacy.handle_user_prompt,
				context=context,
				accept=accept,
				user_text=user_text
		)
	
	@property
	def legacy(self) -> legacyBrowsingContext:
		return self._selenium_browsing_context
	
	async def locate_nodes(
			self,
			context: str,
			locator: Dict,
			max_node_count: Optional[int] = None,
			serialization_options: Optional[Dict] = None,
			start_nodes: Optional[List[Dict]] = None,
	) -> List[Dict]:
		return await self._wrap_to_trio(
				self.legacy.locate_nodes,
				context=context,
				locator=locator,
				max_node_count=max_node_count,
				serialization_options=serialization_options,
				start_nodes=start_nodes
		)
	
	async def navigate(self, context: str, url: str, wait: Optional[str] = None) -> Dict:
		return await self._wrap_to_trio(self.legacy.navigate, context=context, url=url, wait=wait)
	
	async def print(
			self,
			context: str,
			background: bool = False,
			margin: Optional[Dict] = None,
			orientation: str = 'portrait',
			page: Optional[Dict] = None,
			page_ranges: Optional[List[Union[int, str]]] = None,
			scale: float = 1.0,
			shrink_to_fit: bool = True,
	) -> str:
		return await self._wrap_to_trio(
				self.legacy.print,
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
		return await self._wrap_to_trio(
				self.legacy.reload,
				context=context,
				ignore_cache=ignore_cache,
				wait=wait
		)
	
	async def remove_event_handler(self, event: str, callback_id: int) -> None:
		await self._wrap_to_trio(self.legacy.remove_event_handler, event=event, callback_id=callback_id)
	
	async def set_viewport(
			self,
			context: Optional[str] = None,
			viewport: Optional[Dict] = None,
			device_pixel_ratio: Optional[float] = None,
			user_contexts: Optional[List[str]] = None,
	) -> None:
		await self._wrap_to_trio(
				self.legacy.set_viewport,
				context=context,
				viewport=viewport,
				device_pixel_ratio=device_pixel_ratio,
				user_contexts=user_contexts
		)
	
	async def traverse_history(self, context: str, delta: int) -> Dict:
		return await self._wrap_to_trio(self.legacy.traverse_history, context=context, delta=delta)
