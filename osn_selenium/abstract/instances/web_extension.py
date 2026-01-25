from abc import ABC, abstractmethod
from typing import (
	Any,
	Mapping,
	Optional,
	Union
)
from selenium.webdriver.common.bidi.webextension import (
	WebExtension as legacyWebExtension
)


__all__ = ["AbstractWebExtension"]


class AbstractWebExtension(ABC):
	"""
	Abstract base class for managing browser extensions.

	Defines the interface for installing and uninstalling web extensions.
	"""
	
	@abstractmethod
	def install(
			self,
			path: Optional[str] = None,
			archive_path: Optional[str] = None,
			base64_value: Optional[str] = None,
	) -> Mapping[str, Any]:
		"""
		Installs a web extension.

		Args:
			path (Optional[str]): Path to the extension file (.crx or .xpi).
			archive_path (Optional[str]): Path to a zipped extension directory.
			base64_value (Optional[str]): Base64 encoded extension data.

		Returns:
			Mapping[str, Any]: A dictionary containing the result of the installation,
							   typically including the extension ID.
		"""
		
		...
	
	@property
	@abstractmethod
	def legacy(self) -> legacyWebExtension:
		"""
		Returns the underlying legacy Selenium WebExtension instance.

		This provides a way to access the original Selenium object for operations
		not covered by this abstract interface.

		Returns:
			legacyWebExtension: The legacy Selenium WebExtension object.
		"""
		
		...
	
	@abstractmethod
	def uninstall(self, extension_id_or_result: Union[str, Mapping[str, Any]]) -> None:
		"""
		Uninstalls a web extension.

		Args:
			extension_id_or_result (Union[str, Mapping[str, Any]]): The ID of the extension
				or the result dictionary from an install operation.
		"""
		
		...
