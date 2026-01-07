from typing import (
	Any,
	Callable,
	Dict,
	List
)
from osn_selenium.abstract.executors.cdp.animation import (
	AbstractAnimationCDPExecutor
)


class AnimationCDPExecutor(AbstractAnimationCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def disable(self) -> None:
		return self._execute_function("Animation.disable", locals())
	
	def enable(self) -> None:
		return self._execute_function("Animation.enable", locals())
	
	def get_current_time(self, id_: str) -> float:
		return self._execute_function("Animation.getCurrentTime", locals())
	
	def get_playback_rate(self) -> float:
		return self._execute_function("Animation.getPlaybackRate", locals())
	
	def release_animations(self, animations: List[str]) -> None:
		return self._execute_function("Animation.releaseAnimations", locals())
	
	def resolve_animation(self, animation_id: str) -> Any:
		return self._execute_function("Animation.resolveAnimation", locals())
	
	def seek_animations(self, animations: List[str], current_time: float) -> None:
		return self._execute_function("Animation.seekAnimations", locals())
	
	def set_paused(self, animations: List[str], paused: bool) -> None:
		return self._execute_function("Animation.setPaused", locals())
	
	def set_playback_rate(self, playback_rate: float) -> None:
		return self._execute_function("Animation.setPlaybackRate", locals())
	
	def set_timing(self, animation_id: str, duration: float, delay: float) -> None:
		return self._execute_function("Animation.setTiming", locals())
