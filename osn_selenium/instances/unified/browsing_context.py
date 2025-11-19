from osn_selenium.exceptions.instance import NotExpectedTypeError
from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Union
)
from selenium.webdriver.common.bidi.browsing_context import (
	BrowsingContext as legacyBrowsingContext,
	BrowsingContextInfo
)


__all__ = ["UnifiedBrowsingContext"]


class UnifiedBrowsingContext:
	def __init__(self, selenium_browsing_context: legacyBrowsingContext):
		if not isinstance(selenium_browsing_context, legacyBrowsingContext):
			raise NotExpectedTypeError(
					expected_type=legacyBrowsingContext,
					received_instance=selenium_browsing_context
			)
		
		self._selenium_browsing_context = selenium_browsing_context
	
	def _activate_impl(self, context: str) -> Any:
		return self._legacy_impl.activate(context)
	
	def _add_event_handler_impl(
			self,
			event: str,
			callback: Callable,
			contexts: Optional[List[str]] = None,
	) -> int:
		return self._legacy_impl.add_event_handler(event=event, callback=callback, contexts=contexts)
	
	def _capture_screenshot_impl(
			self,
			context: str,
			origin: str = "viewport",
			format: Optional[Dict] = None,
			clip: Optional[Dict] = None,
	) -> str:
		return self._legacy_impl.capture_screenshot(context=context, origin=origin, format=format, clip=clip)
	
	def _clear_event_handlers_impl(self) -> None:
		self._legacy_impl.clear_event_handlers()
	
	def _close_impl(self, context: str, prompt_unload: bool = False) -> None:
		self._legacy_impl.close(context=context, prompt_unload=prompt_unload)
	
	def _create_impl(
			self,
			type: str,
			reference_context: Optional[str] = None,
			background: bool = False,
			user_context: Optional[str] = None,
	) -> str:
		return self._legacy_impl.create(
				type=type,
				reference_context=reference_context,
				background=background,
				user_context=user_context
		)
	
	def _get_tree_impl(self, max_depth: Optional[int] = None, root: Optional[str] = None) -> List[BrowsingContextInfo]:
		return self._legacy_impl.get_tree(max_depth=max_depth, root=root)
	
	def _handle_user_prompt_impl(
			self,
			context: str,
			accept: Optional[bool] = None,
			user_text: Optional[str] = None,
	) -> None:
		self._legacy_impl.handle_user_prompt(context=context, accept=accept, user_text=user_text)
	
	@property
	def _legacy_impl(self) -> legacyBrowsingContext:
		return self._selenium_browsing_context
	
	def _locate_nodes_impl(
			self,
			context: str,
			locator: Dict,
			max_node_count: Optional[int] = None,
			serialization_options: Optional[Dict] = None,
			start_nodes: Optional[List[Dict]] = None,
	) -> List[Dict]:
		return self._legacy_impl.locate_nodes(
				context=context,
				locator=locator,
				max_node_count=max_node_count,
				serialization_options=serialization_options,
				start_nodes=start_nodes
		)
	
	def _navigate_impl(self, context: str, url: str, wait: Optional[str] = None) -> Dict:
		return self._legacy_impl.navigate(context=context, url=url, wait=wait)
	
	def _print_impl(
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
		return self._legacy_impl.print(
				context=context,
				background=background,
				margin=margin,
				orientation=orientation,
				page=page,
				page_ranges=page_ranges,
				scale=scale,
				shrink_to_fit=shrink_to_fit
		)
	
	def _reload_impl(
			self,
			context: str,
			ignore_cache: Optional[bool] = None,
			wait: Optional[str] = None,
	) -> Dict:
		return self._legacy_impl.reload(context=context, ignore_cache=ignore_cache, wait=wait)
	
	def _remove_event_handler_impl(self, event: str, callback_id: int) -> None:
		self._legacy_impl.remove_event_handler(event=event, callback_id=callback_id)
	
	def _set_viewport_impl(
			self,
			context: Optional[str] = None,
			viewport: Optional[Dict] = None,
			device_pixel_ratio: Optional[float] = None,
			user_contexts: Optional[List[str]] = None,
	) -> None:
		self._legacy_impl.set_viewport(
				context=context,
				viewport=viewport,
				device_pixel_ratio=device_pixel_ratio,
				user_contexts=user_contexts
		)
	
	def _traverse_history_impl(self, context: str, delta: int) -> Dict:
		return self._legacy_impl.traverse_history(context=context, delta=delta)
