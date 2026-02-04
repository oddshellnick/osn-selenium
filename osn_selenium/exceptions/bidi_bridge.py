from osn_selenium.exceptions.base import OSNSeleniumError

__all__ = ["BiDiBridgeError", "BiDiBridgeStoppedError", "BiDiExecutionError", "CommandNotMappedToBiDiError"]

class BiDiBridgeError(OSNSeleniumError):
	"""
	Base class for exceptions related to the BiDi Bridge.
	"""
	
	pass


class CommandNotMappedToBiDiError(BiDiBridgeError):
	"""
	Exception raised when a requested W3C command has no corresponding BiDi mapping.
	"""
	
	def __init__(self, command: str) -> None:
		"""
		Initialize the exception.

		Args:
			command (str): The name of the unmapped command.
		"""
		
		super().__init__(f"{command} is not mapped to BiDi.")


class BiDiExecutionError(OSNSeleniumError):
	"""
	Exception raised when a BiDi command execution fails on the browser side.
	"""
	
	def __init__(self, error: str, message: str) -> None:
		"""
		Initialize the exception with the error type and message.

		Args:
			error (str): The error category or code returned by the BiDi protocol.
			message (str): The detailed error message provided by the browser.
		"""
		
		super().__init__(f"BiDi: {error} - {message}")


class BiDiBridgeStoppedError(BiDiBridgeError):
	"""
	Raised when the BiDi bridge has been stopped while tasks were still pending.
	"""
	
	def __init__(self, reason: str) -> None:
		"""
		Initializes the error with the stop reason.

		Args:
			reason (str): The reason why the bridge stopped.
		"""
		
		super().__init__(f"BiDi bridge was stopped. Reason: {reason}")
