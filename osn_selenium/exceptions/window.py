from osn_selenium.exceptions.base import OSNSeleniumError


__all__ = [
	"InvalidWindowHandleError",
	"InvalidWindowIndexError",
	"NoWindowHandlesFoundError",
	"WindowManagementError"
]


class WindowManagementError(OSNSeleniumError):
	"""
	Base class for errors related to window and tab management.
	"""
	
	pass


class NoWindowHandlesFoundError(WindowManagementError):
	"""
	Error raised when the WebDriver session reports having no windows.
	"""
	
	def __init__(self) -> None:
		"""
		Initializes NoWindowHandlesFoundError.
		"""
		
		super().__init__("No window handles found in session.")


class InvalidWindowIndexError(WindowManagementError):
	"""
	Error raised when trying to access a window by an out-of-bounds index.
	"""
	
	def __init__(self, index: int, handles_length: int) -> None:
		"""
		Initializes InvalidWindowIndexError.

		Args:
			index (int): The requested index.
			handles_length (int): The current count of window handles.
		"""
		
		super().__init__(f"Window index {index} out of range [0, {handles_length - 1}]")


class InvalidWindowHandleError(WindowManagementError):
	"""
	Error raised when a specific window handle string is not recognized in the session.
	"""
	
	def __init__(self, handle: str) -> None:
		"""
		Initializes InvalidWindowHandleError.

		Args:
			handle (str): The invalid window handle string.
		"""
		
		super().__init__(f"Handle: {handle} not found in session.")
