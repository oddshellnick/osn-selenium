from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	Optional
)
from osn_selenium.abstract.executors.cdp.cast import (
	AbstractCastCDPExecutor
)


class CastCDPExecutor(AbstractCastCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def disable(self) -> None:
		return await self._execute_function("Cast.disable", locals())
	
	async def enable(self, presentation_url: Optional[str] = None) -> None:
		return await self._execute_function("Cast.enable", locals())
	
	async def set_sink_to_use(self, sink_name: str) -> None:
		return await self._execute_function("Cast.setSinkToUse", locals())
	
	async def start_desktop_mirroring(self, sink_name: str) -> None:
		return await self._execute_function("Cast.startDesktopMirroring", locals())
	
	async def start_tab_mirroring(self, sink_name: str) -> None:
		return await self._execute_function("Cast.startTabMirroring", locals())
	
	async def stop_casting(self, sink_name: str) -> None:
		return await self._execute_function("Cast.stopCasting", locals())
