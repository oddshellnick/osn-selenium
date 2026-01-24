from osn_selenium.exceptions.instance import NotExpectedTypeError
from osn_selenium.javascript._functions import convert_to_js_value
from osn_selenium.javascript.fingerprint._decorators import indent_code
from typing import (
	Any,
	List,
	Optional,
	Sequence,
	Tuple,
	Union
)
from osn_selenium.javascript.fingerprint._functions import reduce_code_level
from osn_selenium.javascript.fingerprint.spoof._typehints import NUMBER_TYPEHINT
from osn_selenium.javascript.fingerprint.spoof.noise import (
	RandomNoise,
	StaticNoise
)
from osn_selenium.javascript.fingerprint.spoof._templates import (
	ABSOLUTE_FREQUENCY,
	ARRAY_GLOBAL_BLOCK,
	INDEX_CALCULATION_PERIODIC,
	INDEX_CALCULATION_RAW,
	INDEX_INCLUSION_LIST_CHECK,
	INDEX_INCLUSION_SINGLE_CHECK,
	VARIABLE_FREQUENCY
)


__all__ = [
	"get_array_global_block_js",
	"get_frequency_js",
	"get_index_calculation_js",
	"get_noise_js",
	"get_random_expression_js"
]


def get_random_expression_js(value: Union[List[Any], Tuple[NUMBER_TYPEHINT, NUMBER_TYPEHINT]]) -> str:
	"""
	Generates JavaScript code to produce a random value based on the input configuration.

	Args:
		value (Union[List[Any], Tuple[NUMBER, NUMBER]]): A list of options or a tuple representing a numeric range (min, max).

	Returns:
		str: A JavaScript expression string that evaluates to a random value.

	Raises:
		TypeError: If the value type is not supported.
	"""
	
	if isinstance(value, tuple) and len(value) == 2:
		min_val, max_val = value
	
		difference = max_val - min_val
	
		val1 = str(difference) if difference >= 0 else f"({difference})"
		operator = "+" if min_val >= 0 else "-"
		val2 = str(abs(min_val))
	
		return f"(Math.random() * {val1} {operator} {val2})"
	
	if isinstance(value, list):
		json_items = convert_to_js_value(value)
		return f"{json_items}[Math.floor(Math.random() * {len(value)})]"
	
	raise NotExpectedTypeError(expected_type=(list, tuple), received_instance=value)


def get_noise_js(
		target: str,
		noise: str,
		operation: str,
		round_result: bool,
		precision: int
) -> str:
	"""
	Generates JavaScript code to apply noise to a target value.

	Args:
		target (str): The JavaScript variable/expression to modify.
		noise (str): The JavaScript expression representing the noise value.
		operation (str): The operation ('add' or 'multiply').
		round_result (bool): Whether to round the final result.
		precision (int): Number of decimal places to keep if rounding.

	Returns:
		str: A JavaScript expression applying the noise.
	"""
	
	base = f"Number({target})"
	
	if operation == "multiply":
		expr = f"({base} * {noise})"
	else:
		expr = f"({base} + {noise})"
	
	if round_result:
		if precision == 0:
			return f"Math.round({expr})"
	
		return f"Math.round({expr} * {precision}) / {precision}"
	
	return expr


def get_index_calculation_js(cycle_length: Optional[int]) -> str:
	"""
	Generates the JavaScript logic for calculating the loop index, optionally handling periodicity.

	Args:
		cycle_length (Optional[int]): The length of the cycle for periodic modification.

	Returns:
		str: The JavaScript expression for the current index.
	"""
	
	if cycle_length is None or cycle_length <= 0:
		return INDEX_CALCULATION_RAW
	
	return INDEX_CALCULATION_PERIODIC.format(cycle_length=cycle_length)


@indent_code
def get_frequency_js(frequency_object: Any, expression: str) -> str:
	"""
	Generates JavaScript code to conditionally execute an assignment based on frequency/probability.

	Args:
		frequency_object (Any): An object containing a 'frequency' attribute (e.g., Noise object).
		expression (str): The JavaScript assignment expression to execute.

	Returns:
		str: JavaScript code block with probability logic.
	"""
	
	if isinstance(frequency_object, (StaticNoise, RandomNoise)):
		frequency = frequency_object.frequency
	else:
		frequency = 1.0
	
	if frequency == 1.0:
		return ABSOLUTE_FREQUENCY.format(assignment_expression=expression)
	
	return VARIABLE_FREQUENCY.format(frequency=frequency, assignment_expression=expression)


@indent_code
def get_array_global_block_js(index_list: Optional[Sequence[int]], frequency_expression: str) -> str:
	"""
	Generates the global block logic for array spoofing, checking if indices match specific rules.

	Args:
		index_list (Optional[Sequence[int]]): specific indices to target, or None for all.
		frequency_expression (str): The logic to execute if indices match.

	Returns:
		str: JavaScript code block for the array loop body.
	"""
	
	if index_list is None:
		return reduce_code_level(code=frequency_expression, num=1)
	
	if len(index_list) == 1:
		index_inclusion_check = INDEX_INCLUSION_SINGLE_CHECK.format(channel_index=index_list[0])
	else:
		index_inclusion_check = INDEX_INCLUSION_LIST_CHECK.format(index_list=",".join(map(str, index_list)))
	
	return ARRAY_GLOBAL_BLOCK.format(
			index_inclusion_check=index_inclusion_check,
			frequency_logic=frequency_expression
	)
