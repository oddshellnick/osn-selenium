from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	List,
	Optional
)
from osn_selenium.abstract.executors.cdp.performance import (
	AbstractPerformanceCDPExecutor
)


class PerformanceCDPExecutor(AbstractPerformanceCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def disable(self) -> None:
		return await self._execute_function("Performance.disable", locals())
	
	async def enable(self, time_domain: Optional[str] = None) -> None:
		return await self._execute_function("Performance.enable", locals())
	
	async def get_metrics(self) -> List[Any]:
		return await self._execute_function("Performance.getMetrics", locals())
	
	async def set_time_domain(self, time_domain: str) -> None:
		return await self._execute_function("Performance.setTimeDomain", locals())
