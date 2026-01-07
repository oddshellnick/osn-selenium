from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	List
)
from osn_selenium.abstract.executors.cdp.animation import (
	AbstractAnimationCDPExecutor
)


class AnimationCDPExecutor(AbstractAnimationCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def disable(self) -> None:
		return await self._execute_function("Animation.disable", locals())
	
	async def enable(self) -> None:
		return await self._execute_function("Animation.enable", locals())
	
	async def get_current_time(self, id_: str) -> float:
		return await self._execute_function("Animation.getCurrentTime", locals())
	
	async def get_playback_rate(self) -> float:
		return await self._execute_function("Animation.getPlaybackRate", locals())
	
	async def release_animations(self, animations: List[str]) -> None:
		return await self._execute_function("Animation.releaseAnimations", locals())
	
	async def resolve_animation(self, animation_id: str) -> Any:
		return await self._execute_function("Animation.resolveAnimation", locals())
	
	async def seek_animations(self, animations: List[str], current_time: float) -> None:
		return await self._execute_function("Animation.seekAnimations", locals())
	
	async def set_paused(self, animations: List[str], paused: bool) -> None:
		return await self._execute_function("Animation.setPaused", locals())
	
	async def set_playback_rate(self, playback_rate: float) -> None:
		return await self._execute_function("Animation.setPlaybackRate", locals())
	
	async def set_timing(self, animation_id: str, duration: float, delay: float) -> None:
		return await self._execute_function("Animation.setTiming", locals())
