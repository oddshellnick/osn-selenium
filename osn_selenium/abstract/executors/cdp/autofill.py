from abc import ABC, abstractmethod
from typing import (
	Any,
	Dict,
	List,
	Optional
)


__all__ = ["AbstractAutofillCDPExecutor"]


class AbstractAutofillCDPExecutor(ABC):
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def enable(self) -> None:
		...
	
	@abstractmethod
	def set_addresses(self, addresses: List[Dict[str, Any]]) -> None:
		...
	
	@abstractmethod
	def trigger(
			self,
			field_id: int,
			frame_id: Optional[str] = None,
			card: Optional[Dict[str, Any]] = None,
			address: Optional[Dict[str, Any]] = None
	) -> None:
		...
