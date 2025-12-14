from typing import Any, Callable, Dict
from osn_selenium.abstract.executors.cdp.file_system import (
	AbstractFileSystemCDPExecutor
)


class FileSystemCDPExecutor(AbstractFileSystemCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def get_directory(self, bucket_file_system_locator: Any) -> Any:
		return self._execute_function("FileSystem.getDirectory", locals())
