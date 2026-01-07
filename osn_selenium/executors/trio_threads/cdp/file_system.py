from typing import (
	Any,
	Callable,
	Coroutine,
	Dict
)
from osn_selenium.abstract.executors.cdp.file_system import (
	AbstractFileSystemCDPExecutor
)


class FileSystemCDPExecutor(AbstractFileSystemCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def get_directory(self, bucket_file_system_locator: Any) -> Any:
		return await self._execute_function("FileSystem.getDirectory", locals())
