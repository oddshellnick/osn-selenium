from pydantic import Field
from typing import Any, Literal
from osn_selenium._base_models import DictModel
from osn_selenium.javascript.fingerprint.spoof._typehints import (
	NOISE_TYPEHINT,
	RANDOM_NOISE_TYPEHINT
)


__all__ = ["BaseNoise", "RandomNoise", "StaticNoise"]


class BaseNoise(DictModel):
	"""
	Base configuration for noise generation.

	Attributes:
		value (Any): The base value or range for the noise.
		frequency (float): Probability of applying the noise (0.0 to 1.0).
		operation (Literal["add", "multiply"]): Mathematical operation to apply noise.
		round (bool): Whether to round the result.
		precision (int): Decimal precision if rounding is enabled.
	"""
	
	value: Any
	frequency: float = Field(default=1.0, gt=0.0, le=1.0)
	operation: Literal["add", "multiply"] = "add"
	round: bool = False
	precision: int = Field(default=0, ge=0)


class StaticNoise(BaseNoise):
	"""
	Configuration for static (constant) noise.

	Attributes:
		value (NOISE): A single numeric value to use as noise.
	"""
	
	value: NOISE_TYPEHINT


class RandomNoise(BaseNoise):
	"""
	Configuration for random noise generation.

	Attributes:
		value (RANDOM_NOISE): A range (tuple) or list of values to pick from.
	"""
	
	value: RANDOM_NOISE_TYPEHINT
