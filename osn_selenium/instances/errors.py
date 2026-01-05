from typing import Any


class ExpectedTypeError(Exception):
	def __init__(self, expected_class: Any, received_instance: Any):
		super().__init__(f"Expected {type(expected_class).__name__}, got {type(received_instance).__name__}")


class TypesConvertError(Exception):
	def __init__(self, from_: Any, to_: Any):
		super().__init__(f"Cannot convert {type(from_).__name__} to {type(to_).__name__}")
