import trio
from osn_selenium.exceptions.base import OSNSeleniumError
from osn_selenium.dev_tools._exception_helpers import (
	extract_exception_trace
)
from selenium.webdriver.common.bidi.cdp import (
	BrowserError,
	CdpConnectionClosed
)


__all__ = [
	"BidiConnectionNotEstablishedError",
	"CDPCommandNotFoundError",
	"CDPEndExceptions",
	"CantEnterDevToolsContextError",
	"DevToolsError",
	"ExceptionThrown",
	"TrioEndExceptions"
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
	
	def __init__(self, exception: BaseException) -> None:
		"""
		Initializes the ExceptionThrown wrapper.

		Args:
			exception (BaseException): The exception to wrap.
		"""
		
		self.exception = exception
		self.traceback = extract_exception_trace(exception)


class DevToolsError(OSNSeleniumError):
	"""
	Base exception for all DevTools-related operations.
	"""
	
	pass


class CantEnterDevToolsContextError(DevToolsError):
	"""
	Custom exception raised when unable to enter the DevTools context.

	This exception is raised when the attempt to switch the WebDriver's context to
	the DevTools frame fails, preventing further DevTools interactions.
	"""
	
	def __init__(self, reason: str) -> None:
		"""
		Initializes CantEnterDevToolsContextError with the reason of failure.

		Args:
			reason (str): The reason why entering the DevTools context failed.
		"""
		
		super().__init__(f"Can't enter devtools context! Reason: {reason}.")


class CDPCommandNotFoundError(DevToolsError):
	"""
	Error raised when a requested CDP command attribute is not found in the specified module.
	"""
	
	def __init__(self, object_: str, module_: str):
		"""
		Initializes CDPCommandNotFoundError.

		Args:
			object_ (str): The name of the missing attribute.
			module_ (str): The name of the module where the attribute was expected.
		"""
		
		super().__init__(f"Attribute '{object_}' not found in '{module_}'")


class BidiConnectionNotEstablishedError(DevToolsError):
	"""
	Custom exception raised when a BiDi connection is required but not established.

	This indicates that a DevTools operation was attempted before the `DevTools`
	context manager was entered, which establishes the necessary BiDi connection.
	"""
	
	def __init__(self) -> None:
		"""
		Initializes BidiConnectionNotEstablishedError.
		"""
		
		super().__init__("Bidi connection not established. Enter the DevTools context first!")


TrioEndExceptions = (trio.Cancelled, trio.EndOfChannel, trio.ClosedResourceError)
CDPEndExceptions = (
		trio.Cancelled,
		trio.EndOfChannel,
		trio.ClosedResourceError,
		CdpConnectionClosed,
		BrowserError
)
