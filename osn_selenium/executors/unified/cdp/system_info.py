from typing import (
	Any,
	Callable,
	Dict,
	List,
	Tuple
)


__all__ = ["UnifiedSystemInfoCDPExecutor"]


class UnifiedSystemInfoCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _get_feature_state_impl(self, feature_state: str) -> bool:
		return self._execute_function("SystemInfo.getFeatureState", {"feature_state": feature_state})
	
	def _get_info_impl(self) -> Tuple[Dict[str, Any], str, str, str]:
		return self._execute_function("SystemInfo.getInfo", {})
	
	def _get_process_info_impl(self) -> List[Dict[str, Any]]:
		return self._execute_function("SystemInfo.getProcessInfo", {})
