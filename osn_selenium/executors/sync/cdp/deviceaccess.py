from typing import Any, Callable, Dict
from osn_selenium.abstract.executors.cdp.deviceaccess import (
	AbstractDeviceAccessCDPExecutor
)


class DeviceAccessCDPExecutor(AbstractDeviceAccessCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def cancel_prompt(self, id_: str) -> None:
		return self._execute_function("DeviceAccess.cancelPrompt", locals())
	
	def disable(self) -> None:
		return self._execute_function("DeviceAccess.disable", locals())
	
	def enable(self) -> None:
		return self._execute_function("DeviceAccess.enable", locals())
	
	def select_prompt(self, id_: str, device_id: str) -> None:
		return self._execute_function("DeviceAccess.selectPrompt", locals())
