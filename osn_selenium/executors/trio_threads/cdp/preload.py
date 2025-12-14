from typing import (
	Any,
	Callable,
	Coroutine,
	Dict
)
from osn_selenium.abstract.executors.cdp.preload import (
	AbstractPreloadCDPExecutor
)


class PreloadCDPExecutor(AbstractPreloadCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def disable(self) -> None:
		return await self._execute_function("Preload.disable", locals())
	
	async def enable(self) -> None:
		return await self._execute_function("Preload.enable", locals())
