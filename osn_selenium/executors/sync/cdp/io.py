from typing import (
	Any,
	Callable,
	Dict,
	Optional,
	Tuple
)
from osn_selenium.abstract.executors.cdp.io import (
	AbstractIoCDPExecutor
)


class IoCDPExecutor(AbstractIoCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def close(self, handle: str) -> None:
		return self._execute_function("IO.close", locals())
	
	def read(
			self,
			handle: str,
			offset: Optional[int] = None,
			size: Optional[int] = None
	) -> Tuple[Optional[bool]]:
		return self._execute_function("IO.read", locals())
	
	def resolve_blob(self, object_id: str) -> str:
		return self._execute_function("IO.resolveBlob", locals())
