from contextlib import asynccontextmanager
from typing import (
	Any,
	AsyncGenerator,
	List
)
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.webdrivers.trio_threads.core.base import CoreBaseMixin
from osn_selenium.abstract.webdriver.core.file import AbstractCoreFileMixin


class CoreFileMixin(CoreBaseMixin, AbstractCoreFileMixin):
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
	
	@property
	@requires_driver
	def file_detector(self) -> Any:
		return self.driver.file_detector
	
	@file_detector.setter
	@requires_driver
	def file_detector(self, value: Any) -> None:
		self.driver.file_detector = value
	
	@asynccontextmanager
	@requires_driver
	async def file_detector_context(self, file_detector_class: Any, *args: Any, **kwargs: Any) -> AsyncGenerator[Any, None]:
		async with self._wrap_to_trio_context(
				self.driver.file_detector_context,
				file_detector_class,
				*args,
				**kwargs
		) as file_detector:
			yield file_detector
	
	@requires_driver
	async def get_downloadable_files(self) -> List[str]:
		return await self._wrap_to_trio(self.driver.get_downloadable_files)
