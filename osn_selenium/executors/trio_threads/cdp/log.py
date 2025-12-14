from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	List
)
from osn_selenium.abstract.executors.cdp.log import (
	AbstractLogCDPExecutor
)


class LogCDPExecutor(AbstractLogCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def clear(self) -> None:
		return await self._execute_function("Log.clear", locals())
	
	async def disable(self) -> None:
		return await self._execute_function("Log.disable", locals())
	
	async def enable(self) -> None:
		return await self._execute_function("Log.enable", locals())
	
	async def start_violations_report(self, config: List[Any]) -> None:
		return await self._execute_function("Log.startViolationsReport", locals())
	
	async def stop_violations_report(self) -> None:
		return await self._execute_function("Log.stopViolationsReport", locals())
