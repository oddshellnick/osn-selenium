from typing import (
	Any,
	Callable,
	Dict,
	Optional,
	Tuple
)
from osn_selenium.abstract.executors.cdp.headlessexperimental import (
	AbstractHeadlessExperimentalCDPExecutor
)


class HeadlessExperimentalCDPExecutor(AbstractHeadlessExperimentalCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def begin_frame(
			self,
			frame_time_ticks: Optional[float] = None,
			interval: Optional[float] = None,
			no_display_updates: Optional[bool] = None,
			screenshot: Optional[Any] = None
	) -> Tuple[bool]:
		return self._execute_function("HeadlessExperimental.beginFrame", locals())
	
	def disable(self) -> None:
		return self._execute_function("HeadlessExperimental.disable", locals())
	
	def enable(self) -> None:
		return self._execute_function("HeadlessExperimental.enable", locals())
