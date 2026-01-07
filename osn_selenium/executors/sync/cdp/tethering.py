from typing import Any, Callable, Dict
from osn_selenium.abstract.executors.cdp.tethering import (
	AbstractTetheringCDPExecutor
)


class TetheringCDPExecutor(AbstractTetheringCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def bind(self, port: int) -> None:
		return self._execute_function("Tethering.bind", locals())
	
	def unbind(self, port: int) -> None:
		return self._execute_function("Tethering.unbind", locals())
