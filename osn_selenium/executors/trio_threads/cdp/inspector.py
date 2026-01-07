from typing import (
	Any,
	Callable,
	Coroutine,
	Dict
)
from osn_selenium.abstract.executors.cdp.inspector import (
	AbstractInspectorCDPExecutor
)


class InspectorCDPExecutor(AbstractInspectorCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def disable(self) -> None:
		return await self._execute_function("Inspector.disable", locals())
	
	async def enable(self) -> None:
		return await self._execute_function("Inspector.enable", locals())
