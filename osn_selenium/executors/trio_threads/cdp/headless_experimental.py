from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	Optional,
	Tuple
)
from osn_selenium.abstract.executors.cdp.headless_experimental import (
	AbstractHeadlessExperimentalCDPExecutor
)


class HeadlessExperimentalCDPExecutor(AbstractHeadlessExperimentalCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def begin_frame(
			self,
			frame_time_ticks: Optional[float] = None,
			interval: Optional[float] = None,
			no_display_updates: Optional[bool] = None,
			screenshot: Optional[Any] = None
	) -> Tuple[bool, Optional[str]]:
		return await self._execute_function("HeadlessExperimental.beginFrame", locals())
	
	async def disable(self) -> None:
		return await self._execute_function("HeadlessExperimental.disable", locals())
	
	async def enable(self) -> None:
		return await self._execute_function("HeadlessExperimental.enable", locals())
