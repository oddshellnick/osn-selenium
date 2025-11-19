from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional
)


__all__ = ["UnifiedOverlayCDPExecutor"]


class UnifiedOverlayCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _disable_impl(self) -> None:
		return self._execute_function("Overlay.disable", {})
	
	def _enable_impl(self) -> None:
		return self._execute_function("Overlay.enable", {})
	
	def _get_grid_highlight_objects_for_test_impl(self, node_ids: List[int]) -> Any:
		return self._execute_function("Overlay.getGridHighlightObjectsForTest", {"node_ids": node_ids})
	
	def _get_highlight_object_for_test_impl(
			self,
			node_id: int,
			include_distance: Optional[bool] = None,
			include_style: Optional[bool] = None,
			color_format: Optional[str] = None,
			show_accessibility_info: Optional[bool] = None
	) -> Any:
		return self._execute_function(
				"Overlay.getHighlightObjectForTest",
				{
					"node_id": node_id,
					"include_distance": include_distance,
					"include_style": include_style,
					"color_format": color_format,
					"show_accessibility_info": show_accessibility_info
				}
		)
	
	def _get_source_order_highlight_object_for_test_impl(self, node_id: int) -> Any:
		return self._execute_function("Overlay.getSourceOrderHighlightObjectForTest", {"node_id": node_id})
	
	def _hide_highlight_impl(self) -> None:
		return self._execute_function("Overlay.hideHighlight", {})
	
	def _highlight_frame_impl(
			self,
			frame_id: str,
			content_color: Optional[Dict[str, Any]] = None,
			content_outline_color: Optional[Dict[str, Any]] = None
	) -> None:
		return self._execute_function(
				"Overlay.highlightFrame",
				{
					"frame_id": frame_id,
					"content_color": content_color,
					"content_outline_color": content_outline_color
				}
		)
	
	def _highlight_node_impl(
			self,
			highlight_config: Dict[str, Any],
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None,
			selector: Optional[str] = None
	) -> None:
		return self._execute_function(
				"Overlay.highlightNode",
				{
					"highlight_config": highlight_config,
					"node_id": node_id,
					"backend_node_id": backend_node_id,
					"object_id": object_id,
					"selector": selector
				}
		)
	
	def _highlight_quad_impl(
			self,
			quad: List[float],
			color: Optional[Dict[str, Any]] = None,
			outline_color: Optional[Dict[str, Any]] = None
	) -> None:
		return self._execute_function(
				"Overlay.highlightQuad",
				{"quad": quad, "color": color, "outline_color": outline_color}
		)
	
	def _highlight_rect_impl(
			self,
			x: int,
			y: int,
			width: int,
			height: int,
			color: Optional[Dict[str, Any]] = None,
			outline_color: Optional[Dict[str, Any]] = None
	) -> None:
		return self._execute_function(
				"Overlay.highlightRect",
				{
					"x": x,
					"y": y,
					"width": width,
					"height": height,
					"color": color,
					"outline_color": outline_color
				}
		)
	
	def _highlight_source_order_impl(
			self,
			source_order_config: Dict[str, Any],
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None
	) -> None:
		return self._execute_function(
				"Overlay.highlightSourceOrder",
				{
					"source_order_config": source_order_config,
					"node_id": node_id,
					"backend_node_id": backend_node_id,
					"object_id": object_id
				}
		)
	
	def _set_inspect_mode_impl(self, mode: str, highlight_config: Optional[Dict[str, Any]] = None) -> None:
		return self._execute_function(
				"Overlay.setInspectMode",
				{"mode": mode, "highlight_config": highlight_config}
		)
	
	def _set_paused_in_debugger_message_impl(self, message: Optional[str] = None) -> None:
		return self._execute_function("Overlay.setPausedInDebuggerMessage", {"message": message})
	
	def _set_show_ad_highlights_impl(self, show: bool) -> None:
		return self._execute_function("Overlay.setShowAdHighlights", {"show": show})
	
	def _set_show_container_query_overlays_impl(self, container_query_highlight_configs: List[Dict[str, Any]]) -> None:
		return self._execute_function(
				"Overlay.setShowContainerQueryOverlays",
				{"container_query_highlight_configs": container_query_highlight_configs}
		)
	
	def _set_show_debug_borders_impl(self, show: bool) -> None:
		return self._execute_function("Overlay.setShowDebugBorders", {"show": show})
	
	def _set_show_flex_overlays_impl(self, flex_node_highlight_configs: List[Dict[str, Any]]) -> None:
		return self._execute_function(
				"Overlay.setShowFlexOverlays",
				{"flex_node_highlight_configs": flex_node_highlight_configs}
		)
	
	def _set_show_fps_counter_impl(self, show: bool) -> None:
		return self._execute_function("Overlay.setShowFPSCounter", {"show": show})
	
	def _set_show_grid_overlays_impl(self, grid_node_highlight_configs: List[Dict[str, Any]]) -> None:
		return self._execute_function(
				"Overlay.setShowGridOverlays",
				{"grid_node_highlight_configs": grid_node_highlight_configs}
		)
	
	def _set_show_hinge_impl(self, hinge_config: Optional[Dict[str, Any]] = None) -> None:
		return self._execute_function("Overlay.setShowHinge", {"hinge_config": hinge_config})
	
	def _set_show_hit_test_borders_impl(self, show: bool) -> None:
		return self._execute_function("Overlay.setShowHitTestBorders", {"show": show})
	
	def _set_show_isolated_elements_impl(self, isolated_element_highlight_configs: List[Dict[str, Any]]) -> None:
		return self._execute_function(
				"Overlay.setShowIsolatedElements",
				{
					"isolated_element_highlight_configs": isolated_element_highlight_configs
				}
		)
	
	def _set_show_layout_shift_regions_impl(self, result: bool) -> None:
		return self._execute_function("Overlay.setShowLayoutShiftRegions", {"result": result})
	
	def _set_show_paint_rects_impl(self, result: bool) -> None:
		return self._execute_function("Overlay.setShowPaintRects", {"result": result})
	
	def _set_show_scroll_bottleneck_rects_impl(self, show: bool) -> None:
		return self._execute_function("Overlay.setShowScrollBottleneckRects", {"show": show})
	
	def _set_show_scroll_snap_overlays_impl(self, scroll_snap_highlight_configs: List[Dict[str, Any]]) -> None:
		return self._execute_function(
				"Overlay.setShowScrollSnapOverlays",
				{"scroll_snap_highlight_configs": scroll_snap_highlight_configs}
		)
	
	def _set_show_viewport_size_on_resize_impl(self, show: bool) -> None:
		return self._execute_function("Overlay.setShowViewportSizeOnResize", {"show": show})
	
	def _set_show_web_vitals_impl(self, show: bool) -> None:
		return self._execute_function("Overlay.setShowWebVitals", {"show": show})
	
	def _set_show_window_controls_overlay_impl(self, window_controls_overlay_config: Optional[Dict[str, Any]] = None) -> None:
		return self._execute_function(
				"Overlay.setShowWindowControlsOverlay",
				{"window_controls_overlay_config": window_controls_overlay_config}
		)
