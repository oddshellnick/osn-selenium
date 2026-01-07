from typing import Any
from abc import ABC, abstractmethod


class AbstractFileSystemCDPExecutor(ABC):
	@abstractmethod
	def get_directory(self, bucket_file_system_locator: Any) -> Any:
		...
