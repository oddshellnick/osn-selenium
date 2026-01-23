from typing import Any, Iterable, Union
from osn_selenium._functions import flatten_types
from osn_selenium.exceptions.base import OSNSeleniumError
from osn_selenium._typehints import (
	TYPES_FOR_FLATTENING_TYPEHINT
)


__all__ = [
	"ConfigurationError",
	"DuplicationError",
	"NotExpectedTypeError",
	"NotExpectedValueError"
]


class ConfigurationError(OSNSeleniumError):
	"""
	Base class for configuration-related errors.
	"""
	
	pass


class NotExpectedValueError(ConfigurationError):
	"""
	Error raised when a configuration value is not among the expected valid values.
	"""
	
	def __init__(self, value_name: str, value: Any, valid_values: Iterable[Any]) -> None:
		"""
		Initializes NotExpectedValueError.

		Args:
			value_name (str): The name of the configuration parameter.
			value (Any): The invalid value provided.
			valid_values (Iterable[Any]): A collection of acceptable values.
		"""
		
		super().__init__(
				f"Invalid '{value_name}' value ({str(value)}. Valid values: {', '.join(str(valid_value) for valid_value in valid_values)}."
		)


class NotExpectedTypeError(ConfigurationError):
	"""
	Error raised when a configuration value has an invalid type.
	"""
	
	def __init__(
			self,
			value_name: str,
			value: Any,
			valid_types: Union[TYPES_FOR_FLATTENING_TYPEHINT, Iterable[TYPES_FOR_FLATTENING_TYPEHINT]]
	) -> None:
		"""
		Initializes NotExpectedTypeError.

		Args:
			value_name (str): The name of the configuration parameter.
			value (Any): The value with the incorrect type.
			valid_types (Union[TYPE_FOR_FLATTENING, Iterable[TYPE_FOR_FLATTENING]]): The expected type or types.
		"""
		
		super().__init__(
				f"Invalid '{value_name}' type ({str(value)}. Valid types: {', '.join(flatten_types(valid_types))}."
		)


class DuplicationError(ConfigurationError):
	"""
	Error raised when a configuration parameter contains duplicated values.
	"""
	
	def __init__(self, value_name: str, duplicated_values: Union[str, Iterable[str]]) -> None:
		"""
		Initializes DuplicationError.

		Args:
			value_name (str): The name of the parameter.
			duplicated_values (Union[str, Iterable[str]]): The value or values that were duplicated.
		"""
		
		super().__init__(f"'{value_name}' has been duplicated: {', '.join(duplicated_values)}.")
