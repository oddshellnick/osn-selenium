from abc import ABC, abstractmethod
from typing import Any, Optional, Tuple


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
	) -> Tuple[Optional[bool]]:
		...
	
	@abstractmethod
	def resolve_blob(self, object_id: str) -> str:
		...
