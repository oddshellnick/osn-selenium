from typing import (
	Any,
	Callable,
	Coroutine,
	Dict
)
from osn_selenium.abstract.executors.cdp.web_audio import (
	AbstractWebAudioCDPExecutor
)


class WebAudioCDPExecutor(AbstractWebAudioCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def disable(self) -> None:
		return await self._execute_function("WebAudio.disable", locals())
	
	async def enable(self) -> None:
		return await self._execute_function("WebAudio.enable", locals())
	
	async def get_realtime_data(self, context_id: str) -> Any:
		return await self._execute_function("WebAudio.getRealtimeData", locals())
