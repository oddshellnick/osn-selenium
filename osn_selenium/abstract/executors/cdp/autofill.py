from abc import ABC, abstractmethod
from typing import Any, List, Optional


class AbstractAutofillCDPExecutor(ABC):
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def enable(self) -> None:
		...
	
	@abstractmethod
	def set_addresses(self, addresses: List[List[Any]]) -> None:
		...
	
	@abstractmethod
	def trigger(
			self,
			field_id: int,
			frame_id: Optional[str] = None,
			card: Optional[Any] = None,
			address: Optional[List[Any]] = None
	) -> None:
		...
