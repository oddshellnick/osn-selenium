from contextlib import contextmanager
from typing import Any, Generator, List
from osn_selenium.webdrivers.unified.core.file import UnifiedCoreFileMixin
from osn_selenium.abstract.webdriver.core.file import (
	AbstractCoreFileMixin
)


__all__ = ["CoreFileMixin"]


class CoreFileMixin(UnifiedCoreFileMixin, AbstractCoreFileMixin):
	"""
	Mixin for file system interactions within Core WebDrivers.

	Manages file upload detection, download verification, and cleanup of
	downloaded files.
	"""
	
	def delete_downloadable_files(self) -> None:
		self._delete_downloadable_files_impl()
	
	def download_file(self, file_name: str, target_directory: str) -> None:
		self._download_file_impl(file_name=file_name, target_directory=target_directory)
	
	@property
	def file_detector(self) -> Any:
		return self._file_detector_get_impl()
	
	@file_detector.setter
	def file_detector(self, value: Any) -> None:
		self._file_detector_set_impl(value)
	
	@contextmanager
	def file_detector_context(self, file_detector_class: Any, *args: Any, **kwargs: Any) -> Generator[None, Any, None]:
		with self._file_detector_context_impl(file_detector_class, *args, **kwargs) as file_detector:
			yield file_detector
	
	def get_downloadable_files(self) -> List[str]:
		return self._get_downloadable_files_impl()
