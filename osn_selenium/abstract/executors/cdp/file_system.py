from typing import Any, Dict
from abc import ABC, abstractmethod


__all__ = ["AbstractFileSystemCDPExecutor"]


class AbstractFileSystemCDPExecutor(ABC):
	@abstractmethod
	def get_directory(self, bucket_file_system_locator: Dict[str, Any]) -> Dict[str, Any]:
		...
