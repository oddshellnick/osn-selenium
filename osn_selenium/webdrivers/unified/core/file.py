from contextlib import contextmanager
from typing import Any, Generator, List
from osn_selenium.webdrivers._decorators import requires_driver
from osn_selenium.webdrivers.unified.core.base import UnifiedCoreBaseMixin


__all__ = ["UnifiedCoreFileMixin"]


class UnifiedCoreFileMixin(UnifiedCoreBaseMixin):
	@requires_driver
	def _delete_downloadable_files_impl(self) -> None:
		self._driver_impl.delete_downloadable_files()
	
	@requires_driver
	def _download_file_impl(self, file_name: str, target_directory: str) -> None:
		self._driver_impl.download_file(file_name=file_name, target_directory=target_directory)
	
	@contextmanager
	@requires_driver
	def _file_detector_context_impl(self, file_detector_class: Any, *args: Any, **kwargs: Any) -> Generator[None, Any, None]:
		with self._driver_impl.file_detector_context(file_detector_class, *args, **kwargs) as file_detector:
			yield file_detector
	
	@requires_driver
	def _file_detector_get_impl(self) -> Any:
		return self._driver_impl.file_detector
	
	@requires_driver
	def _file_detector_set_impl(self, value: Any) -> None:
		self._driver_impl.file_detector = value
	
	@requires_driver
	def _get_downloadable_files_impl(self) -> List[str]:
		return self._driver_impl.get_downloadable_files()
