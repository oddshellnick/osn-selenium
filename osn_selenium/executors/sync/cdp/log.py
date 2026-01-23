from typing import (
	Any,
	Callable,
	Dict,
	List
)
from osn_selenium.executors.unified.cdp.log import (
	UnifiedLogCDPExecutor
)
from osn_selenium.abstract.executors.cdp.log import (
	AbstractLogCDPExecutor
)


__all__ = ["LogCDPExecutor"]


class LogCDPExecutor(UnifiedLogCDPExecutor, AbstractLogCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedLogCDPExecutor.__init__(self, execute_function=execute_function)
	
	def clear(self) -> None:
		return self._clear_impl()
	
	def disable(self) -> None:
		return self._disable_impl()
	
	def enable(self) -> None:
		return self._enable_impl()
	
	def start_violations_report(self, config: List[Dict[str, Any]]) -> None:
		return self._start_violations_report_impl(config=config)
	
	def stop_violations_report(self) -> None:
		return self._stop_violations_report_impl()
