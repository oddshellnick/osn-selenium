import trio
from osn_selenium.base_mixin import TrioThreadMixin
from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.executors.unified.cdp.dom import (
	UnifiedDomCDPExecutor
)
from osn_selenium.abstract.executors.cdp.dom import (
	AbstractDomCDPExecutor
)


__all__ = ["DomCDPExecutor"]


class DomCDPExecutor(UnifiedDomCDPExecutor, TrioThreadMixin, AbstractDomCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedDomCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def collect_class_names_from_subtree(self, node_id: int) -> List[str]:
		return await self.sync_to_trio(sync_function=self._collect_class_names_from_subtree_impl)(node_id=node_id)
	
	async def copy_to(
			self,
			node_id: int,
			target_node_id: int,
			insert_before_node_id: Optional[int] = None
	) -> int:
		return await self.sync_to_trio(sync_function=self._copy_to_impl)(
				node_id=node_id,
				target_node_id=target_node_id,
				insert_before_node_id=insert_before_node_id
		)
	
	async def describe_node(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None,
			depth: Optional[int] = None,
			pierce: Optional[bool] = None
	) -> Dict[str, Any]:
		return await self.sync_to_trio(sync_function=self._describe_node_impl)(
				node_id=node_id,
				backend_node_id=backend_node_id,
				object_id=object_id,
				depth=depth,
				pierce=pierce
		)
	
	async def disable(self) -> None:
		return await self.sync_to_trio(sync_function=self._disable_impl)()
	
	async def discard_search_results(self, search_id: str) -> None:
		return await self.sync_to_trio(sync_function=self._discard_search_results_impl)(search_id=search_id)
	
	async def enable(self, include_whitespace: Optional[str] = None) -> None:
		return await self.sync_to_trio(sync_function=self._enable_impl)(include_whitespace=include_whitespace)
	
	async def focus(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None
	) -> None:
		return await self.sync_to_trio(sync_function=self._focus_impl)(node_id=node_id, backend_node_id=backend_node_id, object_id=object_id)
	
	async def force_show_popover(self, node_id: int, enable: bool) -> List[int]:
		return await self.sync_to_trio(sync_function=self._force_show_popover_impl)(node_id=node_id, enable=enable)
	
	async def get_anchor_element(self, node_id: int, anchor_specifier: Optional[str] = None) -> int:
		return await self.sync_to_trio(sync_function=self._get_anchor_element_impl)(node_id=node_id, anchor_specifier=anchor_specifier)
	
	async def get_attributes(self, node_id: int) -> List[str]:
		return await self.sync_to_trio(sync_function=self._get_attributes_impl)(node_id=node_id)
	
	async def get_box_model(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None
	) -> Dict[str, Any]:
		return await self.sync_to_trio(sync_function=self._get_box_model_impl)(node_id=node_id, backend_node_id=backend_node_id, object_id=object_id)
	
	async def get_container_for_node(
			self,
			node_id: int,
			container_name: Optional[str] = None,
			physical_axes: Optional[str] = None,
			logical_axes: Optional[str] = None,
			queries_scroll_state: Optional[bool] = None,
			queries_anchored: Optional[bool] = None
	) -> Optional[int]:
		return await self.sync_to_trio(sync_function=self._get_container_for_node_impl)(
				node_id=node_id,
				container_name=container_name,
				physical_axes=physical_axes,
				logical_axes=logical_axes,
				queries_scroll_state=queries_scroll_state,
				queries_anchored=queries_anchored
		)
	
	async def get_content_quads(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None
	) -> List[List[float]]:
		return await self.sync_to_trio(sync_function=self._get_content_quads_impl)(node_id=node_id, backend_node_id=backend_node_id, object_id=object_id)
	
	async def get_detached_dom_nodes(self) -> List[Dict[str, Any]]:
		return await self.sync_to_trio(sync_function=self._get_detached_dom_nodes_impl)()
	
	async def get_document(self, depth: Optional[int] = None, pierce: Optional[bool] = None) -> Dict[str, Any]:
		return await self.sync_to_trio(sync_function=self._get_document_impl)(depth=depth, pierce=pierce)
	
	async def get_element_by_relation(self, node_id: int, relation: str) -> int:
		return await self.sync_to_trio(sync_function=self._get_element_by_relation_impl)(node_id=node_id, relation=relation)
	
	async def get_file_info(self, object_id: str) -> str:
		return await self.sync_to_trio(sync_function=self._get_file_info_impl)(object_id=object_id)
	
	async def get_flattened_document(self, depth: Optional[int] = None, pierce: Optional[bool] = None) -> List[Dict[str, Any]]:
		return await self.sync_to_trio(sync_function=self._get_flattened_document_impl)(depth=depth, pierce=pierce)
	
	async def get_frame_owner(self, frame_id: str) -> Tuple[int, Optional[int]]:
		return await self.sync_to_trio(sync_function=self._get_frame_owner_impl)(frame_id=frame_id)
	
	async def get_node_for_location(
			self,
			x: int,
			y: int,
			include_user_agent_shadow_dom: Optional[bool] = None,
			ignore_pointer_events_none: Optional[bool] = None
	) -> Tuple[int, str, Optional[int]]:
		return await self.sync_to_trio(sync_function=self._get_node_for_location_impl)(
				x=x,
				y=y,
				include_user_agent_shadow_dom=include_user_agent_shadow_dom,
				ignore_pointer_events_none=ignore_pointer_events_none
		)
	
	async def get_node_stack_traces(self, node_id: int) -> Optional[Dict[str, Any]]:
		return await self.sync_to_trio(sync_function=self._get_node_stack_traces_impl)(node_id=node_id)
	
	async def get_nodes_for_subtree_by_style(
			self,
			node_id: int,
			computed_styles: List[Dict[str, Any]],
			pierce: Optional[bool] = None
	) -> List[int]:
		return await self.sync_to_trio(sync_function=self._get_nodes_for_subtree_by_style_impl)(node_id=node_id, computed_styles=computed_styles, pierce=pierce)
	
	async def get_outer_html(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None,
			include_shadow_dom: Optional[bool] = None
	) -> str:
		return await self.sync_to_trio(sync_function=self._get_outer_html_impl)(
				node_id=node_id,
				backend_node_id=backend_node_id,
				object_id=object_id,
				include_shadow_dom=include_shadow_dom
		)
	
	async def get_querying_descendants_for_container(self, node_id: int) -> List[int]:
		return await self.sync_to_trio(sync_function=self._get_querying_descendants_for_container_impl)(node_id=node_id)
	
	async def get_relayout_boundary(self, node_id: int) -> int:
		return await self.sync_to_trio(sync_function=self._get_relayout_boundary_impl)(node_id=node_id)
	
	async def get_search_results(self, search_id: str, from_index: int, to_index: int) -> List[int]:
		return await self.sync_to_trio(sync_function=self._get_search_results_impl)(search_id=search_id, from_index=from_index, to_index=to_index)
	
	async def get_top_layer_elements(self) -> List[int]:
		return await self.sync_to_trio(sync_function=self._get_top_layer_elements_impl)()
	
	async def hide_highlight(self) -> None:
		return await self.sync_to_trio(sync_function=self._hide_highlight_impl)()
	
	async def highlight_node(self) -> None:
		return await self.sync_to_trio(sync_function=self._highlight_node_impl)()
	
	async def highlight_rect(self) -> None:
		return await self.sync_to_trio(sync_function=self._highlight_rect_impl)()
	
	async def mark_undoable_state(self) -> None:
		return await self.sync_to_trio(sync_function=self._mark_undoable_state_impl)()
	
	async def move_to(
			self,
			node_id: int,
			target_node_id: int,
			insert_before_node_id: Optional[int] = None
	) -> int:
		return await self.sync_to_trio(sync_function=self._move_to_impl)(
				node_id=node_id,
				target_node_id=target_node_id,
				insert_before_node_id=insert_before_node_id
		)
	
	async def perform_search(self, query: str, include_user_agent_shadow_dom: Optional[bool] = None) -> Tuple[str, int]:
		return await self.sync_to_trio(sync_function=self._perform_search_impl)(
				query=query,
				include_user_agent_shadow_dom=include_user_agent_shadow_dom
		)
	
	async def push_node_by_path_to_frontend(self, path: str) -> int:
		return await self.sync_to_trio(sync_function=self._push_node_by_path_to_frontend_impl)(path=path)
	
	async def push_nodes_by_backend_ids_to_frontend(self, backend_node_ids: List[int]) -> List[int]:
		return await self.sync_to_trio(sync_function=self._push_nodes_by_backend_ids_to_frontend_impl)(backend_node_ids=backend_node_ids)
	
	async def query_selector(self, node_id: int, selector: str) -> int:
		return await self.sync_to_trio(sync_function=self._query_selector_impl)(node_id=node_id, selector=selector)
	
	async def query_selector_all(self, node_id: int, selector: str) -> List[int]:
		return await self.sync_to_trio(sync_function=self._query_selector_all_impl)(node_id=node_id, selector=selector)
	
	async def redo(self) -> None:
		return await self.sync_to_trio(sync_function=self._redo_impl)()
	
	async def remove_attribute(self, node_id: int, name: str) -> None:
		return await self.sync_to_trio(sync_function=self._remove_attribute_impl)(node_id=node_id, name=name)
	
	async def remove_node(self, node_id: int) -> None:
		return await self.sync_to_trio(sync_function=self._remove_node_impl)(node_id=node_id)
	
	async def request_child_nodes(
			self,
			node_id: int,
			depth: Optional[int] = None,
			pierce: Optional[bool] = None
	) -> None:
		return await self.sync_to_trio(sync_function=self._request_child_nodes_impl)(node_id=node_id, depth=depth, pierce=pierce)
	
	async def request_node(self, object_id: str) -> int:
		return await self.sync_to_trio(sync_function=self._request_node_impl)(object_id=object_id)
	
	async def resolve_node(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_group: Optional[str] = None,
			execution_context_id: Optional[int] = None
	) -> Dict[str, Any]:
		return await self.sync_to_trio(sync_function=self._resolve_node_impl)(
				node_id=node_id,
				backend_node_id=backend_node_id,
				object_group=object_group,
				execution_context_id=execution_context_id
		)
	
	async def scroll_into_view_if_needed(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None,
			rect: Optional[Dict[str, Any]] = None
	) -> None:
		return await self.sync_to_trio(sync_function=self._scroll_into_view_if_needed_impl)(
				node_id=node_id,
				backend_node_id=backend_node_id,
				object_id=object_id,
				rect=rect
		)
	
	async def set_attribute_value(self, node_id: int, name: str, value: str) -> None:
		return await self.sync_to_trio(sync_function=self._set_attribute_value_impl)(node_id=node_id, name=name, value=value)
	
	async def set_attributes_as_text(self, node_id: int, text: str, name: Optional[str] = None) -> None:
		return await self.sync_to_trio(sync_function=self._set_attributes_as_text_impl)(node_id=node_id, text=text, name=name)
	
	async def set_file_input_files(
			self,
			files: List[str],
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None
	) -> None:
		return await self.sync_to_trio(sync_function=self._set_file_input_files_impl)(
				files=files,
				node_id=node_id,
				backend_node_id=backend_node_id,
				object_id=object_id
		)
	
	async def set_inspected_node(self, node_id: int) -> None:
		return await self.sync_to_trio(sync_function=self._set_inspected_node_impl)(node_id=node_id)
	
	async def set_node_name(self, node_id: int, name: str) -> int:
		return await self.sync_to_trio(sync_function=self._set_node_name_impl)(node_id=node_id, name=name)
	
	async def set_node_stack_traces_enabled(self, enable: bool) -> None:
		return await self.sync_to_trio(sync_function=self._set_node_stack_traces_enabled_impl)(enable=enable)
	
	async def set_node_value(self, node_id: int, value: str) -> None:
		return await self.sync_to_trio(sync_function=self._set_node_value_impl)(node_id=node_id, value=value)
	
	async def set_outer_html(self, node_id: int, outer_html: str) -> None:
		return await self.sync_to_trio(sync_function=self._set_outer_html_impl)(node_id=node_id, outer_html=outer_html)
	
	async def undo(self) -> None:
		return await self.sync_to_trio(sync_function=self._undo_impl)()
