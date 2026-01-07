from abc import ABC, abstractmethod
from typing import (
	Any,
	List,
	Optional,
	Tuple
)


class AbstractLayerTreeCDPExecutor(ABC):
	@abstractmethod
	def compositing_reasons(self, layer_id: str) -> Tuple[List[str]]:
		...
	
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def enable(self) -> None:
		...
	
	@abstractmethod
	def load_snapshot(self, tiles: List[Any]) -> str:
		...
	
	@abstractmethod
	def make_snapshot(self, layer_id: str) -> str:
		...
	
	@abstractmethod
	def profile_snapshot(
			self,
			snapshot_id: str,
			min_repeat_count: Optional[int] = None,
			min_duration: Optional[float] = None,
			clip_rect: Optional[Any] = None
	) -> List[List[Any]]:
		...
	
	@abstractmethod
	def release_snapshot(self, snapshot_id: str) -> None:
		...
	
	@abstractmethod
	def replay_snapshot(
			self,
			snapshot_id: str,
			from_step: Optional[int] = None,
			to_step: Optional[int] = None,
			scale: Optional[float] = None
	) -> str:
		...
	
	@abstractmethod
	def snapshot_command_log(self, snapshot_id: str) -> List[dict]:
		...
