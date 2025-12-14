from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.abstract.executors.cdp.layertree import (
	AbstractLayerTreeCDPExecutor
)


class AsyncLayerTreeCDPExecutor(AbstractLayerTreeCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def compositing_reasons(self, layer_id: str) -> Tuple[List[str]]:
		return await self._execute_function("LayerTree.compositingReasons", locals())
	
	async def disable(self) -> None:
		return await self._execute_function("LayerTree.disable", locals())
	
	async def enable(self) -> None:
		return await self._execute_function("LayerTree.enable", locals())
	
	async def load_snapshot(self, tiles: List[Any]) -> str:
		return await self._execute_function("LayerTree.loadSnapshot", locals())
	
	async def make_snapshot(self, layer_id: str) -> str:
		return await self._execute_function("LayerTree.makeSnapshot", locals())
	
	async def profile_snapshot(
			self,
			snapshot_id: str,
			min_repeat_count: Optional[int] = None,
			min_duration: Optional[float] = None,
			clip_rect: Optional[Any] = None
	) -> List[List[Any]]:
		return await self._execute_function("LayerTree.profileSnapshot", locals())
	
	async def release_snapshot(self, snapshot_id: str) -> None:
		return await self._execute_function("LayerTree.releaseSnapshot", locals())
	
	async def replay_snapshot(
			self,
			snapshot_id: str,
			from_step: Optional[int] = None,
			to_step: Optional[int] = None,
			scale: Optional[float] = None
	) -> str:
		return await self._execute_function("LayerTree.replaySnapshot", locals())
	
	async def snapshot_command_log(self, snapshot_id: str) -> List[dict]:
		return await self._execute_function("LayerTree.snapshotCommandLog", locals())
