from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.abstract.executors.cdp.profiler import (
	AbstractProfilerCDPExecutor
)


class ProfilerCDPExecutor(AbstractProfilerCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def disable(self) -> None:
		return self._execute_function("Profiler.disable", locals())
	
	def enable(self) -> None:
		return self._execute_function("Profiler.enable", locals())
	
	def get_best_effort_coverage(self) -> List[Any]:
		return self._execute_function("Profiler.getBestEffortCoverage", locals())
	
	def set_sampling_interval(self, interval: int) -> None:
		return self._execute_function("Profiler.setSamplingInterval", locals())
	
	def start(self) -> None:
		return self._execute_function("Profiler.start", locals())
	
	def start_precise_coverage(
			self,
			call_count: Optional[bool] = None,
			detailed: Optional[bool] = None,
			allow_triggered_updates: Optional[bool] = None
	) -> float:
		return self._execute_function("Profiler.startPreciseCoverage", locals())
	
	def stop(self) -> Any:
		return self._execute_function("Profiler.stop", locals())
	
	def stop_precise_coverage(self) -> None:
		return self._execute_function("Profiler.stopPreciseCoverage", locals())
	
	def take_precise_coverage(self) -> Tuple[List[Any], float]:
		return self._execute_function("Profiler.takePreciseCoverage", locals())
