from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional
)


__all__ = ["UnifiedAccessibilityCDPExecutor"]


class UnifiedAccessibilityCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _disable_impl(self) -> None:
		return self._execute_function("Accessibility.disable", {})
	
	def _enable_impl(self) -> None:
		return self._execute_function("Accessibility.enable", {})
	
	def _get_ax_node_and_ancestors_impl(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None
	) -> List[Dict[str, Any]]:
		return self._execute_function(
				"Accessibility.getAXNodeAndAncestors",
				{
					"node_id": node_id,
					"backend_node_id": backend_node_id,
					"object_id": object_id
				}
		)
	
	def _get_child_ax_nodes_impl(self, id_: str, frame_id: Optional[str] = None) -> List[Dict[str, Any]]:
		return self._execute_function("Accessibility.getChildAXNodes", {"id_": id_, "frame_id": frame_id})
	
	def _get_full_ax_tree_impl(self, depth: Optional[int] = None, frame_id: Optional[str] = None) -> List[Dict[str, Any]]:
		return self._execute_function("Accessibility.getFullAXTree", {"depth": depth, "frame_id": frame_id})
	
	def _get_partial_ax_tree_impl(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None,
			fetch_relatives: Optional[bool] = None
	) -> List[Dict[str, Any]]:
		return self._execute_function(
				"Accessibility.getPartialAXTree",
				{
					"node_id": node_id,
					"backend_node_id": backend_node_id,
					"object_id": object_id,
					"fetch_relatives": fetch_relatives
				}
		)
	
	def _get_root_ax_node_impl(self, frame_id: Optional[str] = None) -> Dict[str, Any]:
		return self._execute_function("Accessibility.getRootAXNode", {"frame_id": frame_id})
	
	def _query_ax_tree_impl(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None,
			accessible_name: Optional[str] = None,
			role: Optional[str] = None
	) -> List[Dict[str, Any]]:
		return self._execute_function(
				"Accessibility.queryAXTree",
				{
					"node_id": node_id,
					"backend_node_id": backend_node_id,
					"object_id": object_id,
					"accessible_name": accessible_name,
					"role": role
				}
		)
