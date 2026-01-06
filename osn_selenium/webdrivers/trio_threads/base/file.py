from typing import Any, List
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.webdrivers.trio_threads.base.base import BaseMixin
from osn_selenium.abstract.webdriver.base.file import AbstractFileMixin


class FileMixin(BaseMixin, AbstractFileMixin):
	@requires_driver
	async def delete_downloadable_files(self) -> None:
		await self._wrap_to_trio(self.driver.delete_downloadable_files)
	
	@requires_driver
	async def download_file(self, file_name: str, target_directory: str) -> None:
		await self._wrap_to_trio(
				self.driver.download_file,
				file_name=file_name,
				target_directory=target_directory,
		)
	
	@requires_driver
	async def file_detector(self) -> Any:
		return await self._wrap_to_trio(lambda: self.driver.file_detector)
	
	@requires_driver
	async def get_downloadable_files(self) -> List[str]:
		return await self._wrap_to_trio(self.driver.get_downloadable_files)
	
	@requires_driver
	async def set_file_detector(self, detector: Any) -> None:
		await self._wrap_to_trio(lambda: setattr(self.driver, "file_detector", detector))
