from abc import ABC, abstractmethod
from typing import (
	Any,
	Dict,
	List,
	Optional,
	Tuple
)


__all__ = ["AbstractDomCDPExecutor"]


class AbstractDomCDPExecutor(ABC):
	@abstractmethod
	def collect_class_names_from_subtree(self, node_id: int) -> List[str]:
		...
	
	@abstractmethod
	def copy_to(
			self,
			node_id: int,
			target_node_id: int,
			insert_before_node_id: Optional[int] = None
	) -> int:
		...
	
	@abstractmethod
	def describe_node(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None,
			depth: Optional[int] = None,
			pierce: Optional[bool] = None
	) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def discard_search_results(self, search_id: str) -> None:
		...
	
	@abstractmethod
	def enable(self, include_whitespace: Optional[str] = None) -> None:
		...
	
	@abstractmethod
	def focus(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None
	) -> None:
		...
	
	@abstractmethod
	def force_show_popover(self, node_id: int, enable: bool) -> List[int]:
		...
	
	@abstractmethod
	def get_anchor_element(self, node_id: int, anchor_specifier: Optional[str] = None) -> int:
		...
	
	@abstractmethod
	def get_attributes(self, node_id: int) -> List[str]:
		...
	
	@abstractmethod
	def get_box_model(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None
	) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def get_container_for_node(
			self,
			node_id: int,
			container_name: Optional[str] = None,
			physical_axes: Optional[str] = None,
			logical_axes: Optional[str] = None,
			queries_scroll_state: Optional[bool] = None,
			queries_anchored: Optional[bool] = None
	) -> Optional[int]:
		...
	
	@abstractmethod
	def get_content_quads(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None
	) -> List[List[float]]:
		...
	
	@abstractmethod
	def get_detached_dom_nodes(self) -> List[Dict[str, Any]]:
		...
	
	@abstractmethod
	def get_document(self, depth: Optional[int] = None, pierce: Optional[bool] = None) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def get_element_by_relation(self, node_id: int, relation: str) -> int:
		...
	
	@abstractmethod
	def get_file_info(self, object_id: str) -> str:
		...
	
	@abstractmethod
	def get_flattened_document(self, depth: Optional[int] = None, pierce: Optional[bool] = None) -> List[Dict[str, Any]]:
		...
	
	@abstractmethod
	def get_frame_owner(self, frame_id: str) -> Tuple[int, Optional[int]]:
		...
	
	@abstractmethod
	def get_node_for_location(
			self,
			x: int,
			y: int,
			include_user_agent_shadow_dom: Optional[bool] = None,
			ignore_pointer_events_none: Optional[bool] = None
	) -> Tuple[int, str, Optional[int]]:
		...
	
	@abstractmethod
	def get_node_stack_traces(self, node_id: int) -> Optional[Dict[str, Any]]:
		...
	
	@abstractmethod
	def get_nodes_for_subtree_by_style(
			self,
			node_id: int,
			computed_styles: List[Dict[str, Any]],
			pierce: Optional[bool] = None
	) -> List[int]:
		...
	
	@abstractmethod
	def get_outer_html(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None,
			include_shadow_dom: Optional[bool] = None
	) -> str:
		...
	
	@abstractmethod
	def get_querying_descendants_for_container(self, node_id: int) -> List[int]:
		...
	
	@abstractmethod
	def get_relayout_boundary(self, node_id: int) -> int:
		...
	
	@abstractmethod
	def get_search_results(self, search_id: str, from_index: int, to_index: int) -> List[int]:
		...
	
	@abstractmethod
	def get_top_layer_elements(self) -> List[int]:
		...
	
	@abstractmethod
	def hide_highlight(self) -> None:
		...
	
	@abstractmethod
	def highlight_node(self) -> None:
		...
	
	@abstractmethod
	def highlight_rect(self) -> None:
		...
	
	@abstractmethod
	def mark_undoable_state(self) -> None:
		...
	
	@abstractmethod
	def move_to(
			self,
			node_id: int,
			target_node_id: int,
			insert_before_node_id: Optional[int] = None
	) -> int:
		...
	
	@abstractmethod
	def perform_search(self, query: str, include_user_agent_shadow_dom: Optional[bool] = None) -> Tuple[str, int]:
		...
	
	@abstractmethod
	def push_node_by_path_to_frontend(self, path: str) -> int:
		...
	
	@abstractmethod
	def push_nodes_by_backend_ids_to_frontend(self, backend_node_ids: List[int]) -> List[int]:
		...
	
	@abstractmethod
	def query_selector(self, node_id: int, selector: str) -> int:
		...
	
	@abstractmethod
	def query_selector_all(self, node_id: int, selector: str) -> List[int]:
		...
	
	@abstractmethod
	def redo(self) -> None:
		...
	
	@abstractmethod
	def remove_attribute(self, node_id: int, name: str) -> None:
		...
	
	@abstractmethod
	def remove_node(self, node_id: int) -> None:
		...
	
	@abstractmethod
	def request_child_nodes(
			self,
			node_id: int,
			depth: Optional[int] = None,
			pierce: Optional[bool] = None
	) -> None:
		...
	
	@abstractmethod
	def request_node(self, object_id: str) -> int:
		...
	
	@abstractmethod
	def resolve_node(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_group: Optional[str] = None,
			execution_context_id: Optional[int] = None
	) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def scroll_into_view_if_needed(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None,
			rect: Optional[Dict[str, Any]] = None
	) -> None:
		...
	
	@abstractmethod
	def set_attribute_value(self, node_id: int, name: str, value: str) -> None:
		...
	
	@abstractmethod
	def set_attributes_as_text(self, node_id: int, text: str, name: Optional[str] = None) -> None:
		...
	
	@abstractmethod
	def set_file_input_files(
			self,
			files: List[str],
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None
	) -> None:
		...
	
	@abstractmethod
	def set_inspected_node(self, node_id: int) -> None:
		...
	
	@abstractmethod
	def set_node_name(self, node_id: int, name: str) -> int:
		...
	
	@abstractmethod
	def set_node_stack_traces_enabled(self, enable: bool) -> None:
		...
	
	@abstractmethod
	def set_node_value(self, node_id: int, value: str) -> None:
		...
	
	@abstractmethod
	def set_outer_html(self, node_id: int, outer_html: str) -> None:
		...
	
	@abstractmethod
	def undo(self) -> None:
		...
