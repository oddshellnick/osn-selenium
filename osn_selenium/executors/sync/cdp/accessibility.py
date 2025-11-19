from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional
)
from osn_selenium.executors.unified.cdp.accessibility import (
	UnifiedAccessibilityCDPExecutor
)
from osn_selenium.abstract.executors.cdp.accessibility import (
	AbstractAccessibilityCDPExecutor
)


__all__ = ["AccessibilityCDPExecutor"]


class AccessibilityCDPExecutor(UnifiedAccessibilityCDPExecutor, AbstractAccessibilityCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedAccessibilityCDPExecutor.__init__(self, execute_function=execute_function)
	
	def disable(self) -> None:
		return self._disable_impl()
	
	def enable(self) -> None:
		return self._enable_impl()
	
	def get_ax_node_and_ancestors(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None
	) -> List[Dict[str, Any]]:
		return self._get_ax_node_and_ancestors_impl(node_id=node_id, backend_node_id=backend_node_id, object_id=object_id)
	
	def get_child_ax_nodes(self, id_: str, frame_id: Optional[str] = None) -> List[Dict[str, Any]]:
		return self._get_child_ax_nodes_impl(id_=id_, frame_id=frame_id)
	
	def get_full_ax_tree(self, depth: Optional[int] = None, frame_id: Optional[str] = None) -> List[Dict[str, Any]]:
		return self._get_full_ax_tree_impl(depth=depth, frame_id=frame_id)
	
	def get_partial_ax_tree(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None,
			fetch_relatives: Optional[bool] = None
	) -> List[Dict[str, Any]]:
		return self._get_partial_ax_tree_impl(
				node_id=node_id,
				backend_node_id=backend_node_id,
				object_id=object_id,
				fetch_relatives=fetch_relatives
		)
	
	def get_root_ax_node(self, frame_id: Optional[str] = None) -> Dict[str, Any]:
		return self._get_root_ax_node_impl(frame_id=frame_id)
	
	def query_ax_tree(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None,
			accessible_name: Optional[str] = None,
			role: Optional[str] = None
	) -> List[Dict[str, Any]]:
		return self._query_ax_tree_impl(
				node_id=node_id,
				backend_node_id=backend_node_id,
				object_id=object_id,
				accessible_name=accessible_name,
				role=role
		)
