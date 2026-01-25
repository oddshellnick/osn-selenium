from typing import Any, Dict, List
from abc import ABC, abstractmethod


__all__ = ["AbstractAnimationCDPExecutor"]


class AbstractAnimationCDPExecutor(ABC):
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def enable(self) -> None:
		...
	
	@abstractmethod
	def get_current_time(self, id_: str) -> float:
		...
	
	@abstractmethod
	def get_playback_rate(self) -> float:
		...
	
	@abstractmethod
	def release_animations(self, animations: List[str]) -> None:
		...
	
	@abstractmethod
	def resolve_animation(self, animation_id: str) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def seek_animations(self, animations: List[str], current_time: float) -> None:
		...
	
	@abstractmethod
	def set_paused(self, animations: List[str], paused: bool) -> None:
		...
	
	@abstractmethod
	def set_playback_rate(self, playback_rate: float) -> None:
		...
	
	@abstractmethod
	def set_timing(self, animation_id: str, duration: float, delay: float) -> None:
		...
