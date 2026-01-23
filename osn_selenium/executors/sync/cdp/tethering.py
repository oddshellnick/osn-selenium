from typing import Any, Callable, Dict
from osn_selenium.executors.unified.cdp.tethering import (
	UnifiedTetheringCDPExecutor
)
from osn_selenium.abstract.executors.cdp.tethering import (
	AbstractTetheringCDPExecutor
)


__all__ = ["TetheringCDPExecutor"]


class TetheringCDPExecutor(UnifiedTetheringCDPExecutor, AbstractTetheringCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedTetheringCDPExecutor.__init__(self, execute_function=execute_function)
	
	def bind(self, port: int) -> None:
		return self._bind_impl(port=port)
	
	def unbind(self, port: int) -> None:
		return self._unbind_impl(port=port)
