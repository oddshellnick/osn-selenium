from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	List
)
from osn_selenium.abstract.executors.cdp.schema import (
	AbstractSchemaCDPExecutor
)


class SchemaCDPExecutor(AbstractSchemaCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def get_domains(self) -> List[Any]:
		return await self._execute_function("Schema.getDomains", locals())
