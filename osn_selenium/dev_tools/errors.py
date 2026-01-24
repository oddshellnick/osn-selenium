import trio
from osn_selenium.dev_tools._exception_helpers import (
	extract_exception_trace
)
from selenium.webdriver.common.bidi.cdp import (
	BrowserError,
	CdpConnectionClosed
)


__all__ = [
	"BidiConnectionNotEstablishedError",
	"CantEnterDevToolsContextError",
	"ExceptionThrown",
	"cdp_end_exceptions",
	"trio_end_exceptions"
]


class ExceptionThrown:
	"""
	A wrapper class to indicate that an exception was thrown during an operation.

	This is used in `execute_cdp_command` when `error_mode` is "log" or "pass"
	to return an object indicating an error occurred without re-raising it immediately.

	Attributes:
		exception (BaseException): The exception that was caught.
		traceback (str): The formatted traceback string of the exception.
	"""
	
	def __init__(self, exception: BaseException):
		"""
		Initializes the ExceptionThrown wrapper.

		Args:
			exception (BaseException): The exception to wrap.
		"""
		
		self.exception = exception
		self.traceback = extract_exception_trace(exception)


class CantEnterDevToolsContextError(Exception):
	"""
	Custom exception raised when unable to enter the DevTools context.

	This exception is raised when the attempt to switch the WebDriver's context to
	the DevTools frame fails, preventing further DevTools interactions.
	"""
	
	def __init__(self, reason: str):
		"""
		Initializes CantEnterDevToolsContextError with the reason of failure.

		Args:
			reason (str): The reason why entering the DevTools context failed.
		"""
		
		super().__init__(f"Can't enter devtools context! Reason: {reason}.")


class BidiConnectionNotEstablishedError(Exception):
	"""
	Custom exception raised when a BiDi connection is required but not established.

	This indicates that a DevTools operation was attempted before the `DevTools`
	context manager was entered, which establishes the necessary BiDi connection.
	"""
	
	def __init__(self):
		"""
		Initializes BidiConnectionNotEstablishedError.
		"""
		
		super().__init__("Bidi connection not established. Enter the DevTools context first!")


trio_end_exceptions = (trio.Cancelled, trio.EndOfChannel, trio.ClosedResourceError)
cdp_end_exceptions = (
		trio.Cancelled,
		trio.EndOfChannel,
		trio.ClosedResourceError,
		CdpConnectionClosed,
		BrowserError
)
