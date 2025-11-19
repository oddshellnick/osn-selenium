from typing import (
	Any,
	Callable,
	Dict,
	Optional,
	Tuple
)


__all__ = ["UnifiedIoCDPExecutor"]


class UnifiedIoCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _close_impl(self, handle: str) -> None:
		return self._execute_function("IO.close", {"handle": handle})
	
	def _read_impl(
			self,
			handle: str,
			offset: Optional[int] = None,
			size: Optional[int] = None
	) -> Tuple[Optional[bool], str, bool]:
		return self._execute_function("IO.read", {"handle": handle, "offset": offset, "size": size})
	
	def _resolve_blob_impl(self, object_id: str) -> str:
		return self._execute_function("IO.resolveBlob", {"object_id": object_id})
