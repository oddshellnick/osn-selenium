from osn_selenium._exception_helpers import (
	extract_exception_trace
)

__all__ = ["ExceptionThrown", "OSNSeleniumError"]

class OSNSeleniumError(Exception):
	"""
	Base exception class for all errors in the OSN Selenium library.
	"""
	
	pass


class ExceptionThrown:
	"""
	A wrapper class to indicate that an exception was thrown during an operation.

	This is used in `execute_cdp_command` when `error_mode` is "log" or "pass"
	to return an object indicating an error occurred without re-raising it immediately.

	Attributes:
		exception (BaseException): The exception that was caught.
		traceback (str): The formatted traceback string of the exception.
	"""
	
	def __init__(self, exception: BaseException) -> None:
		"""
		Initializes the ExceptionThrown wrapper.

		Args:
			exception (BaseException): The exception to wrap.
		"""
		
		self.exception = exception
		self.traceback = extract_exception_trace(exception)
