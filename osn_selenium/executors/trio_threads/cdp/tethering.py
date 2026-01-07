from typing import (
	Any,
	Callable,
	Coroutine,
	Dict
)
from osn_selenium.abstract.executors.cdp.tethering import (
	AbstractTetheringCDPExecutor
)


class TetheringCDPExecutor(AbstractTetheringCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def bind(self, port: int) -> None:
		return await self._execute_function("Tethering.bind", locals())
	
	async def unbind(self, port: int) -> None:
		return await self._execute_function("Tethering.unbind", locals())
