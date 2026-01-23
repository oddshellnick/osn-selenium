from abc import ABC, abstractmethod
from typing import (
	Any,
	Dict,
	List,
	Optional
)


__all__ = ["AbstractOverlayCDPExecutor"]


class AbstractOverlayCDPExecutor(ABC):
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def enable(self) -> None:
		...
	
	@abstractmethod
	def get_grid_highlight_objects_for_test(self, node_ids: List[int]) -> Any:
		...
	
	@abstractmethod
	def get_highlight_object_for_test(
			self,
			node_id: int,
			include_distance: Optional[bool] = None,
			include_style: Optional[bool] = None,
			color_format: Optional[str] = None,
			show_accessibility_info: Optional[bool] = None
	) -> Any:
		...
	
	@abstractmethod
	def get_source_order_highlight_object_for_test(self, node_id: int) -> Any:
		...
	
	@abstractmethod
	def hide_highlight(self) -> None:
		...
	
	@abstractmethod
	def highlight_frame(
			self,
			frame_id: str,
			content_color: Optional[Dict[str, Any]] = None,
			content_outline_color: Optional[Dict[str, Any]] = None
	) -> None:
		...
	
	@abstractmethod
	def highlight_node(
			self,
			highlight_config: Dict[str, Any],
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None,
			selector: Optional[str] = None
	) -> None:
		...
	
	@abstractmethod
	def highlight_quad(
			self,
			quad: List[float],
			color: Optional[Dict[str, Any]] = None,
			outline_color: Optional[Dict[str, Any]] = None
	) -> None:
		...
	
	@abstractmethod
	def highlight_rect(
			self,
			x: int,
			y: int,
			width: int,
			height: int,
			color: Optional[Dict[str, Any]] = None,
			outline_color: Optional[Dict[str, Any]] = None
	) -> None:
		...
	
	@abstractmethod
	def highlight_source_order(
			self,
			source_order_config: Dict[str, Any],
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None
	) -> None:
		...
	
	@abstractmethod
	def set_inspect_mode(self, mode: str, highlight_config: Optional[Dict[str, Any]] = None) -> None:
		...
	
	@abstractmethod
	def set_paused_in_debugger_message(self, message: Optional[str] = None) -> None:
		...
	
	@abstractmethod
	def set_show_ad_highlights(self, show: bool) -> None:
		...
	
	@abstractmethod
	def set_show_container_query_overlays(self, container_query_highlight_configs: List[Dict[str, Any]]) -> None:
		...
	
	@abstractmethod
	def set_show_debug_borders(self, show: bool) -> None:
		...
	
	@abstractmethod
	def set_show_flex_overlays(self, flex_node_highlight_configs: List[Dict[str, Any]]) -> None:
		...
	
	@abstractmethod
	def set_show_fps_counter(self, show: bool) -> None:
		...
	
	@abstractmethod
	def set_show_grid_overlays(self, grid_node_highlight_configs: List[Dict[str, Any]]) -> None:
		...
	
	@abstractmethod
	def set_show_hinge(self, hinge_config: Optional[Dict[str, Any]] = None) -> None:
		...
	
	@abstractmethod
	def set_show_hit_test_borders(self, show: bool) -> None:
		...
	
	@abstractmethod
	def set_show_isolated_elements(self, isolated_element_highlight_configs: List[Dict[str, Any]]) -> None:
		...
	
	@abstractmethod
	def set_show_layout_shift_regions(self, result: bool) -> None:
		...
	
	@abstractmethod
	def set_show_paint_rects(self, result: bool) -> None:
		...
	
	@abstractmethod
	def set_show_scroll_bottleneck_rects(self, show: bool) -> None:
		...
	
	@abstractmethod
	def set_show_scroll_snap_overlays(self, scroll_snap_highlight_configs: List[Dict[str, Any]]) -> None:
		...
	
	@abstractmethod
	def set_show_viewport_size_on_resize(self, show: bool) -> None:
		...
	
	@abstractmethod
	def set_show_web_vitals(self, show: bool) -> None:
		...
	
	@abstractmethod
	def set_show_window_controls_overlay(self, window_controls_overlay_config: Optional[Dict[str, Any]] = None) -> None:
		...
