import trio
from selenium.webdriver.common.bidi.cdp import (
	BrowserError,
	CdpConnectionClosed
)


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
