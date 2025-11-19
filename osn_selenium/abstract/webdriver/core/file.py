from typing import Any, List
from abc import ABC, abstractmethod


__all__ = ["AbstractCoreFileMixin"]


class AbstractCoreFileMixin(ABC):
	"""
	Mixin responsible for browser-level file handling and detection.
	"""
	
	@abstractmethod
	def delete_downloadable_files(self) -> None:
		"""
		Deletes all files currently available for download in the browser session.
		"""
		
		...
	
	@abstractmethod
	def download_file(self, file_name: str, target_directory: str) -> None:
		"""
		Downloads a specified file from the browser to a local target directory.

		Args:
			file_name (str): The name of the file to download.
			target_directory (str): The absolute path to the local directory.
		"""
		
		...
	
	@property
	@abstractmethod
	def file_detector(self) -> Any:
		"""
		Gets the file detector used for uploading files to the remote server.

		Returns:
			Any: The file detector instance.
		"""
		
		...
	
	@file_detector.setter
	@abstractmethod
	def file_detector(self, value: Any) -> None:
		"""
		Sets the file detector for the current session.

		Args:
			value (Any): The new file detector instance.
		"""
		
		...
	
	@abstractmethod
	def file_detector_context(self, file_detector_class: Any, *args: Any, **kwargs: Any) -> Any:
		"""
		Context manager to temporarily use a specific file detector.

		Args:
			file_detector_class (Any): The class of the file detector to use.
			*args (Any): Variable positional arguments for the detector.
			**kwargs (Any): Variable keyword arguments for the detector.

		Returns:
			Any: The context manager instance.
		"""
		
		...
	
	@abstractmethod
	def get_downloadable_files(self) -> List[str]:
		"""
		Gets a list of files available for download from the browser.

		Returns:
			List[str]: A list of downloadable file names.
		"""
		
		...
