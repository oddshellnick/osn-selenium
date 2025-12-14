from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	List,
	Tuple
)
from osn_selenium.abstract.executors.cdp.systeminfo import (
	AbstractSystemInfoCDPExecutor
)


class AsyncSystemInfoCDPExecutor(AbstractSystemInfoCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def get_feature_state(self, feature_state: str) -> bool:
		return await self._execute_function("SystemInfo.getFeatureState", locals())
	
	async def get_info(self) -> Tuple[List[Any]]:
		return await self._execute_function("SystemInfo.getInfo", locals())
	
	async def get_process_info(self) -> List[Any]:
		return await self._execute_function("SystemInfo.getProcessInfo", locals())
