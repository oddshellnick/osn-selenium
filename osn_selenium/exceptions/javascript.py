from typing import Iterable, Union
from osn_selenium.exceptions.base import OSNSeleniumError


__all__ = ["JavaScriptError", "JavaScriptResourceError"]


class JavaScriptError(OSNSeleniumError):
	"""
	Base class for JavaScript-related errors.
	"""
	
	pass


class JavaScriptResourceError(JavaScriptError):
	"""
	Error raised when required JavaScript resources or scripts are missing.
	"""
	
	def __init__(self, missing_script: Union[str, Iterable[str]]) -> None:
		"""
		Initializes JavaScriptResourceError.

		Args:
			missing_script (Union[str, Iterable[str]]): The name or names of the missing scripts.
		"""
		
		missing_string = missing_script if isinstance(missing_script, str) else "\n\t- ".join(missing_script)
		
		super().__init__(f"Required JavaScript resources are missing:\n\t- {missing_string}")
