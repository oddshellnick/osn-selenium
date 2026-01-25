from osn_selenium.exceptions.base import OSNSeleniumError


__all__ = ["FlagError", "FlagNotDefinedError", "FlagTypeNotDefinedError"]


class FlagError(OSNSeleniumError):
	"""
	Base class for errors related to management flags.
	"""
	
	pass


class FlagTypeNotDefinedError(FlagError):
	"""
	Error raised when a requested flag category is not recognized by the manager.
	"""
	
	def __init__(self, flag_type: str) -> None:
		"""
		Initializes FlagTypeNotDefinedError.

		Args:
			flag_type (str): The name of the undefined flag category.
		"""
		
		super().__init__(f"Flag category '{flag_type}' is not defined for this manager.")


class FlagNotDefinedError(FlagError):
	"""
	Error raised when a specific flag is not defined within a recognized category.
	"""
	
	def __init__(self, flag_name: str, flag_type: str) -> None:
		"""
		Initializes FlagNotDefinedError.

		Args:
			flag_name (str): The name of the missing flag.
			flag_type (str): The category where the flag was expected.
		"""
		
		super().__init__(f"Flag '{flag_name}' is not defined for type '{flag_type}'.")
