from typing import (
	Any,
	Callable,
	Dict,
	Optional,
	Tuple
)
from osn_selenium.executors.unified.cdp.io import UnifiedIoCDPExecutor
from osn_selenium.abstract.executors.cdp.io import (
	AbstractIoCDPExecutor
)


__all__ = ["IoCDPExecutor"]


class IoCDPExecutor(UnifiedIoCDPExecutor, AbstractIoCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedIoCDPExecutor.__init__(self, execute_function=execute_function)
	
	def close(self, handle: str) -> None:
		return self._close_impl(handle=handle)
	
	def read(
			self,
			handle: str,
			offset: Optional[int] = None,
			size: Optional[int] = None
	) -> Tuple[Optional[bool], str, bool]:
		return self._read_impl(handle=handle, offset=offset, size=size)
	
	def resolve_blob(self, object_id: str) -> str:
		return self._resolve_blob_impl(object_id=object_id)
