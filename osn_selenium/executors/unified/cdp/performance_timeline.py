from typing import (
	Any,
	Callable,
	Dict,
	List
)


__all__ = ["UnifiedPerformanceTimelineCDPExecutor"]


class UnifiedPerformanceTimelineCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _enable_impl(self, event_types: List[str]) -> None:
		return self._execute_function("PerformanceTimeline.enable", {"event_types": event_types})
