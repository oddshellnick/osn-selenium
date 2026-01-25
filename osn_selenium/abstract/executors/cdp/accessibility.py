from abc import ABC, abstractmethod
from typing import (
	Any,
	Dict,
	List,
	Optional
)


__all__ = ["AbstractAccessibilityCDPExecutor"]


class AbstractAccessibilityCDPExecutor(ABC):
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def enable(self) -> None:
		...
	
	@abstractmethod
	def get_ax_node_and_ancestors(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None
	) -> List[Dict[str, Any]]:
		...
	
	@abstractmethod
	def get_child_ax_nodes(self, id_: str, frame_id: Optional[str] = None) -> List[Dict[str, Any]]:
		...
	
	@abstractmethod
	def get_full_ax_tree(self, depth: Optional[int] = None, frame_id: Optional[str] = None) -> List[Dict[str, Any]]:
		...
	
	@abstractmethod
	def get_partial_ax_tree(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None,
			fetch_relatives: Optional[bool] = None
	) -> List[Dict[str, Any]]:
		...
	
	@abstractmethod
	def get_root_ax_node(self, frame_id: Optional[str] = None) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def query_ax_tree(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None,
			accessible_name: Optional[str] = None,
			role: Optional[str] = None
	) -> List[Dict[str, Any]]:
		...
