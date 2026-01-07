from typing import Any, List
from abc import ABC, abstractmethod


class AbstractFileSystemCDPExecutor(ABC):
	@abstractmethod
	def get_directory(self, bucket_file_system_locator: List[str]) -> List[Any]:
		...
