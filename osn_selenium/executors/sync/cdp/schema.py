from typing import (
	Any,
	Callable,
	Dict,
	List
)
from osn_selenium.executors.unified.cdp.schema import (
	UnifiedSchemaCDPExecutor
)
from osn_selenium.abstract.executors.cdp.schema import (
	AbstractSchemaCDPExecutor
)


__all__ = ["SchemaCDPExecutor"]


class SchemaCDPExecutor(UnifiedSchemaCDPExecutor, AbstractSchemaCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedSchemaCDPExecutor.__init__(self, execute_function=execute_function)
	
	def get_domains(self) -> List[Dict[str, Any]]:
		return self._get_domains_impl()
