from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional
)
from osn_selenium.abstract.executors.cdp.accessibility import (
	AbstractAccessibilityCDPExecutor
)


class AccessibilityCDPExecutor(AbstractAccessibilityCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def disable(self) -> None:
		return self._execute_function("Accessibility.disable", locals())
	
	def enable(self) -> None:
		return self._execute_function("Accessibility.enable", locals())
	
	def get_ax_node_and_ancestors(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None
	) -> List[Any]:
		return self._execute_function("Accessibility.getAXNodeAndAncestors", locals())
	
	def get_child_ax_nodes(self, id_: str, frame_id: Optional[str] = None) -> List[Any]:
		return self._execute_function("Accessibility.getChildAXNodes", locals())
	
	def get_full_ax_tree(self, depth: Optional[int] = None, frame_id: Optional[str] = None) -> List[Any]:
		return self._execute_function("Accessibility.getFullAXTree", locals())
	
	def get_partial_ax_tree(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None,
			fetch_relatives: Optional[bool] = None
	) -> List[Any]:
		return self._execute_function("Accessibility.getPartialAXTree", locals())
	
	def get_root_ax_node(self, frame_id: Optional[str] = None) -> Any:
		return self._execute_function("Accessibility.getRootAXNode", locals())
	
	def query_ax_tree(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None,
			accessible_name: Optional[str] = None,
			role: Optional[str] = None
	) -> List[Any]:
		return self._execute_function("Accessibility.queryAXTree", locals())
