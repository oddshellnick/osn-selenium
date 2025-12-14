from typing import Any, List
from abc import ABC, abstractmethod


class AbstractDomStorageCDPExecutor(ABC):
	@abstractmethod
	def clear(self, storage_id: Any) -> None:
		...
	
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def enable(self) -> None:
		...
	
	@abstractmethod
	def get_dom_storage_items(self, storage_id: Any) -> List[List[Any]]:
		...
	
	@abstractmethod
	def remove_dom_storage_item(self, storage_id: Any, key: str) -> None:
		...
	
	@abstractmethod
	def set_dom_storage_item(self, storage_id: Any, key: str, value: str) -> None:
		...
