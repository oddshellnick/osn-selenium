from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional
)
from osn_selenium.executors.unified.cdp.overlay import (
	UnifiedOverlayCDPExecutor
)
from osn_selenium.abstract.executors.cdp.overlay import (
	AbstractOverlayCDPExecutor
)


__all__ = ["OverlayCDPExecutor"]


class OverlayCDPExecutor(UnifiedOverlayCDPExecutor, AbstractOverlayCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedOverlayCDPExecutor.__init__(self, execute_function=execute_function)
	
	def disable(self) -> None:
		return self._disable_impl()
	
	def enable(self) -> None:
		return self._enable_impl()
	
	def get_grid_highlight_objects_for_test(self, node_ids: List[int]) -> Any:
		return self._get_grid_highlight_objects_for_test_impl(node_ids=node_ids)
	
	def get_highlight_object_for_test(
			self,
			node_id: int,
			include_distance: Optional[bool] = None,
			include_style: Optional[bool] = None,
			color_format: Optional[str] = None,
			show_accessibility_info: Optional[bool] = None
	) -> Any:
		return self._get_highlight_object_for_test_impl(
				node_id=node_id,
				include_distance=include_distance,
				include_style=include_style,
				color_format=color_format,
				show_accessibility_info=show_accessibility_info
		)
	
	def get_source_order_highlight_object_for_test(self, node_id: int) -> Any:
		return self._get_source_order_highlight_object_for_test_impl(node_id=node_id)
	
	def hide_highlight(self) -> None:
		return self._hide_highlight_impl()
	
	def highlight_frame(
			self,
			frame_id: str,
			content_color: Optional[Dict[str, Any]] = None,
			content_outline_color: Optional[Dict[str, Any]] = None
	) -> None:
		return self._highlight_frame_impl(
				frame_id=frame_id,
				content_color=content_color,
				content_outline_color=content_outline_color
		)
	
	def highlight_node(
			self,
			highlight_config: Dict[str, Any],
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None,
			selector: Optional[str] = None
	) -> None:
		return self._highlight_node_impl(
				highlight_config=highlight_config,
				node_id=node_id,
				backend_node_id=backend_node_id,
				object_id=object_id,
				selector=selector
		)
	
	def highlight_quad(
			self,
			quad: List[float],
			color: Optional[Dict[str, Any]] = None,
			outline_color: Optional[Dict[str, Any]] = None
	) -> None:
		return self._highlight_quad_impl(quad=quad, color=color, outline_color=outline_color)
	
	def highlight_rect(
			self,
			x: int,
			y: int,
			width: int,
			height: int,
			color: Optional[Dict[str, Any]] = None,
			outline_color: Optional[Dict[str, Any]] = None
	) -> None:
		return self._highlight_rect_impl(
				x=x,
				y=y,
				width=width,
				height=height,
				color=color,
				outline_color=outline_color
		)
	
	def highlight_source_order(
			self,
			source_order_config: Dict[str, Any],
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None
	) -> None:
		return self._highlight_source_order_impl(
				source_order_config=source_order_config,
				node_id=node_id,
				backend_node_id=backend_node_id,
				object_id=object_id
		)
	
	def set_inspect_mode(self, mode: str, highlight_config: Optional[Dict[str, Any]] = None) -> None:
		return self._set_inspect_mode_impl(mode=mode, highlight_config=highlight_config)
	
	def set_paused_in_debugger_message(self, message: Optional[str] = None) -> None:
		return self._set_paused_in_debugger_message_impl(message=message)
	
	def set_show_ad_highlights(self, show: bool) -> None:
		return self._set_show_ad_highlights_impl(show=show)
	
	def set_show_container_query_overlays(self, container_query_highlight_configs: List[Dict[str, Any]]) -> None:
		return self._set_show_container_query_overlays_impl(container_query_highlight_configs=container_query_highlight_configs)
	
	def set_show_debug_borders(self, show: bool) -> None:
		return self._set_show_debug_borders_impl(show=show)
	
	def set_show_flex_overlays(self, flex_node_highlight_configs: List[Dict[str, Any]]) -> None:
		return self._set_show_flex_overlays_impl(flex_node_highlight_configs=flex_node_highlight_configs)
	
	def set_show_fps_counter(self, show: bool) -> None:
		return self._set_show_fps_counter_impl(show=show)
	
	def set_show_grid_overlays(self, grid_node_highlight_configs: List[Dict[str, Any]]) -> None:
		return self._set_show_grid_overlays_impl(grid_node_highlight_configs=grid_node_highlight_configs)
	
	def set_show_hinge(self, hinge_config: Optional[Dict[str, Any]] = None) -> None:
		return self._set_show_hinge_impl(hinge_config=hinge_config)
	
	def set_show_hit_test_borders(self, show: bool) -> None:
		return self._set_show_hit_test_borders_impl(show=show)
	
	def set_show_isolated_elements(self, isolated_element_highlight_configs: List[Dict[str, Any]]) -> None:
		return self._set_show_isolated_elements_impl(isolated_element_highlight_configs=isolated_element_highlight_configs)
	
	def set_show_layout_shift_regions(self, result: bool) -> None:
		return self._set_show_layout_shift_regions_impl(result=result)
	
	def set_show_paint_rects(self, result: bool) -> None:
		return self._set_show_paint_rects_impl(result=result)
	
	def set_show_scroll_bottleneck_rects(self, show: bool) -> None:
		return self._set_show_scroll_bottleneck_rects_impl(show=show)
	
	def set_show_scroll_snap_overlays(self, scroll_snap_highlight_configs: List[Dict[str, Any]]) -> None:
		return self._set_show_scroll_snap_overlays_impl(scroll_snap_highlight_configs=scroll_snap_highlight_configs)
	
	def set_show_viewport_size_on_resize(self, show: bool) -> None:
		return self._set_show_viewport_size_on_resize_impl(show=show)
	
	def set_show_web_vitals(self, show: bool) -> None:
		return self._set_show_web_vitals_impl(show=show)
	
	def set_show_window_controls_overlay(self, window_controls_overlay_config: Optional[Dict[str, Any]] = None) -> None:
		return self._set_show_window_controls_overlay_impl(window_controls_overlay_config=window_controls_overlay_config)
