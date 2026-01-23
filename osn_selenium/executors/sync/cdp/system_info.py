from typing import (
	Any,
	Callable,
	Dict,
	List,
	Tuple
)
from osn_selenium.executors.unified.cdp.system_info import (
	UnifiedSystemInfoCDPExecutor
)
from osn_selenium.abstract.executors.cdp.system_info import (
	AbstractSystemInfoCDPExecutor
)


__all__ = ["SystemInfoCDPExecutor"]


class SystemInfoCDPExecutor(UnifiedSystemInfoCDPExecutor, AbstractSystemInfoCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedSystemInfoCDPExecutor.__init__(self, execute_function=execute_function)
	
	def get_feature_state(self, feature_state: str) -> bool:
		return self._get_feature_state_impl(feature_state=feature_state)
	
	def get_info(self) -> Tuple[Dict[str, Any], str, str, str]:
		return self._get_info_impl()
	
	def get_process_info(self) -> List[Dict[str, Any]]:
		return self._get_process_info_impl()
