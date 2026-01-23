from typing import (
	Any,
	Callable,
	Dict,
	Optional,
	Tuple
)
from osn_selenium.executors.unified.cdp.headless_experimental import (
	UnifiedHeadlessExperimentalCDPExecutor
)
from osn_selenium.abstract.executors.cdp.headless_experimental import (
	AbstractHeadlessExperimentalCDPExecutor
)


__all__ = ["HeadlessExperimentalCDPExecutor"]


class HeadlessExperimentalCDPExecutor(
		UnifiedHeadlessExperimentalCDPExecutor,
		AbstractHeadlessExperimentalCDPExecutor
):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedHeadlessExperimentalCDPExecutor.__init__(self, execute_function=execute_function)
	
	def begin_frame(
			self,
			frame_time_ticks: Optional[float] = None,
			interval: Optional[float] = None,
			no_display_updates: Optional[bool] = None,
			screenshot: Optional[Dict[str, Any]] = None
	) -> Tuple[bool, Optional[str]]:
		return self._begin_frame_impl(
				frame_time_ticks=frame_time_ticks,
				interval=interval,
				no_display_updates=no_display_updates,
				screenshot=screenshot
		)
	
	def disable(self) -> None:
		return self._disable_impl()
	
	def enable(self) -> None:
		return self._enable_impl()
