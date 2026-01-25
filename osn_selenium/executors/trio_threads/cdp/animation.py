import trio
from osn_selenium.base_mixin import TrioThreadMixin
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


class AnimationCDPExecutor(
		UnifiedAnimationCDPExecutor,
		TrioThreadMixin,
		AbstractAnimationCDPExecutor
):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedAnimationCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def disable(self) -> None:
		return await self.sync_to_trio(sync_function=self._disable_impl)()
	
	async def enable(self) -> None:
		return await self.sync_to_trio(sync_function=self._enable_impl)()
	
	async def get_current_time(self, id_: str) -> float:
		return await self.sync_to_trio(sync_function=self._get_current_time_impl)(id_=id_)
	
	async def get_playback_rate(self) -> float:
		return await self.sync_to_trio(sync_function=self._get_playback_rate_impl)()
	
	async def release_animations(self, animations: List[str]) -> None:
		return await self.sync_to_trio(sync_function=self._release_animations_impl)(animations=animations)
	
	async def resolve_animation(self, animation_id: str) -> Dict[str, Any]:
		return await self.sync_to_trio(sync_function=self._resolve_animation_impl)(animation_id=animation_id)
	
	async def seek_animations(self, animations: List[str], current_time: float) -> None:
		return await self.sync_to_trio(sync_function=self._seek_animations_impl)(animations=animations, current_time=current_time)
	
	async def set_paused(self, animations: List[str], paused: bool) -> None:
		return await self.sync_to_trio(sync_function=self._set_paused_impl)(animations=animations, paused=paused)
	
	async def set_playback_rate(self, playback_rate: float) -> None:
		return await self.sync_to_trio(sync_function=self._set_playback_rate_impl)(playback_rate=playback_rate)
	
	async def set_timing(self, animation_id: str, duration: float, delay: float) -> None:
		return await self.sync_to_trio(sync_function=self._set_timing_impl)(animation_id=animation_id, duration=duration, delay=delay)
