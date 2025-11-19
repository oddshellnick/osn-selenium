from typing import Dict, List

import trio
from selenium.webdriver.common.bidi.cdp import CdpConnectionClosed


class WrongHandlerSettingsTypeError(Exception):
	"""
	Custom exception raised when the event handler settings type is incorrect.

	This exception is raised when the provided handler settings is not a dictionary,
	but expected to be for proper configuration of event handlers.
	"""
	
	def __init__(self, handler_settings_type: type):
		"""
		Initializes WrongHandlerSettingsTypeError with the incorrect settings type.

		Args:
			handler_settings_type (type): The type of the handler settings that caused the error.
		"""
		
		super().__init__(
				f"Wrong event handler settings type ({handler_settings_type}). It must be a Dict!"
		)


class WrongHandlerSettingsError(Exception):
	"""
	Custom exception raised when event handler settings are incorrect.

	This exception is raised if the provided handler settings dictionary does not contain
	exactly one of the expected keys, as specified in the `one_of` attribute.
	"""
	
	def __init__(self, handler_settings: Dict, one_of: List[str]):
		"""
		Initializes WrongHandlerSettingsError with the incorrect handler settings and expected keys.

		Args:
			handler_settings (Dict[str, Any]): The dictionary of handler settings that caused the error.
			one_of (Sequence[str]): A List of expected keys, exactly one of which should be in `handler_settings`.
		"""
		
		super().__init__(
				f"Wrong event handler settings ({handler_settings})\n\nIt must contain exactly one of {one_of} keys!"
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
		CdpConnectionClosed
)
