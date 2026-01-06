from typing import Any, List
from abc import ABC, abstractmethod


class AbstractFileMixin(ABC):
	"""Mixin responsible for file handling and detection."""
	
	@abstractmethod
	def delete_downloadable_files(self) -> None:
		"""
		Deletes all files currently available for download.
		"""
		
		...
	
	@abstractmethod
	def download_file(self, file_name: str, target_directory: str) -> None:
		"""
		Downloads a specified file to a target directory.

		Args:
			file_name (str): The name of the file to download.
			target_directory (str): The directory to save the file in.
		"""
		
		...
	
	@abstractmethod
	def file_detector(self) -> Any:
		"""
		Gets the file detector for the current session.

		Returns:
			Any: The file detector instance.
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
	
	@abstractmethod
	def set_file_detector(self, detector: Any) -> None:
		"""
		Sets the file detector for the driver.

		Args:
			detector (Any): The file detector to use.
		"""
		
		...
