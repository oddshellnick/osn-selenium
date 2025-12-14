from typing import Any, Callable, Dict
from osn_selenium.abstract.executors.cdp.inspector import (
	AbstractInspectorCDPExecutor
)


class InspectorCDPExecutor(AbstractInspectorCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def disable(self) -> None:
		return self._execute_function("Inspector.disable", locals())
	
	def enable(self) -> None:
		return self._execute_function("Inspector.enable", locals())
