import trio
from typing import Any, Callable, Dict
from osn_selenium.base_mixin import TrioThreadMixin
from osn_selenium.executors.unified.cdp.file_system import (
	UnifiedFileSystemCDPExecutor
)
from osn_selenium.abstract.executors.cdp.file_system import (
	AbstractFileSystemCDPExecutor
)


__all__ = ["FileSystemCDPExecutor"]


class FileSystemCDPExecutor(
		UnifiedFileSystemCDPExecutor,
		TrioThreadMixin,
		AbstractFileSystemCDPExecutor
):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedFileSystemCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def get_directory(self, bucket_file_system_locator: Dict[str, Any]) -> Dict[str, Any]:
		return await self.sync_to_trio(sync_function=self._get_directory_impl)(bucket_file_system_locator=bucket_file_system_locator)
