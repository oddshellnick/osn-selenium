from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.abstract.executors.cdp.profiler import (
	AbstractProfilerCDPExecutor
)


class ProfilerCDPExecutor(AbstractProfilerCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def disable(self) -> None:
		return await self._execute_function("Profiler.disable", locals())
	
	async def enable(self) -> None:
		return await self._execute_function("Profiler.enable", locals())
	
	async def get_best_effort_coverage(self) -> List[List[List[Any]]]:
		return await self._execute_function("Profiler.getBestEffortCoverage", locals())
	
	async def set_sampling_interval(self, interval: int) -> None:
		return await self._execute_function("Profiler.setSamplingInterval", locals())
	
	async def start(self) -> None:
		return await self._execute_function("Profiler.start", locals())
	
	async def start_precise_coverage(
			self,
			call_count: Optional[bool] = None,
			detailed: Optional[bool] = None,
			allow_triggered_updates: Optional[bool] = None
	) -> float:
		return await self._execute_function("Profiler.startPreciseCoverage", locals())
	
	async def stop(self) -> List[Any]:
		return await self._execute_function("Profiler.stop", locals())
	
	async def stop_precise_coverage(self) -> None:
		return await self._execute_function("Profiler.stopPreciseCoverage", locals())
	
	async def take_precise_coverage(self) -> Tuple[List[List[List[Any]]]]:
		return await self._execute_function("Profiler.takePreciseCoverage", locals())
