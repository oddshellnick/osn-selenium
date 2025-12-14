from typing import (
	Any,
	List,
	Set,
	Tuple,
	Union
)


class TypesConvertError(Exception):
	def __init__(self, from_: Any, to_: Any):
		super().__init__(f"Cannot convert {type(from_).__name__} to {type(to_).__name__}")


class ExpectedTypeError(Exception):
	def __init__(
			self,
			expected_class: Union[Any, List[Any], Set[Any], Tuple[Any, ...]],
			received_instance: Any
	):
		expected_str = " or ".join(x.__name__ for x in expected_class) if isinstance(expected_class, (List, Set, Tuple)) else type(expected_class).__name__
		
		super().__init__(f"Expected {expected_str}, got {type(received_instance).__name__}")
