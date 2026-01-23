from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional
)
from osn_selenium.executors.unified.cdp.performance import (
	UnifiedPerformanceCDPExecutor
)
from osn_selenium.abstract.executors.cdp.performance import (
	AbstractPerformanceCDPExecutor
)


__all__ = ["PerformanceCDPExecutor"]


class PerformanceCDPExecutor(UnifiedPerformanceCDPExecutor, AbstractPerformanceCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedPerformanceCDPExecutor.__init__(self, execute_function=execute_function)
	
	def disable(self) -> None:
		return self._disable_impl()
	
	def enable(self, time_domain: Optional[str] = None) -> None:
		return self._enable_impl(time_domain=time_domain)
	
	def get_metrics(self) -> List[Dict[str, Any]]:
		return self._get_metrics_impl()
	
	def set_time_domain(self, time_domain: str) -> None:
		return self._set_time_domain_impl(time_domain=time_domain)
