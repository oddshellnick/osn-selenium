import trio
from osn_selenium.base_mixin import TrioThreadMixin
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


class AccessibilityCDPExecutor(
		UnifiedAccessibilityCDPExecutor,
		TrioThreadMixin,
		AbstractAccessibilityCDPExecutor
):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedAccessibilityCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def disable(self) -> None:
		return await self.sync_to_trio(sync_function=self._disable_impl)()
	
	async def enable(self) -> None:
		return await self.sync_to_trio(sync_function=self._enable_impl)()
	
	async def get_ax_node_and_ancestors(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None
	) -> List[Dict[str, Any]]:
		return await self.sync_to_trio(sync_function=self._get_ax_node_and_ancestors_impl)(node_id=node_id, backend_node_id=backend_node_id, object_id=object_id)
	
	async def get_child_ax_nodes(self, id_: str, frame_id: Optional[str] = None) -> List[Dict[str, Any]]:
		return await self.sync_to_trio(sync_function=self._get_child_ax_nodes_impl)(id_=id_, frame_id=frame_id)
	
	async def get_full_ax_tree(self, depth: Optional[int] = None, frame_id: Optional[str] = None) -> List[Dict[str, Any]]:
		return await self.sync_to_trio(sync_function=self._get_full_ax_tree_impl)(depth=depth, frame_id=frame_id)
	
	async def get_partial_ax_tree(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None,
			fetch_relatives: Optional[bool] = None
	) -> List[Dict[str, Any]]:
		return await self.sync_to_trio(sync_function=self._get_partial_ax_tree_impl)(
				node_id=node_id,
				backend_node_id=backend_node_id,
				object_id=object_id,
				fetch_relatives=fetch_relatives
		)
	
	async def get_root_ax_node(self, frame_id: Optional[str] = None) -> Dict[str, Any]:
		return await self.sync_to_trio(sync_function=self._get_root_ax_node_impl)(frame_id=frame_id)
	
	async def query_ax_tree(
			self,
			node_id: Optional[int] = None,
			backend_node_id: Optional[int] = None,
			object_id: Optional[str] = None,
			accessible_name: Optional[str] = None,
			role: Optional[str] = None
	) -> List[Dict[str, Any]]:
		return await self.sync_to_trio(sync_function=self._query_ax_tree_impl)(
				node_id=node_id,
				backend_node_id=backend_node_id,
				object_id=object_id,
				accessible_name=accessible_name,
				role=role
		)
