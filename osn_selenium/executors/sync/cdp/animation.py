from typing import (
	Any,
	Callable,
	Dict,
	List
)
from osn_selenium.executors.unified.cdp.animation import (
	UnifiedAnimationCDPExecutor
)
from osn_selenium.abstract.executors.cdp.animation import (
	AbstractAnimationCDPExecutor
)


__all__ = ["AnimationCDPExecutor"]


class AnimationCDPExecutor(UnifiedAnimationCDPExecutor, AbstractAnimationCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedAnimationCDPExecutor.__init__(self, execute_function=execute_function)
	
	def disable(self) -> None:
		return self._disable_impl()
	
	def enable(self) -> None:
		return self._enable_impl()
	
	def get_current_time(self, id_: str) -> float:
		return self._get_current_time_impl(id_=id_)
	
	def get_playback_rate(self) -> float:
		return self._get_playback_rate_impl()
	
	def release_animations(self, animations: List[str]) -> None:
		return self._release_animations_impl(animations=animations)
	
	def resolve_animation(self, animation_id: str) -> Dict[str, Any]:
		return self._resolve_animation_impl(animation_id=animation_id)
	
	def seek_animations(self, animations: List[str], current_time: float) -> None:
		return self._seek_animations_impl(animations=animations, current_time=current_time)
	
	def set_paused(self, animations: List[str], paused: bool) -> None:
		return self._set_paused_impl(animations=animations, paused=paused)
	
	def set_playback_rate(self, playback_rate: float) -> None:
		return self._set_playback_rate_impl(playback_rate=playback_rate)
	
	def set_timing(self, animation_id: str, duration: float, delay: float) -> None:
		return self._set_timing_impl(animation_id=animation_id, duration=duration, delay=delay)
