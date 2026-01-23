from typing import Any, Callable, Dict
from osn_selenium.executors.unified.cdp.device_access import (
	UnifiedDeviceAccessCDPExecutor
)
from osn_selenium.abstract.executors.cdp.device_access import (
	AbstractDeviceAccessCDPExecutor
)


__all__ = ["DeviceAccessCDPExecutor"]


class DeviceAccessCDPExecutor(UnifiedDeviceAccessCDPExecutor, AbstractDeviceAccessCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedDeviceAccessCDPExecutor.__init__(self, execute_function=execute_function)
	
	def cancel_prompt(self, id_: str) -> None:
		return self._cancel_prompt_impl(id_=id_)
	
	def disable(self) -> None:
		return self._disable_impl()
	
	def enable(self) -> None:
		return self._enable_impl()
	
	def select_prompt(self, id_: str, device_id: str) -> None:
		return self._select_prompt_impl(id_=id_, device_id=device_id)
