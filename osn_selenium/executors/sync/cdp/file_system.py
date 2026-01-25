from typing import Any, Callable, Dict
from osn_selenium.executors.unified.cdp.file_system import (
	UnifiedFileSystemCDPExecutor
)
from osn_selenium.abstract.executors.cdp.file_system import (
	AbstractFileSystemCDPExecutor
)


__all__ = ["FileSystemCDPExecutor"]


class FileSystemCDPExecutor(UnifiedFileSystemCDPExecutor, AbstractFileSystemCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedFileSystemCDPExecutor.__init__(self, execute_function=execute_function)
	
	def get_directory(self, bucket_file_system_locator: Dict[str, Any]) -> Dict[str, Any]:
		return self._get_directory_impl(bucket_file_system_locator=bucket_file_system_locator)
