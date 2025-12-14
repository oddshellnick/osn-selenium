from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional
)
from osn_selenium.abstract.executors.cdp.performance import (
	AbstractPerformanceCDPExecutor
)


class PerformanceCDPExecutor(AbstractPerformanceCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def disable(self) -> None:
		return self._execute_function("Performance.disable", locals())
	
	def enable(self, time_domain: Optional[str] = None) -> None:
		return self._execute_function("Performance.enable", locals())
	
	def get_metrics(self) -> List[Any]:
		return self._execute_function("Performance.getMetrics", locals())
	
	def set_time_domain(self, time_domain: str) -> None:
		return self._execute_function("Performance.setTimeDomain", locals())
