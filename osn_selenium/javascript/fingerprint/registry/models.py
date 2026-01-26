from pydantic import Field
from typing import Any, Dict, Optional
from osn_selenium._base_models import DictModel
from osn_selenium.javascript.fingerprint._typehints import SPOOF_RULE_TYPEHINT
from osn_selenium.javascript.fingerprint.registry._typehints import ITEM_TYPE_TYPEHINT


__all__ = ["RegistryItem"]


class RegistryItem(DictModel):
	"""
	Represents a single entry in the fingerprint registry, defining how a specific
	JavaScript API (method, property, or constructor) should be handled.

	Attributes:
		target (str): The global object or prototype path (e.g., 'window.navigator').
		name (Optional[str]): The name of the method or property. None for constructors/objects.
		type_ (ITEM_TYPE): The type of the item ('method', 'prop', 'constructor').
		api (str): The logical API category (e.g., 'webgl', 'battery').
		settings (Optional[Dict[str, Any]]): specific configuration for the hook.
		spoofing_rule (Optional[SPOOF_RULE_TYPEHINT]): The rule used to spoof the return value.
	"""
	
	target: str
	name: Optional[str] = None
	type_: ITEM_TYPE_TYPEHINT = Field(alias="type")
	api: str
	settings: Optional[Dict[str, Any]] = None
	spoofing_rule: Optional[SPOOF_RULE_TYPEHINT] = None
	
	@property
	def path(self) -> str:
		"""
		Constructs the full path identifier for the registry item.

		Returns:
			str: The dot-notation path (e.g., 'window.navigator.userAgent').
		"""
		
		return f"{self.target}.{self.name}" if self.name else self.target
