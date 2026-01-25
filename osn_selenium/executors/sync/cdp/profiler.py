from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.executors.unified.cdp.profiler import (
	UnifiedProfilerCDPExecutor
)
from osn_selenium.abstract.executors.cdp.profiler import (
	AbstractProfilerCDPExecutor
)


__all__ = ["ProfilerCDPExecutor"]


class ProfilerCDPExecutor(UnifiedProfilerCDPExecutor, AbstractProfilerCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedProfilerCDPExecutor.__init__(self, execute_function=execute_function)
	
	def disable(self) -> None:
		return self._disable_impl()
	
	def enable(self) -> None:
		return self._enable_impl()
	
	def get_best_effort_coverage(self) -> List[Dict[str, Any]]:
		return self._get_best_effort_coverage_impl()
	
	def set_sampling_interval(self, interval: int) -> None:
		return self._set_sampling_interval_impl(interval=interval)
	
	def start(self) -> None:
		return self._start_impl()
	
	def start_precise_coverage(
			self,
			call_count: Optional[bool] = None,
			detailed: Optional[bool] = None,
			allow_triggered_updates: Optional[bool] = None
	) -> float:
		return self._start_precise_coverage_impl(
				call_count=call_count,
				detailed=detailed,
				allow_triggered_updates=allow_triggered_updates
		)
	
	def stop(self) -> Dict[str, Any]:
		return self._stop_impl()
	
	def stop_precise_coverage(self) -> None:
		return self._stop_precise_coverage_impl()
	
	def take_precise_coverage(self) -> Tuple[List[Dict[str, Any]], float]:
		return self._take_precise_coverage_impl()
