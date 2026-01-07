from typing import (
	Any,
	Callable,
	Coroutine,
	Dict
)
from osn_selenium.abstract.executors.cdp.media import (
	AbstractMediaCDPExecutor
)


class MediaCDPExecutor(AbstractMediaCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def disable(self) -> None:
		return await self._execute_function("Media.disable", locals())
	
	async def enable(self) -> None:
		return await self._execute_function("Media.enable", locals())
