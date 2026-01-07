from typing import (
	Any,
	Callable,
	Dict,
	List,
	Tuple
)
from osn_selenium.abstract.executors.cdp.system_info import (
	AbstractSystemInfoCDPExecutor
)


class SystemInfoCDPExecutor(AbstractSystemInfoCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def get_feature_state(self, feature_state: str) -> bool:
		return self._execute_function("SystemInfo.getFeatureState", locals())
	
	def get_info(self) -> Tuple[Any, str, str, str]:
		return self._execute_function("SystemInfo.getInfo", locals())
	
	def get_process_info(self) -> List[Any]:
		return self._execute_function("SystemInfo.getProcessInfo", locals())
