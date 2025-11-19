from typing import Any, Callable, Dict


__all__ = ["UnifiedFileSystemCDPExecutor"]


class UnifiedFileSystemCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _get_directory_impl(self, bucket_file_system_locator: Dict[str, Any]) -> Dict[str, Any]:
		return self._execute_function(
				"FileSystem.getDirectory",
				{"bucket_file_system_locator": bucket_file_system_locator}
		)
