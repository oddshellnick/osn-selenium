from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	List
)
from osn_selenium.abstract.executors.cdp.performancetimeline import (
	AbstractPerformanceTimelineCDPExecutor
)


class AsyncPerformanceTimelineCDPExecutor(AbstractPerformanceTimelineCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def enable(self, event_types: List[str]) -> None:
		return await self._execute_function("PerformanceTimeline.enable", locals())
