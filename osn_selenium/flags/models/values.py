from typing import Any
from osn_selenium._base_models import DictModel


__all__ = ["ArgumentValue", "AttributeValue", "ExperimentalOptionValue"]


class ExperimentalOptionValue(DictModel):
	"""
	Experimental option structure.

	Attributes:
		option_name (str): Option name.
		value (Any): Option value.
	"""
	
	option_name: str
	value: Any


class AttributeValue(DictModel):
	"""
	WebDriver attribute structure.

	Attributes:
		attribute_name (str): Attribute name.
		value (Any): Attribute value.
	"""
	
	attribute_name: str
	value: Any


class ArgumentValue(DictModel):
	"""
	Command-line argument structure.

	Attributes:
		command_line (str): The command-line string.
		value (Any): Value associated with the argument.
	"""
	
	command_line: str
	value: Any
