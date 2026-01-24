from typing import Any
from osn_selenium._functions import flatten_types


__all__ = [
	"CannotConvertTypeError",
	"NotExpectedTypeError",
	"TypeIsNotWrapperError"
]


class TypeIsNotWrapperError(Exception):
	"""
	Error raised when a class does not implement the required wrapper protocol.
	"""
	
	def __init__(self, class_var: Any, wrapper_protocol: Any):
		"""
		Initializes the error with the invalid class and the expected protocol.

		Args:
			class_var (Any): The class that failed the check.
			wrapper_protocol (Any): The protocol that was expected.
		"""
		
		super().__init__(
				f"Class {class_var} is not a wrapper class. Check {wrapper_protocol} protocol"
		)


class NotExpectedTypeError(Exception):
	"""
	Error raised when an object is not of the expected type.
	"""
	
	def __init__(self, expected_class: Any, received_instance: Any):
		"""
		Initializes the error with expected types and the actual received instance.

		Args:
			expected_class (Any): The type or collection of types expected.
			received_instance (Any): The actual instance received.
		"""
		
		expected_str = ", ".join(flatten_types(expected_class))
		
		super().__init__(
				f"Expected one of [{expected_str}], got {type(received_instance).__name__}"
		)


class CannotConvertTypeError(Exception):
	"""
	Error raised when conversion between two types is not possible.
	"""
	
	def __init__(self, from_: Any, to_: Any):
		"""
		Initializes the error with the source and target objects.

		Args:
			from_ (Any): The object being converted from.
			to_ (Any): The object being converted to.
		"""
		
		super().__init__(f"Cannot convert {type(from_).__name__} to {type(to_).__name__}")
