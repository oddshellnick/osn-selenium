from osn_selenium._functions import flatten_types
from typing import (
	Any,
	Iterable,
	Type,
	Union
)
from osn_selenium.exceptions.base import OSNSeleniumError
from osn_selenium._typehints import (
	TYPES_FOR_FLATTENING_TYPEHINT
)


__all__ = [
	"CannotConvertTypeError",
	"ElementInteractionError",
	"ElementNotVisibleError",
	"InstanceError",
	"NotExpectedTypeError"
]


class InstanceError(OSNSeleniumError):
	"""
	Base class for errors related to object instances and types.
	"""
	
	pass


class NotExpectedTypeError(InstanceError):
	"""
	Error raised when an object is not of the expected type.
	"""
	
	def __init__(
			self,
			expected_type: Union[TYPES_FOR_FLATTENING_TYPEHINT, Iterable[TYPES_FOR_FLATTENING_TYPEHINT]],
			received_instance: Any
	) -> None:
		"""
		Initializes the error with expected types and the actual received instance.

		Args:
			expected_type (Any): The type or collection of types expected.
			received_instance (Any): The actual instance received.
		"""
		
		super().__init__(
				f"Expected one of [{', '.join(flatten_types(expected_type))}], got {type(received_instance).__name__}"
		)


class ElementInteractionError(InstanceError):
	"""
	Error raised when an interaction with a web element fails.
	"""
	
	pass


class ElementNotVisibleError(ElementInteractionError):
	"""
	Error raised when a web element is not visible or has no size on the page.
	"""
	
	def __init__(self, element_id: str) -> None:
		"""
		Initializes ElementNotVisibleError.

		Args:
			element_id (str): The identifier of the hidden element.
		"""
		
		super().__init__(f"Element '{element_id}' is not visible or has no size.")


class CannotConvertTypeError(InstanceError):
	"""
	Error raised when conversion between two types is not possible.
	"""
	
	def __init__(self, from_: Type, to_: Any) -> None:
		"""
		Initializes the error with the source and target objects.

		Args:
			from_ (Any): The object being converted from.
			to_ (Any): The object being converted to.
		"""
		
		super().__init__(f"Cannot convert {from_.__name__} to {type(to_).__name__}")
