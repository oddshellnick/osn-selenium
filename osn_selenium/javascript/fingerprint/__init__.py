from pydantic import Field
from typing import Dict, List, Literal
from osn_selenium._base_models import DictModel
from osn_selenium.javascript.functions import get_js_scripts
from osn_selenium.javascript.fingerprint._functions import add_code_level
from osn_selenium.javascript.fingerprint.registry.models import RegistryItem
from osn_selenium.javascript.fingerprint._detect.functions import get_hook_js
from osn_selenium.javascript.fingerprint.registry import FINGERPRINT_REGISTRY
from osn_selenium.javascript.fingerprint._typehints import SPOOF_RULE_TYPEHINT
from osn_selenium.javascript._functions import (
	convert_to_js_value,
	inject_data_in_js_script
)


__all__ = ["FingerprintSettings"]


class FingerprintSettings(DictModel):
	"""
	Configuration settings for browser fingerprinting detection and spoofing.

	Attributes:
		optimize_events (bool): Whether to optimize event reporting to avoid duplicates.
		detect_events_mode (Literal["disable", "always", "not_spoofed"]): Logic for reporting detected events.
		registry (Dict[str, RegistryItem]): Custom registry items to override or extend defaults.
		use_preset_registry (bool): Whether to include the default built-in registry.
	"""
	
	optimize_events: bool = True
	detect_events_mode: Literal["disable", "always", "not_spoofed"] = "not_spoofed"
	
	registry: Dict[str, RegistryItem] = Field(default_factory=dict)
	use_preset_registry: bool = True
	
	def _get_registry(self) -> Dict[str, RegistryItem]:
		"""
		Compiles the final registry by merging presets with custom user overrides.

		Returns:
			Dict[str, RegistryItem]: The active registry map.
		"""
		
		if self.use_preset_registry:
			registry_ = FINGERPRINT_REGISTRY.copy()
		else:
			registry_ = {}
		
		if self.registry:
			registry_.update(**self.registry)
		
		return registry_
	
	def _generate_hooks_js(self) -> str:
		"""
		Generates the JavaScript code that hooks into browser APIs for detection and spoofing.

		Returns:
			str: The generated hooks block.
		"""
		
		registry_ = self._get_registry()
		
		hooks: List[str] = []
		register_items = {item.path: item for item in registry_.values()}
		
		for path, entry in register_items.items():
			is_spoofed: bool = entry is not None and entry.spoofing_rule is not None
			is_detected: bool = (
					self.detect_events_mode == "always"
					or self.detect_events_mode == "not_spoofed"
					and not is_spoofed
			)
		
			hooks.append(
					get_hook_js(path=path, entry=entry, is_detected=is_detected, is_spoofed=is_spoofed)
			)
		
		return "\n".join(hooks)
	
	def _generate_modifiers_js(self) -> str:
		"""
		Generates the JavaScript code that defines spoofing modifiers.

		Returns:
			str: The generated modifiers block.
		"""
		
		registry_ = self._get_registry()
		lines = []
		
		for key, parameter in registry_.items():
			if parameter.spoofing_rule is not None:
				js_func = parameter.spoofing_rule.generate_js(path=parameter.path)
				lines.append(f"MODIFIERS['{parameter.path}'] = {js_func};")
		
		return "\n".join(lines)
	
	def generate_js(self) -> str:
		"""
		Generates the complete JavaScript code to inject into the browser.

		This methods combines the fingerprint injection script with the dynamic
		modifiers and detection hooks based on the current configuration.

		Returns:
			str: The executable JavaScript code.
		"""
		
		scripts = get_js_scripts()
		
		return inject_data_in_js_script(
				script=scripts.start_fingerprint_detection,
				data={
					"__MODIFIERS_PLACEHOLDER__": add_code_level(code=self._generate_modifiers_js(), num=1),
					"__DETECTION_PLACEHOLDER__": add_code_level(code=self._generate_hooks_js(), num=1),
					"__SETTINGS__PLACEHOLDER__": convert_to_js_value(value={"optimize_events": self.optimize_events})
				},
				convert_to_js=False,
		)
