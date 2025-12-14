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
from osn_selenium.abstract.instances.browsing_context import (
	AbstractBrowsingContext
)
from selenium.webdriver.common.bidi.browsing_context import (
	BrowsingContext as legacyBrowsingContext,
	BrowsingContextInfo
)


class BrowsingContext(AbstractBrowsingContext):
	def __init__(self, selenium_browsing_context: legacyBrowsingContext) -> None:
		if not isinstance(selenium_browsing_context, legacyBrowsingContext):
			raise TypeError(
					f"Expected {type(legacyBrowsingContext)}, got {type(selenium_browsing_context)}"
			)
		
		self._selenium_browsing_context = selenium_browsing_context
	
	def activate(self, context: str) -> Any:
		return self.legacy.activate(context)
	
	def add_event_handler(
			self,
			event: str,
			callback: Callable,
			contexts: Optional[List[str]] = None,
	) -> int:
		return self.legacy.add_event_handler(event=event, callback=callback, contexts=contexts)
	
	def capture_screenshot(
			self,
			context: str,
			origin: str = 'viewport',
			format: Optional[Dict] = None,
			clip: Optional[Dict] = None,
	) -> str:
		return self.legacy.capture_screenshot(context=context, origin=origin, format=format, clip=clip)
	
	def clear_event_handlers(self) -> None:
		self.legacy.clear_event_handlers()
	
	def close(self, context: str, prompt_unload: bool = False) -> None:
		self.legacy.close(context=context, prompt_unload=prompt_unload)
	
	def create(
			self,
			type: str,
			reference_context: Optional[str] = None,
			background: bool = False,
			user_context: Optional[str] = None,
	) -> str:
		return self.legacy.create(
				type=type,
				reference_context=reference_context,
				background=background,
				user_context=user_context
		)
	
	@classmethod
	def from_legacy(cls, selenium_browsing_context: BROWSING_CONTEXT_TYPEHINT) -> Self:
		"""
		Creates an instance from a legacy Selenium BrowsingContext object.

		This factory method is used to wrap an existing Selenium BrowsingContext
		instance into the new interface.

		Args:
			selenium_browsing_context (BROWSING_CONTEXT_TYPEHINT): The legacy Selenium BrowsingContext instance or its wrapper.

		Returns:
			Self: A new instance of a class implementing BrowsingContext.
		"""

		legacy_browsing_context_obj = get_legacy_instance(selenium_browsing_context)
		if not isinstance(legacy_browsing_context_obj, legacyBrowsingContext):
			raise TypeError(
					f"Could not convert input to {type(legacyBrowsingContext)}: {type(selenium_browsing_context)}"
			)
		
		return cls(selenium_browsing_context=legacy_browsing_context_obj)
	
	def get_tree(self, max_depth: Optional[int] = None, root: Optional[str] = None) -> List[BrowsingContextInfo]:
		return self.legacy.get_tree(max_depth=max_depth, root=root)
	
	def handle_user_prompt(
			self,
			context: str,
			accept: Optional[bool] = None,
			user_text: Optional[str] = None,
	) -> None:
		self.legacy.handle_user_prompt(context=context, accept=accept, user_text=user_text)
	
	@property
	def legacy(self) -> legacyBrowsingContext:
		return self._selenium_browsing_context
	
	def locate_nodes(
			self,
			context: str,
			locator: Dict,
			max_node_count: Optional[int] = None,
			serialization_options: Optional[Dict] = None,
			start_nodes: Optional[List[Dict]] = None,
	) -> List[Dict]:
		return self.legacy.locate_nodes(
				context=context,
				locator=locator,
				max_node_count=max_node_count,
				serialization_options=serialization_options,
				start_nodes=start_nodes
		)
	
	def navigate(self, context: str, url: str, wait: Optional[str] = None) -> Dict:
		return self.legacy.navigate(context=context, url=url, wait=wait)
	
	def print(
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
		return self.legacy.print(
				context=context,
				background=background,
				margin=margin,
				orientation=orientation,
				page=page,
				page_ranges=page_ranges,
				scale=scale,
				shrink_to_fit=shrink_to_fit
		)
	
	def reload(
			self,
			context: str,
			ignore_cache: Optional[bool] = None,
			wait: Optional[str] = None,
	) -> Dict:
		return self.legacy.reload(context=context, ignore_cache=ignore_cache, wait=wait)
	
	def remove_event_handler(self, event: str, callback_id: int) -> None:
		self.legacy.remove_event_handler(event=event, callback_id=callback_id)
	
	def set_viewport(
			self,
			context: Optional[str] = None,
			viewport: Optional[Dict] = None,
			device_pixel_ratio: Optional[float] = None,
			user_contexts: Optional[List[str]] = None,
	) -> None:
		self.legacy.set_viewport(
				context=context,
				viewport=viewport,
				device_pixel_ratio=device_pixel_ratio,
				user_contexts=user_contexts
		)
	
	def traverse_history(self, context: str, delta: int) -> Dict:
		return self.legacy.traverse_history(context=context, delta=delta)
