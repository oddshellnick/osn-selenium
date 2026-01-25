from typing import (
	Any,
	Callable,
	Dict,
	Optional,
	Tuple
)


__all__ = ["UnifiedHeadlessExperimentalCDPExecutor"]


class UnifiedHeadlessExperimentalCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _begin_frame_impl(
			self,
			frame_time_ticks: Optional[float] = None,
			interval: Optional[float] = None,
			no_display_updates: Optional[bool] = None,
			screenshot: Optional[Dict[str, Any]] = None
	) -> Tuple[bool, Optional[str]]:
		return self._execute_function(
				"HeadlessExperimental.beginFrame",
				{
					"frame_time_ticks": frame_time_ticks,
					"interval": interval,
					"no_display_updates": no_display_updates,
					"screenshot": screenshot
				}
		)
	
	def _disable_impl(self) -> None:
		return self._execute_function("HeadlessExperimental.disable", {})
	
	def _enable_impl(self) -> None:
		return self._execute_function("HeadlessExperimental.enable", {})
