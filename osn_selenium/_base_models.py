from pydantic import (
	BaseModel,
	ConfigDict
)


__all__ = ["DictModel", "ExtraDictModel"]


class ExtraDictModel(BaseModel):
	"""
	Base class for Pydantic models that allows extra fields.

	This configuration allows the model to accept fields that are not
	explicitly defined in the model's schema.
	"""
	
	model_config = ConfigDict(
			populate_by_name=True,
			extra="allow",
			use_enum_values=True,
			str_strip_whitespace=True,
			validate_assignment=True,
	)


class DictModel(BaseModel):
	"""
	Base class for Pydantic models with a predefined configuration.

	This configuration enforces strict validation rules such as forbidding extra
	fields and stripping whitespace from string inputs.
	"""
	
	model_config = ConfigDict(
			populate_by_name=True,
			extra="forbid",
			use_enum_values=True,
			str_strip_whitespace=True,
			validate_assignment=True,
	)
