from typing import (
	Any,
	Callable,
	Dict,
	List
)


__all__ = ["UnifiedAnimationCDPExecutor"]


class UnifiedAnimationCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _disable_impl(self) -> None:
		return self._execute_function("Animation.disable", {})
	
	def _enable_impl(self) -> None:
		return self._execute_function("Animation.enable", {})
	
	def _get_current_time_impl(self, id_: str) -> float:
		return self._execute_function("Animation.getCurrentTime", {"id_": id_})
	
	def _get_playback_rate_impl(self) -> float:
		return self._execute_function("Animation.getPlaybackRate", {})
	
	def _release_animations_impl(self, animations: List[str]) -> None:
		return self._execute_function("Animation.releaseAnimations", {"animations": animations})
	
	def _resolve_animation_impl(self, animation_id: str) -> Dict[str, Any]:
		return self._execute_function("Animation.resolveAnimation", {"animation_id": animation_id})
	
	def _seek_animations_impl(self, animations: List[str], current_time: float) -> None:
		return self._execute_function(
				"Animation.seekAnimations",
				{"animations": animations, "current_time": current_time}
		)
	
	def _set_paused_impl(self, animations: List[str], paused: bool) -> None:
		return self._execute_function("Animation.setPaused", {"animations": animations, "paused": paused})
	
	def _set_playback_rate_impl(self, playback_rate: float) -> None:
		return self._execute_function("Animation.setPlaybackRate", {"playback_rate": playback_rate})
	
	def _set_timing_impl(self, animation_id: str, duration: float, delay: float) -> None:
		return self._execute_function(
				"Animation.setTiming",
				{"animation_id": animation_id, "duration": duration, "delay": delay}
		)
