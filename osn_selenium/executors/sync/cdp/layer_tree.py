from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.executors.unified.cdp.layer_tree import (
	UnifiedLayerTreeCDPExecutor
)
from osn_selenium.abstract.executors.cdp.layer_tree import (
	AbstractLayerTreeCDPExecutor
)


__all__ = ["LayerTreeCDPExecutor"]


class LayerTreeCDPExecutor(UnifiedLayerTreeCDPExecutor, AbstractLayerTreeCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedLayerTreeCDPExecutor.__init__(self, execute_function=execute_function)
	
	def compositing_reasons(self, layer_id: str) -> Tuple[List[str], List[str]]:
		return self._compositing_reasons_impl(layer_id=layer_id)
	
	def disable(self) -> None:
		return self._disable_impl()
	
	def enable(self) -> None:
		return self._enable_impl()
	
	def load_snapshot(self, tiles: List[Dict[str, Any]]) -> str:
		return self._load_snapshot_impl(tiles=tiles)
	
	def make_snapshot(self, layer_id: str) -> str:
		return self._make_snapshot_impl(layer_id=layer_id)
	
	def profile_snapshot(
			self,
			snapshot_id: str,
			min_repeat_count: Optional[int] = None,
			min_duration: Optional[float] = None,
			clip_rect: Optional[Dict[str, Any]] = None
	) -> List[List[float]]:
		return self._profile_snapshot_impl(
				snapshot_id=snapshot_id,
				min_repeat_count=min_repeat_count,
				min_duration=min_duration,
				clip_rect=clip_rect
		)
	
	def release_snapshot(self, snapshot_id: str) -> None:
		return self._release_snapshot_impl(snapshot_id=snapshot_id)
	
	def replay_snapshot(
			self,
			snapshot_id: str,
			from_step: Optional[int] = None,
			to_step: Optional[int] = None,
			scale: Optional[float] = None
	) -> str:
		return self._replay_snapshot_impl(
				snapshot_id=snapshot_id,
				from_step=from_step,
				to_step=to_step,
				scale=scale
		)
	
	def snapshot_command_log(self, snapshot_id: str) -> List[Any]:
		return self._snapshot_command_log_impl(snapshot_id=snapshot_id)
