from osn_selenium.abstract.executors.cdp.dom import (
	AbstractDomCDPExecutor
)
from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	List,
	Optional,
	Tuple
)


class DomCDPExecutor(AbstractDomCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def collect_class_names_from_subtree(self, node_id: int) -> List[str]:
		return await self._execute_function("DOM.collectClassNamesFromSubtree", locals())
	
	async def copy_to(
			self,
			node_id: int,
			target_node_id: int,
			insert_before_node_id: Optional[int] = None
	) -> int:
		return await self._execute_function("DOM.copyTo", locals())
	
	async def describe_node(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None,
			depth: Optional[int] = None,
			pierce: Optional[bool] = None
	) -> Any:
		return await self._execute_function("DOM.describeNode", locals())
	
	async def disable(self) -> None:
		return await self._execute_function("DOM.disable", locals())
	
	async def discard_search_results(self, search_id: str) -> None:
		return await self._execute_function("DOM.discardSearchResults", locals())
	
	async def enable(self, include_whitespace: Optional[str] = None) -> None:
		return await self._execute_function("DOM.enable", locals())
	
	async def focus(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None
	) -> None:
		return await self._execute_function("DOM.focus", locals())
	
	async def force_show_popover(self, node_id: int, enable: bool) -> List[int]:
		return await self._execute_function("DOM.forceShowPopover", locals())
	
	async def get_anchor_element(self, node_id: int, anchor_specifier: Optional[str] = None) -> int:
		return await self._execute_function("DOM.getAnchorElement", locals())
	
	async def get_attributes(self, node_id: int) -> List[str]:
		return await self._execute_function("DOM.getAttributes", locals())
	
	async def get_box_model(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None
	) -> Any:
		return await self._execute_function("DOM.getBoxModel", locals())
	
	async def get_container_for_node(
			self,
			node_id: int,
			container_name: Optional[str] = None,
			physical_axes: Optional[str] = None,
			logical_axes: Optional[str] = None,
			queries_scroll_state: Optional[bool] = None,
			queries_anchored: Optional[bool] = None
	) -> Optional[int]:
		return await self._execute_function("DOM.getContainerForNode", locals())
	
	async def get_content_quads(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None
	) -> List[List[Any]]:
		return await self._execute_function("DOM.getContentQuads", locals())
	
	async def get_detached_dom_nodes(self) -> List[List[int]]:
		return await self._execute_function("DOM.getDetachedDomNodes", locals())
	
	async def get_document(self, depth: Optional[int] = None, pierce: Optional[bool] = None) -> Any:
		return await self._execute_function("DOM.getDocument", locals())
	
	async def get_element_by_relation(self, node_id: int, relation: str) -> int:
		return await self._execute_function("DOM.getElementByRelation", locals())
	
	async def get_file_info(self, object_id: str) -> str:
		return await self._execute_function("DOM.getFileInfo", locals())
	
	async def get_flattened_document(self, depth: Optional[int] = None, pierce: Optional[bool] = None) -> List[Any]:
		return await self._execute_function("DOM.getFlattenedDocument", locals())
	
	async def get_frame_owner(self, frame_id: str) -> Tuple[int]:
		return await self._execute_function("DOM.getFrameOwner", locals())
	
	async def get_node_for_location(
			self,
			x: int,
			y: int,
			include_user_agent_shadow_dom: Optional[bool] = None,
			ignore_pointer_events_none: Optional[bool] = None
	) -> Tuple[int]:
		return await self._execute_function("DOM.getNodeForLocation", locals())
	
	async def get_node_stack_traces(self, node_id: int) -> Optional[List[Any]]:
		return await self._execute_function("DOM.getNodeStackTraces", locals())
	
	async def get_nodes_for_subtree_by_style(
			self,
			node_id: int,
			computed_styles: List[Any],
			pierce: Optional[bool] = None
	) -> List[int]:
		return await self._execute_function("DOM.getNodesForSubtreeByStyle", locals())
	
	async def get_outer_html(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None,
			include_shadow_dom: Optional[bool] = None
	) -> str:
		return await self._execute_function("DOM.getOuterHTML", locals())
	
	async def get_querying_descendants_for_container(self, node_id: int) -> List[int]:
		return await self._execute_function("DOM.getQueryingDescendantsForContainer", locals())
	
	async def get_relayout_boundary(self, node_id: int) -> int:
		return await self._execute_function("DOM.getRelayoutBoundary", locals())
	
	async def get_search_results(self, search_id: str, from_index: int, to_index: int) -> List[int]:
		return await self._execute_function("DOM.getSearchResults", locals())
	
	async def get_top_layer_elements(self) -> List[int]:
		return await self._execute_function("DOM.getTopLayerElements", locals())
	
	async def hide_highlight(self) -> None:
		return await self._execute_function("DOM.hideHighlight", locals())
	
	async def highlight_node(self) -> None:
		return await self._execute_function("DOM.highlightNode", locals())
	
	async def highlight_rect(self) -> None:
		return await self._execute_function("DOM.highlightRect", locals())
	
	async def mark_undoable_state(self) -> None:
		return await self._execute_function("DOM.markUndoableState", locals())
	
	async def move_to(
			self,
			node_id: int,
			target_node_id: int,
			insert_before_node_id: Optional[int] = None
	) -> int:
		return await self._execute_function("DOM.moveTo", locals())
	
	async def perform_search(self, query: str, include_user_agent_shadow_dom: Optional[bool] = None) -> Tuple[str]:
		return await self._execute_function("DOM.performSearch", locals())
	
	async def push_node_by_path_to_frontend(self, path: str) -> int:
		return await self._execute_function("DOM.pushNodeByPathToFrontend", locals())
	
	async def push_nodes_by_backend_ids_to_frontend(self, backend_node_ids: List[int]) -> List[int]:
		return await self._execute_function("DOM.pushNodesByBackendIdsToFrontend", locals())
	
	async def query_selector(self, node_id: int, selector: str) -> int:
		return await self._execute_function("DOM.querySelector", locals())
	
	async def query_selector_all(self, node_id: int, selector: str) -> List[int]:
		return await self._execute_function("DOM.querySelectorAll", locals())
	
	async def redo(self) -> None:
		return await self._execute_function("DOM.redo", locals())
	
	async def remove_attribute(self, node_id: int, name: str) -> None:
		return await self._execute_function("DOM.removeAttribute", locals())
	
	async def remove_node(self, node_id: int) -> None:
		return await self._execute_function("DOM.removeNode", locals())
	
	async def request_child_nodes(
			self,
			node_id: int,
			depth: Optional[int] = None,
			pierce: Optional[bool] = None
	) -> None:
		return await self._execute_function("DOM.requestChildNodes", locals())
	
	async def request_node(self, object_id: str) -> int:
		return await self._execute_function("DOM.requestNode", locals())
	
	async def resolve_node(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_group: Optional[str] = None,
			execution_context_id: Optional[int] = None
	) -> Any:
		return await self._execute_function("DOM.resolveNode", locals())
	
	async def scroll_into_view_if_needed(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None,
			rect: Optional[Any] = None
	) -> None:
		return await self._execute_function("DOM.scrollIntoViewIfNeeded", locals())
	
	async def set_attribute_value(self, node_id: int, name: str, value: str) -> None:
		return await self._execute_function("DOM.setAttributeValue", locals())
	
	async def set_attributes_as_text(self, node_id: int, text: str, name: Optional[str] = None) -> None:
		return await self._execute_function("DOM.setAttributesAsText", locals())
	
	async def set_file_input_files(
			self,
			files: List[str],
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None
	) -> None:
		return await self._execute_function("DOM.setFileInputFiles", locals())
	
	async def set_inspected_node(self, node_id: int) -> None:
		return await self._execute_function("DOM.setInspectedNode", locals())
	
	async def set_node_name(self, node_id: int, name: str) -> int:
		return await self._execute_function("DOM.setNodeName", locals())
	
	async def set_node_stack_traces_enabled(self, enable: bool) -> None:
		return await self._execute_function("DOM.setNodeStackTracesEnabled", locals())
	
	async def set_node_value(self, node_id: int, value: str) -> None:
		return await self._execute_function("DOM.setNodeValue", locals())
	
	async def set_outer_html(self, node_id: int, outer_html: str) -> None:
		return await self._execute_function("DOM.setOuterHTML", locals())
	
	async def undo(self) -> None:
		return await self._execute_function("DOM.undo", locals())
