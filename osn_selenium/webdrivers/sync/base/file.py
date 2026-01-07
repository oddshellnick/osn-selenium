from contextlib import contextmanager
from typing import Any, Generator, List
from osn_selenium.webdrivers.sync.base.base import BaseMixin
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.abstract.webdriver.base.file import AbstractFileMixin


class FileMixin(BaseMixin, AbstractFileMixin):
	@requires_driver
	def delete_downloadable_files(self) -> None:
		self.driver.delete_downloadable_files()
	
	@requires_driver
	def download_file(self, file_name: str, target_directory: str) -> None:
		self.driver.download_file(file_name=file_name, target_directory=target_directory)
	
	@property
	@requires_driver
	def file_detector(self) -> Any:
		return self.driver.file_detector
	
	@file_detector.setter
	@requires_driver
	def file_detector(self, value: Any) -> None:
		self.driver.file_detector = value
	
	@contextmanager
	@requires_driver
	def file_detector_context(self, file_detector_class: Any, *args: Any, **kwargs: Any) -> Generator[None, Any, None]:
		with self.driver.file_detector_context(file_detector_class, *args, **kwargs) as file_detector:
			yield file_detector
	
	@requires_driver
	def get_downloadable_files(self) -> List[str]:
		return self.driver.get_downloadable_files()
