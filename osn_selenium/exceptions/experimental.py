from osn_selenium.exceptions.base import OSNSeleniumError

__all__ = ["ExperimentalFeatureError", "NotImplementedExperimentalFeatureError"]

class ExperimentalFeatureError(OSNSeleniumError):
	"""
	Base exception for experimental feature errors.
	"""
	
	pass


class NotImplementedExperimentalFeatureError(ExperimentalFeatureError):
	"""
	Raised when an experimental feature is not yet implemented.
	"""
	
	def __init__(self, name: str):
		"""
		Initializes the error with the name of the missing feature.

		Args:
			name (str): The name of the feature.
		"""
		
		super().__init__(f"{name} is not implemented in current version.")
