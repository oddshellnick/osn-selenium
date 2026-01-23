from osn_selenium.exceptions.base import OSNSeleniumError


__all__ = [
	"WebDriverAlreadyRunningError",
	"WebDriverError",
	"WebDriverNotStartedError"
]


class WebDriverError(OSNSeleniumError):
	"""
	Base class for WebDriver lifecycle and control errors.
	"""
	
	pass


class WebDriverNotStartedError(WebDriverError):
	"""
	Error raised when an operation is performed while the WebDriver session is not active.
	"""
	
	def __init__(self) -> None:
		"""
		Initializes WebDriverNotStartedError.
		"""
		
		super().__init__("WebDriver is not started. Call start_webdriver() first.")


class WebDriverAlreadyRunningError(WebDriverError):
	"""
	Error raised when an attempt is made to start a WebDriver that is already active.
	"""
	
	def __init__(self) -> None:
		"""
		Initializes WebDriverAlreadyRunningError.
		"""
		
		super().__init__(
				"WebDriver is already active. Stop it or use restart_webdriver() to apply changes."
		)
