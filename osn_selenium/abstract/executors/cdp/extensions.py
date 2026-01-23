from abc import ABC, abstractmethod
from typing import Any, List, Optional


__all__ = ["AbstractExtensionsCDPExecutor"]


class AbstractExtensionsCDPExecutor(ABC):
	@abstractmethod
	def clear_storage_items(self, id_: str, storage_area: str) -> None:
		...
	
	@abstractmethod
	def get_storage_items(self, id_: str, storage_area: str, keys: Optional[List[str]] = None) -> Any:
		...
	
	@abstractmethod
	def load_unpacked(self, path: str) -> str:
		...
	
	@abstractmethod
	def remove_storage_items(self, id_: str, storage_area: str, keys: List[str]) -> None:
		...
	
	@abstractmethod
	def set_storage_items(self, id_: str, storage_area: str, values: Any) -> None:
		...
	
	@abstractmethod
	def uninstall(self, id_: str) -> None:
		...
