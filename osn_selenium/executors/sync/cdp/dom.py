from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.abstract.executors.cdp.dom import (
	AbstractDomCDPExecutor
)


class DomCDPExecutor(AbstractDomCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def collect_class_names_from_subtree(self, node_id: int) -> List[str]:
		return self._execute_function("DOM.collectClassNamesFromSubtree", locals())
	
	def copy_to(
			self,
			node_id: int,
			target_node_id: int,
			insert_before_node_id: Optional[int] = None
	) -> int:
		return self._execute_function("DOM.copyTo", locals())
	
	def describe_node(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None,
			depth: Optional[int] = None,
			pierce: Optional[bool] = None
	) -> Any:
		return self._execute_function("DOM.describeNode", locals())
	
	def disable(self) -> None:
		return self._execute_function("DOM.disable", locals())
	
	def discard_search_results(self, search_id: str) -> None:
		return self._execute_function("DOM.discardSearchResults", locals())
	
	def enable(self, include_whitespace: Optional[str] = None) -> None:
		return self._execute_function("DOM.enable", locals())
	
	def focus(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None
	) -> None:
		return self._execute_function("DOM.focus", locals())
	
	def force_show_popover(self, node_id: int, enable: bool) -> List[int]:
		return self._execute_function("DOM.forceShowPopover", locals())
	
	def get_anchor_element(self, node_id: int, anchor_specifier: Optional[str] = None) -> int:
		return self._execute_function("DOM.getAnchorElement", locals())
	
	def get_attributes(self, node_id: int) -> List[str]:
		return self._execute_function("DOM.getAttributes", locals())
	
	def get_box_model(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None
	) -> Any:
		return self._execute_function("DOM.getBoxModel", locals())
	
	def get_container_for_node(
			self,
			node_id: int,
			container_name: Optional[str] = None,
			physical_axes: Optional[str] = None,
			logical_axes: Optional[str] = None,
			queries_scroll_state: Optional[bool] = None,
			queries_anchored: Optional[bool] = None
	) -> Optional[int]:
		return self._execute_function("DOM.getContainerForNode", locals())
	
	def get_content_quads(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None
	) -> List[List[Any]]:
		return self._execute_function("DOM.getContentQuads", locals())
	
	def get_detached_dom_nodes(self) -> List[Any]:
		return self._execute_function("DOM.getDetachedDomNodes", locals())
	
	def get_document(self, depth: Optional[int] = None, pierce: Optional[bool] = None) -> Any:
		return self._execute_function("DOM.getDocument", locals())
	
	def get_element_by_relation(self, node_id: int, relation: str) -> int:
		return self._execute_function("DOM.getElementByRelation", locals())
	
	def get_file_info(self, object_id: str) -> str:
		return self._execute_function("DOM.getFileInfo", locals())
	
	def get_flattened_document(self, depth: Optional[int] = None, pierce: Optional[bool] = None) -> List[Any]:
		return self._execute_function("DOM.getFlattenedDocument", locals())
	
	def get_frame_owner(self, frame_id: str) -> Tuple[int, Optional[int]]:
		return self._execute_function("DOM.getFrameOwner", locals())
	
	def get_node_for_location(
			self,
			x: int,
			y: int,
			include_user_agent_shadow_dom: Optional[bool] = None,
			ignore_pointer_events_none: Optional[bool] = None
	) -> Tuple[int, str, Optional[int]]:
		return self._execute_function("DOM.getNodeForLocation", locals())
	
	def get_node_stack_traces(self, node_id: int) -> Optional[Any]:
		return self._execute_function("DOM.getNodeStackTraces", locals())
	
	def get_nodes_for_subtree_by_style(
			self,
			node_id: int,
			computed_styles: List[Any],
			pierce: Optional[bool] = None
	) -> List[int]:
		return self._execute_function("DOM.getNodesForSubtreeByStyle", locals())
	
	def get_outer_html(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None,
			include_shadow_dom: Optional[bool] = None
	) -> str:
		return self._execute_function("DOM.getOuterHTML", locals())
	
	def get_querying_descendants_for_container(self, node_id: int) -> List[int]:
		return self._execute_function("DOM.getQueryingDescendantsForContainer", locals())
	
	def get_relayout_boundary(self, node_id: int) -> int:
		return self._execute_function("DOM.getRelayoutBoundary", locals())
	
	def get_search_results(self, search_id: str, from_index: int, to_index: int) -> List[int]:
		return self._execute_function("DOM.getSearchResults", locals())
	
	def get_top_layer_elements(self) -> List[int]:
		return self._execute_function("DOM.getTopLayerElements", locals())
	
	def hide_highlight(self) -> None:
		return self._execute_function("DOM.hideHighlight", locals())
	
	def highlight_node(self) -> None:
		return self._execute_function("DOM.highlightNode", locals())
	
	def highlight_rect(self) -> None:
		return self._execute_function("DOM.highlightRect", locals())
	
	def mark_undoable_state(self) -> None:
		return self._execute_function("DOM.markUndoableState", locals())
	
	def move_to(
			self,
			node_id: int,
			target_node_id: int,
			insert_before_node_id: Optional[int] = None
	) -> int:
		return self._execute_function("DOM.moveTo", locals())
	
	def perform_search(self, query: str, include_user_agent_shadow_dom: Optional[bool] = None) -> Tuple[str, int]:
		return self._execute_function("DOM.performSearch", locals())
	
	def push_node_by_path_to_frontend(self, path: str) -> int:
		return self._execute_function("DOM.pushNodeByPathToFrontend", locals())
	
	def push_nodes_by_backend_ids_to_frontend(self, backend_node_ids: List[int]) -> List[int]:
		return self._execute_function("DOM.pushNodesByBackendIdsToFrontend", locals())
	
	def query_selector(self, node_id: int, selector: str) -> int:
		return self._execute_function("DOM.querySelector", locals())
	
	def query_selector_all(self, node_id: int, selector: str) -> List[int]:
		return self._execute_function("DOM.querySelectorAll", locals())
	
	def redo(self) -> None:
		return self._execute_function("DOM.redo", locals())
	
	def remove_attribute(self, node_id: int, name: str) -> None:
		return self._execute_function("DOM.removeAttribute", locals())
	
	def remove_node(self, node_id: int) -> None:
		return self._execute_function("DOM.removeNode", locals())
	
	def request_child_nodes(
			self,
			node_id: int,
			depth: Optional[int] = None,
			pierce: Optional[bool] = None
	) -> None:
		return self._execute_function("DOM.requestChildNodes", locals())
	
	def request_node(self, object_id: str) -> int:
		return self._execute_function("DOM.requestNode", locals())
	
	def resolve_node(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_group: Optional[str] = None,
			execution_context_id: Optional[int] = None
	) -> Any:
		return self._execute_function("DOM.resolveNode", locals())
	
	def scroll_into_view_if_needed(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None,
			rect: Optional[Any] = None
	) -> None:
		return self._execute_function("DOM.scrollIntoViewIfNeeded", locals())
	
	def set_attribute_value(self, node_id: int, name: str, value: str) -> None:
		return self._execute_function("DOM.setAttributeValue", locals())
	
	def set_attributes_as_text(self, node_id: int, text: str, name: Optional[str] = None) -> None:
		return self._execute_function("DOM.setAttributesAsText", locals())
	
	def set_file_input_files(
			self,
			files: List[str],
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None
	) -> None:
		return self._execute_function("DOM.setFileInputFiles", locals())
	
	def set_inspected_node(self, node_id: int) -> None:
		return self._execute_function("DOM.setInspectedNode", locals())
	
	def set_node_name(self, node_id: int, name: str) -> int:
		return self._execute_function("DOM.setNodeName", locals())
	
	def set_node_stack_traces_enabled(self, enable: bool) -> None:
		return self._execute_function("DOM.setNodeStackTracesEnabled", locals())
	
	def set_node_value(self, node_id: int, value: str) -> None:
		return self._execute_function("DOM.setNodeValue", locals())
	
	def set_outer_html(self, node_id: int, outer_html: str) -> None:
		return self._execute_function("DOM.setOuterHTML", locals())
	
	def undo(self) -> None:
		return self._execute_function("DOM.undo", locals())
