from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	Optional,
	Tuple
)
from osn_selenium.abstract.executors.cdp.io import (
	AbstractIoCDPExecutor
)


class IoCDPExecutor(AbstractIoCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def close(self, handle: str) -> None:
		return await self._execute_function("IO.close", locals())
	
	async def read(
			self,
			handle: str,
			offset: Optional[int] = None,
			size: Optional[int] = None
	) -> Tuple[Optional[bool]]:
		return await self._execute_function("IO.read", locals())
	
	async def resolve_blob(self, object_id: str) -> str:
		return await self._execute_function("IO.resolveBlob", locals())
