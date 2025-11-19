from typing import Any, Callable, Dict
from osn_selenium.executors.unified.cdp.inspector import (
	UnifiedInspectorCDPExecutor
)
from osn_selenium.abstract.executors.cdp.inspector import (
	AbstractInspectorCDPExecutor
)


__all__ = ["InspectorCDPExecutor"]


class InspectorCDPExecutor(UnifiedInspectorCDPExecutor, AbstractInspectorCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedInspectorCDPExecutor.__init__(self, execute_function=execute_function)
	
	def disable(self) -> None:
		return self._disable_impl()
	
	def enable(self) -> None:
		return self._enable_impl()
