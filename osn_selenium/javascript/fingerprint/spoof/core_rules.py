from osn_selenium._base_models import DictModel
from pydantic import (
	Field,
	model_validator
)
from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Self
)
from osn_selenium.javascript.fingerprint._functions import add_code_level
from osn_selenium.exceptions.logic import (
	AbstractImplementationError
)
from osn_selenium.javascript.fingerprint.spoof._templates import (
	ARRAY_CHANNEL_BLOCK,
	ARRAY_LOOP_WRAPPER
)
from osn_selenium.javascript.fingerprint.spoof._functions import (
	get_array_global_block_js,
	get_frequency_js,
	get_index_calculation_js
)


__all__ = ["ArrayRule", "BaseRule", "RandomRule"]


class BaseRule(DictModel):
	"""
	Abstract base class for all spoofing rules.

	Attributes:
		mode (str): The identifier for the rule type.
		value (Any): The value associated with the rule.
	"""
	
	mode: str
	value: Any
	
	def generate_js(self, path: str) -> str:
		"""
		Generates the JavaScript implementation for this rule.

		Args:
			path (str): The object path where the rule applies.

		Returns:
			str: The generated JavaScript code.

		Raises:
			NotImplementedError: Must be implemented by subclasses.
		"""
		
		raise AbstractImplementationError(method_name="generate_js", class_name=self.__class__.__name__)


class RandomRule(BaseRule):
	"""
	Base class for rules involving random value generation with optional persistence.

	Attributes:
		mode (str): The identifier for the rule type.
		value (Any): The value associated with the rule.
		persist (bool): Whether to store and reuse the generated random value.
	"""
	
	persist: bool = False


class ArrayRule(BaseRule):
	"""
	Base class for rules that modify array contents.

	Attributes:
		mode (str): The identifier for the rule type.
		value (Any): The value associated with the rule.
		cycle_length (Optional[int]): Length of the cycle for periodic modification.
		index_list (Optional[List[int]]): Specific indices to target globally.
		value_by_channel (Dict[int, Any]): Specific values for specific indices.
	"""
	
	cycle_length: Optional[int] = None
	index_list: Optional[List[int]] = None
	value_by_channel: Dict[int, Any] = Field(default_factory=dict)
	
	@model_validator(mode="after")
	def _cleanup_channels(self) -> Self:
		"""
		Validates and cleans up the index list to avoid conflicts with explicit channels.

		Returns:
			Self: The validated model.
		"""
		
		if self.index_list is not None and self.value_by_channel:
			exclusive_channels = set(self.value_by_channel.keys())
			self.index_list = [c for c in self.index_list if c not in exclusive_channels]
		
		return self
	
	def _generate_array_js(self, get_expression_fn: Callable[[Any], str]) -> str:
		"""
		Helper to generate the array looping and modification logic.

		Args:
			get_expression_fn (Callable[[Any], str]): Function to convert a value/noise item into a JS expression.

		Returns:
			str: The complete JavaScript code for the array wrapper.
		"""
		
		body_parts = []
		
		if self.value_by_channel:
			for ch, item in self.value_by_channel.items():
				expression = get_expression_fn(item)
				frequency_expression = get_frequency_js(frequency_object=item, expression=expression)
		
				body_parts.append(
						add_code_level(
								code=ARRAY_CHANNEL_BLOCK.format(target_index=ch, frequency_logic=frequency_expression),
								num=1
						)
				)
		
		if self.value is not None:
			expression = get_expression_fn(self.value)
			frequency_expression = get_frequency_js(frequency_object=self.value, expression=expression)
		
			body_parts.append(
					get_array_global_block_js(index_list=self.index_list, frequency_expression=frequency_expression)
			)
		
		return ARRAY_LOOP_WRAPPER.format(
				index_calculation=get_index_calculation_js(cycle_length=self.cycle_length),
				loop_body_logic=add_code_level(code="\n".join(body_parts), num=1)
		)
