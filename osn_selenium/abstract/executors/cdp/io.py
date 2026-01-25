from typing import Optional, Tuple
from abc import ABC, abstractmethod


__all__ = ["AbstractIoCDPExecutor"]


class AbstractIoCDPExecutor(ABC):
	@abstractmethod
	def close(self, handle: str) -> None:
		...
	
	@abstractmethod
	def read(
			self,
			handle: str,
			offset: Optional[int] = None,
			size: Optional[int] = None
	) -> Tuple[Optional[bool], str, bool]:
		...
	
	@abstractmethod
	def resolve_blob(self, object_id: str) -> str:
		...
