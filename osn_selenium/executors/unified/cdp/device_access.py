from typing import Any, Callable, Dict


__all__ = ["UnifiedDeviceAccessCDPExecutor"]


class UnifiedDeviceAccessCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _cancel_prompt_impl(self, id_: str) -> None:
		return self._execute_function("DeviceAccess.cancelPrompt", {"id_": id_})
	
	def _disable_impl(self) -> None:
		return self._execute_function("DeviceAccess.disable", {})
	
	def _enable_impl(self) -> None:
		return self._execute_function("DeviceAccess.enable", {})
	
	def _select_prompt_impl(self, id_: str, device_id: str) -> None:
		return self._execute_function("DeviceAccess.selectPrompt", {"id_": id_, "device_id": device_id})
