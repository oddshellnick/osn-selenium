from typing import (
	Any,
	Callable,
	Dict,
	List
)
from osn_selenium.abstract.executors.cdp.filesystem import (
	AbstractFileSystemCDPExecutor
)


class FileSystemCDPExecutor(AbstractFileSystemCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def get_directory(self, bucket_file_system_locator: List[str]) -> List[Any]:
		return self._execute_function("FileSystem.getDirectory", locals())
