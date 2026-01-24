import os
import pathlib
from typing import Optional
from osn_selenium._typehints import PATH_TYPEHINT


__all__ = [
	"bool_adding_validation_function",
	"int_adding_validation_function",
	"optional_bool_adding_validation_function",
	"path_adding_validation_function",
	"str_adding_validation_function"
]


def str_adding_validation_function(value: Optional[str]) -> bool:
	"""
	Validation function that checks if a value is a non-empty string.

	Args:
		value (Optional[str]): The value to validate.

	Returns:
		bool: `True` if the value is a non-empty string, `False` otherwise.
	"""
	
	if value is not None and not isinstance(value, str):
		return False
	
	return bool(value)


def path_adding_validation_function(value: Optional[PATH_TYPEHINT]) -> bool:
	"""
	Validation function that checks if a value is a non-empty string or a Path object.

	Args:
		value (Optional[PATH_TYPEHINT]): The value to validate.

	Returns:
		bool: `True` if the value is a valid path-like object, `False` otherwise.
	"""
	
	if value is not None and not isinstance(value, (str, bytes, pathlib.Path, os.PathLike)):
		return False
	
	return bool(value)


def optional_bool_adding_validation_function(value: Optional[bool]) -> bool:
	"""
	Validation function that checks if a value is a boolean or None.

	The function returns `True` if the value is not None, allowing the flag
	to be added.

	Args:
		value (Optional[bool]): The value to validate.

	Returns:
		bool: `True` if the value is not None, `False` if the value is not a boolean.
	"""
	
	if value is not None and not isinstance(value, bool):
		return False
	
	return value is not None


def int_adding_validation_function(value: Optional[int]) -> bool:
	"""
	Validation function that checks if a value is an integer.

	Args:
		value (Optional[int]): The value to validate.

	Returns:
		bool: `True` if the value is an integer or None, `False` otherwise.
	"""
	
	if value is not None and not isinstance(value, int):
		return False
	
	return True


def bool_adding_validation_function(value: Optional[bool]) -> bool:
	"""
	Validation function that checks if a value is a boolean and `True`.

	Args:
		value (Optional[bool]): The value to validate.

	Returns:
		bool: `True` if the value is `True`, `False` otherwise.
	"""
	
	if not isinstance(value, bool):
		return False
	
	return value
