from typing import (
	Any,
	Callable,
	Coroutine,
	Dict
)
from osn_selenium.abstract.executors.cdp.deviceaccess import (
	AbstractDeviceAccessCDPExecutor
)


class AsyncDeviceAccessCDPExecutor(AbstractDeviceAccessCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def cancel_prompt(self, id_: str) -> None:
		return await self._execute_function("DeviceAccess.cancelPrompt", locals())
	
	async def disable(self) -> None:
		return await self._execute_function("DeviceAccess.disable", locals())
	
	async def enable(self) -> None:
		return await self._execute_function("DeviceAccess.enable", locals())
	
	async def select_prompt(self, id_: str, device_id: str) -> None:
		return await self._execute_function("DeviceAccess.selectPrompt", locals())
