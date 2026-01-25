from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.executors.unified.cdp.dom_snapshot import (
	UnifiedDomSnapshotCDPExecutor
)
from osn_selenium.abstract.executors.cdp.dom_snapshot import (
	AbstractDomSnapshotCDPExecutor
)


__all__ = ["DomSnapshotCDPExecutor"]


class DomSnapshotCDPExecutor(UnifiedDomSnapshotCDPExecutor, AbstractDomSnapshotCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedDomSnapshotCDPExecutor.__init__(self, execute_function=execute_function)
	
	def capture_snapshot(
			self,
			computed_styles: List[str],
			include_paint_order: Optional[bool] = None,
			include_dom_rects: Optional[bool] = None,
			include_blended_background_colors: Optional[bool] = None,
			include_text_color_opacities: Optional[bool] = None
	) -> Tuple[List[Dict[str, Any]], List[str]]:
		return self._capture_snapshot_impl(
				computed_styles=computed_styles,
				include_paint_order=include_paint_order,
				include_dom_rects=include_dom_rects,
				include_blended_background_colors=include_blended_background_colors,
				include_text_color_opacities=include_text_color_opacities
		)
	
	def disable(self) -> None:
		return self._disable_impl()
	
	def enable(self) -> None:
		return self._enable_impl()
	
	def get_snapshot(
			self,
			computed_style_whitelist: List[str],
			include_event_listeners: Optional[bool] = None,
			include_paint_order: Optional[bool] = None,
			include_user_agent_shadow_tree: Optional[bool] = None
	) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
		return self._get_snapshot_impl(
				computed_style_whitelist=computed_style_whitelist,
				include_event_listeners=include_event_listeners,
				include_paint_order=include_paint_order,
				include_user_agent_shadow_tree=include_user_agent_shadow_tree
		)
