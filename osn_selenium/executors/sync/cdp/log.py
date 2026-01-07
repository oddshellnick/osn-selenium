from typing import (
	Any,
	Callable,
	Dict,
	List
)
from osn_selenium.abstract.executors.cdp.log import (
	AbstractLogCDPExecutor
)


class LogCDPExecutor(AbstractLogCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def clear(self) -> None:
		return self._execute_function("Log.clear", locals())
	
	def disable(self) -> None:
		return self._execute_function("Log.disable", locals())
	
	def enable(self) -> None:
		return self._execute_function("Log.enable", locals())
	
	def start_violations_report(self, config: List[Any]) -> None:
		return self._execute_function("Log.startViolationsReport", locals())
	
	def stop_violations_report(self) -> None:
		return self._execute_function("Log.stopViolationsReport", locals())
