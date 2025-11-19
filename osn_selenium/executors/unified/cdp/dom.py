from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)


__all__ = ["UnifiedDomCDPExecutor"]


class UnifiedDomCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _collect_class_names_from_subtree_impl(self, node_id: int) -> List[str]:
		return self._execute_function("DOM.collectClassNamesFromSubtree", {"node_id": node_id})
	
	def _copy_to_impl(
			self,
			node_id: int,
			target_node_id: int,
			insert_before_node_id: Optional[int] = None
	) -> int:
		return self._execute_function(
				"DOM.copyTo",
				{
					"node_id": node_id,
					"target_node_id": target_node_id,
					"insert_before_node_id": insert_before_node_id
				}
		)
	
	def _describe_node_impl(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None,
			depth: Optional[int] = None,
			pierce: Optional[bool] = None
	) -> Dict[str, Any]:
		return self._execute_function(
				"DOM.describeNode",
				{
					"node_id": node_id,
					"backend_node_id": backend_node_id,
					"object_id": object_id,
					"depth": depth,
					"pierce": pierce
				}
		)
	
	def _disable_impl(self) -> None:
		return self._execute_function("DOM.disable", {})
	
	def _discard_search_results_impl(self, search_id: str) -> None:
		return self._execute_function("DOM.discardSearchResults", {"search_id": search_id})
	
	def _enable_impl(self, include_whitespace: Optional[str] = None) -> None:
		return self._execute_function("DOM.enable", {"include_whitespace": include_whitespace})
	
	def _focus_impl(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None
	) -> None:
		return self._execute_function(
				"DOM.focus",
				{
					"node_id": node_id,
					"backend_node_id": backend_node_id,
					"object_id": object_id
				}
		)
	
	def _force_show_popover_impl(self, node_id: int, enable: bool) -> List[int]:
		return self._execute_function("DOM.forceShowPopover", {"node_id": node_id, "enable": enable})
	
	def _get_anchor_element_impl(self, node_id: int, anchor_specifier: Optional[str] = None) -> int:
		return self._execute_function(
				"DOM.getAnchorElement",
				{"node_id": node_id, "anchor_specifier": anchor_specifier}
		)
	
	def _get_attributes_impl(self, node_id: int) -> List[str]:
		return self._execute_function("DOM.getAttributes", {"node_id": node_id})
	
	def _get_box_model_impl(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None
	) -> Dict[str, Any]:
		return self._execute_function(
				"DOM.getBoxModel",
				{
					"node_id": node_id,
					"backend_node_id": backend_node_id,
					"object_id": object_id
				}
		)
	
	def _get_container_for_node_impl(
			self,
			node_id: int,
			container_name: Optional[str] = None,
			physical_axes: Optional[str] = None,
			logical_axes: Optional[str] = None,
			queries_scroll_state: Optional[bool] = None,
			queries_anchored: Optional[bool] = None
	) -> Optional[int]:
		return self._execute_function(
				"DOM.getContainerForNode",
				{
					"node_id": node_id,
					"container_name": container_name,
					"physical_axes": physical_axes,
					"logical_axes": logical_axes,
					"queries_scroll_state": queries_scroll_state,
					"queries_anchored": queries_anchored
				}
		)
	
	def _get_content_quads_impl(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None
	) -> List[List[float]]:
		return self._execute_function(
				"DOM.getContentQuads",
				{
					"node_id": node_id,
					"backend_node_id": backend_node_id,
					"object_id": object_id
				}
		)
	
	def _get_detached_dom_nodes_impl(self) -> List[Dict[str, Any]]:
		return self._execute_function("DOM.getDetachedDomNodes", {})
	
	def _get_document_impl(self, depth: Optional[int] = None, pierce: Optional[bool] = None) -> Dict[str, Any]:
		return self._execute_function("DOM.getDocument", {"depth": depth, "pierce": pierce})
	
	def _get_element_by_relation_impl(self, node_id: int, relation: str) -> int:
		return self._execute_function("DOM.getElementByRelation", {"node_id": node_id, "relation": relation})
	
	def _get_file_info_impl(self, object_id: str) -> str:
		return self._execute_function("DOM.getFileInfo", {"object_id": object_id})
	
	def _get_flattened_document_impl(self, depth: Optional[int] = None, pierce: Optional[bool] = None) -> List[Dict[str, Any]]:
		return self._execute_function("DOM.getFlattenedDocument", {"depth": depth, "pierce": pierce})
	
	def _get_frame_owner_impl(self, frame_id: str) -> Tuple[int, Optional[int]]:
		return self._execute_function("DOM.getFrameOwner", {"frame_id": frame_id})
	
	def _get_node_for_location_impl(
			self,
			x: int,
			y: int,
			include_user_agent_shadow_dom: Optional[bool] = None,
			ignore_pointer_events_none: Optional[bool] = None
	) -> Tuple[int, str, Optional[int]]:
		return self._execute_function(
				"DOM.getNodeForLocation",
				{
					"x": x,
					"y": y,
					"include_user_agent_shadow_dom": include_user_agent_shadow_dom,
					"ignore_pointer_events_none": ignore_pointer_events_none
				}
		)
	
	def _get_node_stack_traces_impl(self, node_id: int) -> Optional[Dict[str, Any]]:
		return self._execute_function("DOM.getNodeStackTraces", {"node_id": node_id})
	
	def _get_nodes_for_subtree_by_style_impl(
			self,
			node_id: int,
			computed_styles: List[Dict[str, Any]],
			pierce: Optional[bool] = None
	) -> List[int]:
		return self._execute_function(
				"DOM.getNodesForSubtreeByStyle",
				{
					"node_id": node_id,
					"computed_styles": computed_styles,
					"pierce": pierce
				}
		)
	
	def _get_outer_html_impl(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None,
			include_shadow_dom: Optional[bool] = None
	) -> str:
		return self._execute_function(
				"DOM.getOuterHTML",
				{
					"node_id": node_id,
					"backend_node_id": backend_node_id,
					"object_id": object_id,
					"include_shadow_dom": include_shadow_dom
				}
		)
	
	def _get_querying_descendants_for_container_impl(self, node_id: int) -> List[int]:
		return self._execute_function("DOM.getQueryingDescendantsForContainer", {"node_id": node_id})
	
	def _get_relayout_boundary_impl(self, node_id: int) -> int:
		return self._execute_function("DOM.getRelayoutBoundary", {"node_id": node_id})
	
	def _get_search_results_impl(self, search_id: str, from_index: int, to_index: int) -> List[int]:
		return self._execute_function(
				"DOM.getSearchResults",
				{"search_id": search_id, "from_index": from_index, "to_index": to_index}
		)
	
	def _get_top_layer_elements_impl(self) -> List[int]:
		return self._execute_function("DOM.getTopLayerElements", {})
	
	def _hide_highlight_impl(self) -> None:
		return self._execute_function("DOM.hideHighlight", {})
	
	def _highlight_node_impl(self) -> None:
		return self._execute_function("DOM.highlightNode", {})
	
	def _highlight_rect_impl(self) -> None:
		return self._execute_function("DOM.highlightRect", {})
	
	def _mark_undoable_state_impl(self) -> None:
		return self._execute_function("DOM.markUndoableState", {})
	
	def _move_to_impl(
			self,
			node_id: int,
			target_node_id: int,
			insert_before_node_id: Optional[int] = None
	) -> int:
		return self._execute_function(
				"DOM.moveTo",
				{
					"node_id": node_id,
					"target_node_id": target_node_id,
					"insert_before_node_id": insert_before_node_id
				}
		)
	
	def _perform_search_impl(self, query: str, include_user_agent_shadow_dom: Optional[bool] = None) -> Tuple[str, int]:
		return self._execute_function(
				"DOM.performSearch",
				{
					"query": query,
					"include_user_agent_shadow_dom": include_user_agent_shadow_dom
				}
		)
	
	def _push_node_by_path_to_frontend_impl(self, path: str) -> int:
		return self._execute_function("DOM.pushNodeByPathToFrontend", {"path": path})
	
	def _push_nodes_by_backend_ids_to_frontend_impl(self, backend_node_ids: List[int]) -> List[int]:
		return self._execute_function(
				"DOM.pushNodesByBackendIdsToFrontend",
				{"backend_node_ids": backend_node_ids}
		)
	
	def _query_selector_all_impl(self, node_id: int, selector: str) -> List[int]:
		return self._execute_function("DOM.querySelectorAll", {"node_id": node_id, "selector": selector})
	
	def _query_selector_impl(self, node_id: int, selector: str) -> int:
		return self._execute_function("DOM.querySelector", {"node_id": node_id, "selector": selector})
	
	def _redo_impl(self) -> None:
		return self._execute_function("DOM.redo", {})
	
	def _remove_attribute_impl(self, node_id: int, name: str) -> None:
		return self._execute_function("DOM.removeAttribute", {"node_id": node_id, "name": name})
	
	def _remove_node_impl(self, node_id: int) -> None:
		return self._execute_function("DOM.removeNode", {"node_id": node_id})
	
	def _request_child_nodes_impl(
			self,
			node_id: int,
			depth: Optional[int] = None,
			pierce: Optional[bool] = None
	) -> None:
		return self._execute_function(
				"DOM.requestChildNodes",
				{"node_id": node_id, "depth": depth, "pierce": pierce}
		)
	
	def _request_node_impl(self, object_id: str) -> int:
		return self._execute_function("DOM.requestNode", {"object_id": object_id})
	
	def _resolve_node_impl(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_group: Optional[str] = None,
			execution_context_id: Optional[int] = None
	) -> Dict[str, Any]:
		return self._execute_function(
				"DOM.resolveNode",
				{
					"node_id": node_id,
					"backend_node_id": backend_node_id,
					"object_group": object_group,
					"execution_context_id": execution_context_id
				}
		)
	
	def _scroll_into_view_if_needed_impl(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None,
			rect: Optional[Dict[str, Any]] = None
	) -> None:
		return self._execute_function(
				"DOM.scrollIntoViewIfNeeded",
				{
					"node_id": node_id,
					"backend_node_id": backend_node_id,
					"object_id": object_id,
					"rect": rect
				}
		)
	
	def _set_attribute_value_impl(self, node_id: int, name: str, value: str) -> None:
		return self._execute_function(
				"DOM.setAttributeValue",
				{"node_id": node_id, "name": name, "value": value}
		)
	
	def _set_attributes_as_text_impl(self, node_id: int, text: str, name: Optional[str] = None) -> None:
		return self._execute_function(
				"DOM.setAttributesAsText",
				{"node_id": node_id, "text": text, "name": name}
		)
	
	def _set_file_input_files_impl(
			self,
			files: List[str],
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None
	) -> None:
		return self._execute_function(
				"DOM.setFileInputFiles",
				{
					"files": files,
					"node_id": node_id,
					"backend_node_id": backend_node_id,
					"object_id": object_id
				}
		)
	
	def _set_inspected_node_impl(self, node_id: int) -> None:
		return self._execute_function("DOM.setInspectedNode", {"node_id": node_id})
	
	def _set_node_name_impl(self, node_id: int, name: str) -> int:
		return self._execute_function("DOM.setNodeName", {"node_id": node_id, "name": name})
	
	def _set_node_stack_traces_enabled_impl(self, enable: bool) -> None:
		return self._execute_function("DOM.setNodeStackTracesEnabled", {"enable": enable})
	
	def _set_node_value_impl(self, node_id: int, value: str) -> None:
		return self._execute_function("DOM.setNodeValue", {"node_id": node_id, "value": value})
	
	def _set_outer_html_impl(self, node_id: int, outer_html: str) -> None:
		return self._execute_function("DOM.setOuterHTML", {"node_id": node_id, "outer_html": outer_html})
	
	def _undo_impl(self) -> None:
		return self._execute_function("DOM.undo", {})
