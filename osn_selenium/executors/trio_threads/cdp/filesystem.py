from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	List
)
from osn_selenium.abstract.executors.cdp.filesystem import (
	AbstractFileSystemCDPExecutor
)


class AsyncFileSystemCDPExecutor(AbstractFileSystemCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def get_directory(self, bucket_file_system_locator: List[str]) -> List[Any]:
		return await self._execute_function("FileSystem.getDirectory", locals())
