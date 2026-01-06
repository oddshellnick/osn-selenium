from typing import Any, List
from osn_selenium.webdrivers.sync.base.base import BaseMixin
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.abstract.webdriver.base.file import AbstractFileMixin


class FileMixin(BaseMixin, AbstractFileMixin):
	@requires_driver
	def delete_downloadable_files(self) -> None:
		self.driver.delete_downloadable_files()
	
	@requires_driver
	def download_file(self, file_name: str, target_directory: str) -> None:
		self.driver.download_file(file_name=file_name, target_directory=target_directory,)
	
	@requires_driver
	def file_detector(self) -> Any:
		return self.driver.file_detector
	
	@requires_driver
	def get_downloadable_files(self) -> List[str]:
		return self.driver.get_downloadable_files()
	
	@requires_driver
	def set_file_detector(self, detector: Any) -> None:
		setattr(self.driver, "file_detector", detector)
