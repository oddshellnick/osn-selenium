from typing import (
	Any,
	Callable,
	Dict,
	List
)
from osn_selenium.executors.unified.cdp.performance_timeline import (
	UnifiedPerformanceTimelineCDPExecutor
)
from osn_selenium.abstract.executors.cdp.performance_timeline import (
	AbstractPerformanceTimelineCDPExecutor
)


__all__ = ["PerformanceTimelineCDPExecutor"]


class PerformanceTimelineCDPExecutor(
		UnifiedPerformanceTimelineCDPExecutor,
		AbstractPerformanceTimelineCDPExecutor
):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedPerformanceTimelineCDPExecutor.__init__(self, execute_function=execute_function)
	
	def enable(self, event_types: List[str]) -> None:
		return self._enable_impl(event_types=event_types)
