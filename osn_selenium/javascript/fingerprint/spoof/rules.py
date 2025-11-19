from pydantic import Field
from typing import (
	Dict,
	Literal,
	Optional
)
from osn_selenium.javascript._functions import convert_to_js_value
from osn_selenium.javascript.fingerprint._functions import add_code_level
from osn_selenium.javascript.fingerprint.spoof.noise import (
	RandomNoise,
	StaticNoise
)
from osn_selenium.javascript.fingerprint.spoof._typehints import (
	RANDOM_VALUE_TYPEHINT
)
from osn_selenium.javascript.fingerprint.spoof.core_rules import (
	ArrayRule,
	BaseRule,
	RandomRule
)
from osn_selenium.javascript.fingerprint.spoof._functions import (
	get_noise_js,
	get_random_expression_js
)
from osn_selenium.javascript.fingerprint.spoof._templates import (
	CUSTOM_RULE,
	PERSISTED_RANDOM_ITEM_NOISE,
	PERSISTED_RANDOM_ITEM_SET,
	PERSISTENCE_CHECK_NOISE,
	PERSISTENCE_CHECK_RETURN,
	PERSISTENCE_SAVE_NOISE,
	PERSISTENCE_SAVE_RESULT,
	RANDOM_ITEM_NOISE,
	RANDOM_ITEM_SET,
	STATIC_ITEM_NOISE,
	STATIC_ITEM_SET
)


__all__ = [
	"CustomRule",
	"RandomArrayNoiseRule",
	"RandomArraySetRule",
	"RandomItemNoiseRule",
	"RandomItemSetRule",
	"StaticArrayNoiseRule",
	"StaticArraySetRule",
	"StaticItemNoiseRule",
	"StaticItemSetRule"
]


class StaticItemSetRule(BaseRule):
	"""
	Rule to replace a value with a static constant.
	"""
	
	mode: Literal["static_item_set"] = "static_item_set"
	
	def generate_js(self, path: str) -> str:
		"""
		Generates JS to return a fixed value.

		Args:
			path (str): The object path.

		Returns:
			str: The generated JS.
		"""
		
		return STATIC_ITEM_SET.format(result_value=convert_to_js_value(self.value))


class StaticItemNoiseRule(BaseRule):
	"""
	Rule to apply static noise to a value.
	"""
	
	mode: Literal["static_item_noise"] = "static_item_noise"
	value: StaticNoise
	
	def generate_js(self, path: str) -> str:
		"""
		Generates JS to apply calculated static noise.

		Args:
			path (str): The object path.

		Returns:
			str: The generated JS.
		"""
		
		expression = get_noise_js(
				target="originalValue",
				noise=str(self.value.value),
				operation=self.value.operation,
				round_result=self.value.round,
				precision=self.value.precision,
		)
		
		return STATIC_ITEM_NOISE.format(math_expression=expression)


class StaticArraySetRule(ArrayRule):
	"""
	Rule to replace elements in an array with static values.
	"""
	
	mode: Literal["static_array_set"] = "static_array_set"
	
	def generate_js(self, path: str) -> str:
		"""
		Generates JS to loop through array and set static values.

		Args:
			path (str): The object path.

		Returns:
			str: The generated JS.
		"""
		
		def get_expr(item):
			return convert_to_js_value(item)
		
		return self._generate_array_js(get_expr)


class StaticArrayNoiseRule(ArrayRule):
	"""
	Rule to apply static noise to elements in an array.
	"""
	
	mode: Literal["static_array_noise"] = "static_array_noise"
	value_by_channel: Dict[int, StaticNoise] = Field(default_factory=dict)
	
	def generate_js(self, path: str) -> str:
		"""
		Generates JS to loop through array and apply static noise.

		Args:
			path (str): The object path.

		Returns:
			str: The generated JS.
		"""
		
		def get_expr(item):
			return get_noise_js(
					target="dataArray[i]",
					noise=str(item.value),
					operation=item.operation,
					round_result=item.round,
					precision=item.precision,
			)
		
		return self._generate_array_js(get_expr)


class RandomItemSetRule(RandomRule):
	"""
	Rule to replace a value with a randomly generated one.
	"""
	
	mode: Literal["random_item_set"] = "random_item_set"
	
	def generate_js(self, path: str) -> str:
		"""
		Generates JS to return a random value, optionally persisted.

		Args:
			path (str): The object path.

		Returns:
			str: The generated JS.
		"""
		
		if self.persist:
			storage_key = f"prop_{path.replace('.', '_')}"
		
			return PERSISTED_RANDOM_ITEM_SET.format(
					persistence_check_code=add_code_level(code=PERSISTENCE_CHECK_RETURN.format(storage_key=storage_key), num=1),
					calculation_expression=get_random_expression_js(self.value),
					persistence_save_code=PERSISTENCE_SAVE_RESULT.format(storage_key=storage_key)
			)
		
		return RANDOM_ITEM_SET.format(calculation_expression=get_random_expression_js(self.value))


class RandomItemNoiseRule(RandomRule):
	"""
	Rule to apply random noise to a value.
	"""
	
	mode: Literal["random_item_noise"] = "random_item_noise"
	
	def generate_js(self, path: str) -> str:
		"""
		Generates JS to apply random noise, optionally persisted.

		Args:
			path (str): The object path.

		Returns:
			str: The generated JS.
		"""
		
		storage_key = f"prop_{path.replace('.', '_')}"
		
		math_expression = get_noise_js(
				target="originalValue",
				noise="noiseValue",
				operation=self.value.operation,
				round_result=self.value.round,
				precision=self.value.precision,
		)
		
		if self.persist:
			return PERSISTED_RANDOM_ITEM_NOISE.format(
					persistence_check_code=add_code_level(
							code=PERSISTENCE_CHECK_NOISE.format(storage_key=storage_key, math_expression_with_noise=math_expression),
							num=1
					),
					calculation_expression=get_random_expression_js(self.value.value),
					persistence_save_code=PERSISTENCE_SAVE_NOISE.format(storage_key=storage_key),
					math_expression=math_expression
			)
		
		return RANDOM_ITEM_NOISE.format(
				calculation_expression=get_random_expression_js(self.value.value),
				math_expression=math_expression
		)


class RandomArraySetRule(ArrayRule):
	"""
	Rule to replace elements in an array with random values.
	"""
	
	mode: Literal["random_array_set"] = "random_array_set"
	value: Optional[RANDOM_VALUE_TYPEHINT]
	value_by_channel: Dict[int, RANDOM_VALUE_TYPEHINT] = Field(default_factory=dict)
	
	def generate_js(self, path: str) -> str:
		"""
		Generates JS to loop through array and set random values.

		Args:
			path (str): The object path.

		Returns:
			str: The generated JS.
		"""
		
		def get_expr(item):
			return get_random_expression_js(item)
		
		return self._generate_array_js(get_expr)


class RandomArrayNoiseRule(ArrayRule):
	"""
	Rule to apply random noise to elements in an array.
	"""
	
	mode: Literal["random_array_noise"] = "random_array_noise"
	value: Optional[RandomNoise]
	value_by_channel: Dict[int, RandomNoise] = Field(default_factory=dict)
	
	def generate_js(self, path: str) -> str:
		"""
		Generates JS to loop through array and apply random noise.

		Args:
			path (str): The object path.

		Returns:
			str: The generated JS.
		"""
		
		def get_expr(item):
			noise_expr = get_random_expression_js(item.value)
			
			return get_noise_js(
					target="dataArray[i]",
					noise=noise_expr,
					operation=item.operation,
					round_result=item.round,
					precision=item.precision,
			)
		
		return self._generate_array_js(get_expr)


class CustomRule(BaseRule):
	"""
	Rule to apply custom JavaScript code.
	"""
	
	mode: Literal["custom"] = "custom"
	value: str
	
	def generate_js(self, path: str) -> str:
		"""
		Generates the custom JS injection.

		Args:
			path (str): The object path.

		Returns:
			str: The generated JS.
		"""
		
		return CUSTOM_RULE.format(custom_javascript_code=self.value)
