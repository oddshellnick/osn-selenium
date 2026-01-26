from contextlib import asynccontextmanager
from typing import (
	Any,
	AsyncGenerator,
	List
)
from osn_selenium.trio_threads_mixin import TrioThreadMixin
from osn_selenium.webdrivers.unified.core.file import UnifiedCoreFileMixin
from osn_selenium.abstract.webdriver.core.file import (
	AbstractCoreFileMixin
)


__all__ = ["CoreFileMixin"]


class CoreFileMixin(UnifiedCoreFileMixin, TrioThreadMixin, AbstractCoreFileMixin):
	"""
	Mixin for file system interactions within Core WebDrivers.

	Manages file upload detection, download verification, and cleanup of
	downloaded files.
	"""
	
	async def delete_downloadable_files(self) -> None:
		await self.sync_to_trio(sync_function=self._delete_downloadable_files_impl)()
	
	async def download_file(self, file_name: str, target_directory: str) -> None:
		await self.sync_to_trio(sync_function=self._download_file_impl)(file_name=file_name, target_directory=target_directory)
	
	@property
	async def file_detector(self) -> Any:
		return await self.sync_to_trio(sync_function=self._file_detector_get_impl)()
	
	@file_detector.setter
	async def file_detector(self, value: Any) -> None:
		await self.sync_to_trio(sync_function=self._file_detector_set_impl)(value=value)
	
	@asynccontextmanager
	async def file_detector_context(self, file_detector_class: Any, *args: Any, **kwargs: Any) -> AsyncGenerator[Any, Any]:
		async with self.sync_to_trio_context(context_manager_factory=self._file_detector_context_impl)(file_detector_class, *args, **kwargs) as file_detector:
			yield file_detector
	
	async def get_downloadable_files(self) -> List[str]:
		return await self.sync_to_trio(sync_function=self._get_downloadable_files_impl)()
