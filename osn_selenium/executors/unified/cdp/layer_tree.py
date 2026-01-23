from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)


__all__ = ["UnifiedLayerTreeCDPExecutor"]


class UnifiedLayerTreeCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _compositing_reasons_impl(self, layer_id: str) -> Tuple[List[str], List[str]]:
		return self._execute_function("LayerTree.compositingReasons", {"layer_id": layer_id})
	
	def _disable_impl(self) -> None:
		return self._execute_function("LayerTree.disable", {})
	
	def _enable_impl(self) -> None:
		return self._execute_function("LayerTree.enable", {})
	
	def _load_snapshot_impl(self, tiles: List[Dict[str, Any]]) -> str:
		return self._execute_function("LayerTree.loadSnapshot", {"tiles": tiles})
	
	def _make_snapshot_impl(self, layer_id: str) -> str:
		return self._execute_function("LayerTree.makeSnapshot", {"layer_id": layer_id})
	
	def _profile_snapshot_impl(
			self,
			snapshot_id: str,
			min_repeat_count: Optional[int] = None,
			min_duration: Optional[float] = None,
			clip_rect: Optional[Dict[str, Any]] = None
	) -> List[List[float]]:
		return self._execute_function(
				"LayerTree.profileSnapshot",
				{
					"snapshot_id": snapshot_id,
					"min_repeat_count": min_repeat_count,
					"min_duration": min_duration,
					"clip_rect": clip_rect
				}
		)
	
	def _release_snapshot_impl(self, snapshot_id: str) -> None:
		return self._execute_function("LayerTree.releaseSnapshot", {"snapshot_id": snapshot_id})
	
	def _replay_snapshot_impl(
			self,
			snapshot_id: str,
			from_step: Optional[int] = None,
			to_step: Optional[int] = None,
			scale: Optional[float] = None
	) -> str:
		return self._execute_function(
				"LayerTree.replaySnapshot",
				{
					"snapshot_id": snapshot_id,
					"from_step": from_step,
					"to_step": to_step,
					"scale": scale
				}
		)
	
	def _snapshot_command_log_impl(self, snapshot_id: str) -> List[Any]:
		return self._execute_function("LayerTree.snapshotCommandLog", {"snapshot_id": snapshot_id})
