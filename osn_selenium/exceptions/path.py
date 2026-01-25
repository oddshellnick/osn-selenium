from typing import Any
from osn_selenium._typehints import PATH_TYPEHINT
from osn_selenium.exceptions.base import OSNSeleniumError


__all__ = [
	"BrowserExecutableNotFoundError",
	"ExecutableError",
	"PathError",
	"PathValidationError",
	"WebDriverExecutableNotFoundError"
]


class PathError(OSNSeleniumError):
	"""
	Base class for file system and path-related errors.
	"""
	
	pass


class ExecutableError(PathError):
	"""
	Base class for errors related to binary executables.
	"""
	
	pass


class WebDriverExecutableNotFoundError(ExecutableError):
	"""
	Error raised when the WebDriver executable file cannot be found.
	"""
	
	def __init__(self, path: PATH_TYPEHINT) -> None:
		"""
		Initializes WebDriverExecutableNotFoundError.

		Args:
			path (PATH_TYPEHINT): The path where the WebDriver was expected.
		"""
		
		super().__init__(f"WebDriver executable not found at: {path}")


class PathValidationError(PathError):
	"""
	Error raised when a path fails to meet specific validation criteria.
	"""
	
	def __init__(self, path: Any, exception: Exception) -> None:
		"""
		Initializes PathValidationError.

		Args:
			path (Any): The path that failed validation.
			exception (Exception): The original exception caught during validation.
		"""
		
		super().__init__(f"Path '{path}' validation error:\n{exception}")


class BrowserExecutableNotFoundError(ExecutableError):
	"""
	Error raised when the browser executable binary cannot be found.
	"""
	
	def __init__(self, path: PATH_TYPEHINT) -> None:
		"""
		Initializes BrowserExecutableNotFoundError.

		Args:
			path (PATH_TYPEHINT): The path where the browser binary was expected.
		"""
		
		super().__init__(f"Browser executable not found at: {path}")
