from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)


__all__ = ["UnifiedDomSnapshotCDPExecutor"]


class UnifiedDomSnapshotCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _capture_snapshot_impl(
			self,
			computed_styles: List[str],
			include_paint_order: Optional[bool] = None,
			include_dom_rects: Optional[bool] = None,
			include_blended_background_colors: Optional[bool] = None,
			include_text_color_opacities: Optional[bool] = None
	) -> Tuple[List[Dict[str, Any]], List[str]]:
		return self._execute_function(
				"DOMSnapshot.captureSnapshot",
				{
					"computed_styles": computed_styles,
					"include_paint_order": include_paint_order,
					"include_dom_rects": include_dom_rects,
					"include_blended_background_colors": include_blended_background_colors,
					"include_text_color_opacities": include_text_color_opacities
				}
		)
	
	def _disable_impl(self) -> None:
		return self._execute_function("DOMSnapshot.disable", {})
	
	def _enable_impl(self) -> None:
		return self._execute_function("DOMSnapshot.enable", {})
	
	def _get_snapshot_impl(
			self,
			computed_style_whitelist: List[str],
			include_event_listeners: Optional[bool] = None,
			include_paint_order: Optional[bool] = None,
			include_user_agent_shadow_tree: Optional[bool] = None
	) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
		return self._execute_function(
				"DOMSnapshot.getSnapshot",
				{
					"computed_style_whitelist": computed_style_whitelist,
					"include_event_listeners": include_event_listeners,
					"include_paint_order": include_paint_order,
					"include_user_agent_shadow_tree": include_user_agent_shadow_tree
				}
		)
