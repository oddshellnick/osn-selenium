from typing import Any, Dict
from abc import ABC, abstractmethod


class AbstractFileSystemCDPExecutor(ABC):
	@abstractmethod
	def get_directory(self, bucket_file_system_locator: Dict[str, Any]) -> Dict[str, Any]:
		...
