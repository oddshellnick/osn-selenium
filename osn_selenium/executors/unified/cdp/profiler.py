from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)


__all__ = ["UnifiedProfilerCDPExecutor"]


class UnifiedProfilerCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _disable_impl(self) -> None:
		return self._execute_function("Profiler.disable", {})
	
	def _enable_impl(self) -> None:
		return self._execute_function("Profiler.enable", {})
	
	def _get_best_effort_coverage_impl(self) -> List[Dict[str, Any]]:
		return self._execute_function("Profiler.getBestEffortCoverage", {})
	
	def _set_sampling_interval_impl(self, interval: int) -> None:
		return self._execute_function("Profiler.setSamplingInterval", {"interval": interval})
	
	def _start_impl(self) -> None:
		return self._execute_function("Profiler.start", {})
	
	def _start_precise_coverage_impl(
			self,
			call_count: Optional[bool] = None,
			detailed: Optional[bool] = None,
			allow_triggered_updates: Optional[bool] = None
	) -> float:
		return self._execute_function(
				"Profiler.startPreciseCoverage",
				{
					"call_count": call_count,
					"detailed": detailed,
					"allow_triggered_updates": allow_triggered_updates
				}
		)
	
	def _stop_impl(self) -> Dict[str, Any]:
		return self._execute_function("Profiler.stop", {})
	
	def _stop_precise_coverage_impl(self) -> None:
		return self._execute_function("Profiler.stopPreciseCoverage", {})
	
	def _take_precise_coverage_impl(self) -> Tuple[List[Dict[str, Any]], float]:
		return self._execute_function("Profiler.takePreciseCoverage", {})
