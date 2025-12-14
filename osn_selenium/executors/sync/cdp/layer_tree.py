from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.abstract.executors.cdp.layer_tree import (
	AbstractLayerTreeCDPExecutor
)


class LayerTreeCDPExecutor(AbstractLayerTreeCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def compositing_reasons(self, layer_id: str) -> Tuple[List[str], List[str]]:
		return self._execute_function("LayerTree.compositingReasons", locals())
	
	def disable(self) -> None:
		return self._execute_function("LayerTree.disable", locals())
	
	def enable(self) -> None:
		return self._execute_function("LayerTree.enable", locals())
	
	def load_snapshot(self, tiles: List[Any]) -> str:
		return self._execute_function("LayerTree.loadSnapshot", locals())
	
	def make_snapshot(self, layer_id: str) -> str:
		return self._execute_function("LayerTree.makeSnapshot", locals())
	
	def profile_snapshot(
			self,
			snapshot_id: str,
			min_repeat_count: Optional[int] = None,
			min_duration: Optional[float] = None,
			clip_rect: Optional[Any] = None
	) -> List[List[Any]]:
		return self._execute_function("LayerTree.profileSnapshot", locals())
	
	def release_snapshot(self, snapshot_id: str) -> None:
		return self._execute_function("LayerTree.releaseSnapshot", locals())
	
	def replay_snapshot(
			self,
			snapshot_id: str,
			from_step: Optional[int] = None,
			to_step: Optional[int] = None,
			scale: Optional[float] = None
	) -> str:
		return self._execute_function("LayerTree.replaySnapshot", locals())
	
	def snapshot_command_log(self, snapshot_id: str) -> List[dict]:
		return self._execute_function("LayerTree.snapshotCommandLog", locals())
