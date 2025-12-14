from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional
)
from osn_selenium.abstract.executors.cdp.overlay import (
	AbstractOverlayCDPExecutor
)


class OverlayCDPExecutor(AbstractOverlayCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def disable(self) -> None:
		return self._execute_function("Overlay.disable", locals())
	
	def enable(self) -> None:
		return self._execute_function("Overlay.enable", locals())
	
	def get_grid_highlight_objects_for_test(self, node_ids: List[int]) -> dict:
		return self._execute_function("Overlay.getGridHighlightObjectsForTest", locals())
	
	def get_highlight_object_for_test(
			self,
			node_id: int,
			include_distance: Optional[bool] = None,
			include_style: Optional[bool] = None,
			color_format: Optional[str] = None,
			show_accessibility_info: Optional[bool] = None
	) -> dict:
		return self._execute_function("Overlay.getHighlightObjectForTest", locals())
	
	def get_source_order_highlight_object_for_test(self, node_id: int) -> dict:
		return self._execute_function("Overlay.getSourceOrderHighlightObjectForTest", locals())
	
	def hide_highlight(self) -> None:
		return self._execute_function("Overlay.hideHighlight", locals())
	
	def highlight_frame(
			self,
			frame_id: str,
			content_color: Optional[Any] = None,
			content_outline_color: Optional[Any] = None
	) -> None:
		return self._execute_function("Overlay.highlightFrame", locals())
	
	def highlight_node(
			self,
			highlight_config: Any,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None,
			selector: Optional[str] = None
	) -> None:
		return self._execute_function("Overlay.highlightNode", locals())
	
	def highlight_quad(
			self,
			quad: List[Any],
			color: Optional[Any] = None,
			outline_color: Optional[Any] = None
	) -> None:
		return self._execute_function("Overlay.highlightQuad", locals())
	
	def highlight_rect(
			self,
			x: int,
			y: int,
			width: int,
			height: int,
			color: Optional[Any] = None,
			outline_color: Optional[Any] = None
	) -> None:
		return self._execute_function("Overlay.highlightRect", locals())
	
	def highlight_source_order(
			self,
			source_order_config: Any,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None
	) -> None:
		return self._execute_function("Overlay.highlightSourceOrder", locals())
	
	def set_inspect_mode(self, mode: str, highlight_config: Optional[Any] = None) -> None:
		return self._execute_function("Overlay.setInspectMode", locals())
	
	def set_paused_in_debugger_message(self, message: Optional[str] = None) -> None:
		return self._execute_function("Overlay.setPausedInDebuggerMessage", locals())
	
	def set_show_ad_highlights(self, show: bool) -> None:
		return self._execute_function("Overlay.setShowAdHighlights", locals())
	
	def set_show_container_query_overlays(self, container_query_highlight_configs: List[Any]) -> None:
		return self._execute_function("Overlay.setShowContainerQueryOverlays", locals())
	
	def set_show_debug_borders(self, show: bool) -> None:
		return self._execute_function("Overlay.setShowDebugBorders", locals())
	
	def set_show_flex_overlays(self, flex_node_highlight_configs: List[Any]) -> None:
		return self._execute_function("Overlay.setShowFlexOverlays", locals())
	
	def set_show_fps_counter(self, show: bool) -> None:
		return self._execute_function("Overlay.setShowFPSCounter", locals())
	
	def set_show_grid_overlays(self, grid_node_highlight_configs: List[Any]) -> None:
		return self._execute_function("Overlay.setShowGridOverlays", locals())
	
	def set_show_hinge(self, hinge_config: Optional[Any] = None) -> None:
		return self._execute_function("Overlay.setShowHinge", locals())
	
	def set_show_hit_test_borders(self, show: bool) -> None:
		return self._execute_function("Overlay.setShowHitTestBorders", locals())
	
	def set_show_isolated_elements(self, isolated_element_highlight_configs: List[Any]) -> None:
		return self._execute_function("Overlay.setShowIsolatedElements", locals())
	
	def set_show_layout_shift_regions(self, result: bool) -> None:
		return self._execute_function("Overlay.setShowLayoutShiftRegions", locals())
	
	def set_show_paint_rects(self, result: bool) -> None:
		return self._execute_function("Overlay.setShowPaintRects", locals())
	
	def set_show_scroll_bottleneck_rects(self, show: bool) -> None:
		return self._execute_function("Overlay.setShowScrollBottleneckRects", locals())
	
	def set_show_scroll_snap_overlays(self, scroll_snap_highlight_configs: List[Any]) -> None:
		return self._execute_function("Overlay.setShowScrollSnapOverlays", locals())
	
	def set_show_viewport_size_on_resize(self, show: bool) -> None:
		return self._execute_function("Overlay.setShowViewportSizeOnResize", locals())
	
	def set_show_web_vitals(self, show: bool) -> None:
		return self._execute_function("Overlay.setShowWebVitals", locals())
	
	def set_show_window_controls_overlay(self, window_controls_overlay_config: Optional[Any] = None) -> None:
		return self._execute_function("Overlay.setShowWindowControlsOverlay", locals())
