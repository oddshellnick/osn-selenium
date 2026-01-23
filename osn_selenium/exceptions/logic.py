from osn_selenium.exceptions.base import OSNSeleniumError


__all__ = ["AbstractImplementationError", "LogicError"]


class LogicError(OSNSeleniumError):
	"""
	Base class for internal logic and implementation errors.
	"""
	
	pass


class AbstractImplementationError(LogicError):
	"""
	Error raised when an abstract method is not implemented in a subclass.
	"""
	
	def __init__(self, method_name: str, class_name: str) -> None:
		"""
		Initializes AbstractImplementationError.

		Args:
			method_name (str): The name of the method that should have been implemented.
			class_name (str): The name of the base class defining the abstract method.
		"""
		
		super().__init__(
				f"Method '{method_name}' must be implemented in subclass of '{class_name}'."
		)
