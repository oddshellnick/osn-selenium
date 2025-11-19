from typing import (
	Any,
	Callable,
	Dict,
	List
)


__all__ = ["UnifiedSchemaCDPExecutor"]


class UnifiedSchemaCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _get_domains_impl(self) -> List[Dict[str, Any]]:
		return self._execute_function("Schema.getDomains", {})
