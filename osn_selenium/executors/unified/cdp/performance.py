from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional
)


__all__ = ["UnifiedPerformanceCDPExecutor"]


class UnifiedPerformanceCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _disable_impl(self) -> None:
		return self._execute_function("Performance.disable", {})
	
	def _enable_impl(self, time_domain: Optional[str] = None) -> None:
		return self._execute_function("Performance.enable", {"time_domain": time_domain})
	
	def _get_metrics_impl(self) -> List[Dict[str, Any]]:
		return self._execute_function("Performance.getMetrics", {})
	
	def _set_time_domain_impl(self, time_domain: str) -> None:
		return self._execute_function("Performance.setTimeDomain", {"time_domain": time_domain})
