from typing import Optional
from osn_selenium.javascript.fingerprint._decorators import indent_code
from osn_selenium.javascript.fingerprint._functions import add_code_level
from osn_selenium.javascript.fingerprint.registry.models import RegistryItem
from osn_selenium.javascript.fingerprint._detect.templates import (
	ARG_WRAPPER_LOGIC,
	CALL_ORIGINAL_METHOD,
	CALL_ORIGINAL_PROP,
	DESCRIPTOR_LOOKUP_METHOD,
	DESCRIPTOR_LOOKUP_PROP,
	HOOK_IIFE_WRAPPER,
	METADATA_PRESERVATION,
	PART_ARG_WRAPPER,
	PART_REPORT,
	PART_SPOOF_METHOD,
	PART_SPOOF_PROP,
	REPORT_LOGIC,
	TARGET_RESOLUTION,
	WRAPPER_CONSTRUCTOR_SKELETON,
	WRAPPER_METHOD_SKELETON,
	WRAPPER_PROP_SKELETON
)


__all__ = [
	"build_function_body",
	"get_arg_wrapper_js",
	"get_constructor_hook_body",
	"get_hook_js",
	"get_method_hook_body",
	"get_prop_hook_body"
]


def build_function_body(
		report_js: str,
		arg_wrapper_js: Optional[str],
		call_original: Optional[str],
		spoof_path: Optional[str],
		is_method: bool,
		indent_level: int,
) -> str:
	"""
	Constructs the internal body of a hook function in JavaScript.

	Args:
		report_js (str): The JavaScript code for reporting.
		arg_wrapper_js (Optional[str]): The JavaScript code for argument wrapping.
		call_original (Optional[str]): The JavaScript code to call the original method/property.
		spoof_path (Optional[str]): The path key for looking up spoofing modifiers.
		is_method (bool): True if building a method hook, False for a property hook.
		indent_level (int): The indentation level to apply to the generated code.

	Returns:
		str: The indented JavaScript function body.
	"""
	
	parts = []
	
	if report_js:
		parts.append(PART_REPORT.format(report_logic=report_js))
	
	if arg_wrapper_js:
		parts.append(PART_ARG_WRAPPER.format(arg_wrapper_logic=arg_wrapper_js))
	
	if call_original:
		parts.append(call_original)
	
	if spoof_path:
		template = PART_SPOOF_METHOD if is_method else PART_SPOOF_PROP
		parts.append(template.format(path=spoof_path))
	
	raw_body = "\n".join(parts)
	
	return add_code_level(code=raw_body, num=indent_level)


@indent_code
def get_constructor_hook_body(target: str, report_js: str, arg_wrapper_js: str) -> str:
	"""
	Generates the body of a constructor hook.

	Args:
		target (str): The JS target class name.
		report_js (str): JavaScript code for reporting usage.
		arg_wrapper_js (str): JavaScript code for wrapping arguments.

	Returns:
		str: The complete JavaScript code for hooking the constructor via Proxy.
	"""
	
	resolution = f"const originalClass = window['{target}'];\nif (!originalClass) return;"
	
	wrapper_body = build_function_body(
			report_js=report_js,
			arg_wrapper_js=arg_wrapper_js,
			call_original=None,
			spoof_path=None,
			is_method=True,
			indent_level=2,
	)
	
	wrapper = WRAPPER_CONSTRUCTOR_SKELETON.format(class_name=target, wrapper_body=wrapper_body)
	
	return f"{resolution}\n\n{wrapper}"


@indent_code
def get_prop_hook_body(target: str, name: str, report_js: str, spoof_path: Optional[str]) -> str:
	"""
	Generates the body of a property getter hook.

	Args:
		target (str): The JS target object (e.g., 'window').
		name (str): The name of the property.
		report_js (str): JavaScript code for reporting usage.
		spoof_path (Optional[str]): Path key for spoofing logic, if enabled.

	Returns:
		str: The complete JavaScript code for hooking the property.
	"""
	
	lookup = DESCRIPTOR_LOOKUP_PROP.format(prop_name=name)
	resolution = TARGET_RESOLUTION.format(target_object=target, descriptor_lookup=lookup)
	
	wrapper_body = build_function_body(
			report_js=report_js,
			arg_wrapper_js=None,
			call_original=CALL_ORIGINAL_PROP,
			spoof_path=spoof_path,
			is_method=False,
			indent_level=1,
	)
	
	wrapper = WRAPPER_PROP_SKELETON.format(prop_name=name, wrapper_body=wrapper_body)
	
	return f"{resolution}\n\n{wrapper}"


@indent_code
def get_method_hook_body(
		target: str,
		name: str,
		report_js: str,
		arg_wrapper_js: str,
		spoof_path: Optional[str]
) -> str:
	"""
	Generates the body of a method hook.

	Args:
		target (str): The JS target object.
		name (str): The name of the method.
		report_js (str): JavaScript code for reporting usage.
		arg_wrapper_js (str): JavaScript code for wrapping arguments.
		spoof_path (Optional[str]): Path key for spoofing logic, if enabled.

	Returns:
		str: The complete JavaScript code for hooking the method.
	"""
	
	lookup = DESCRIPTOR_LOOKUP_METHOD.format(method_name=name)
	resolution = TARGET_RESOLUTION.format(target_object=target, descriptor_lookup=lookup)
	
	wrapper_body = build_function_body(
			report_js=report_js,
			arg_wrapper_js=arg_wrapper_js,
			call_original=CALL_ORIGINAL_METHOD,
			spoof_path=spoof_path,
			is_method=True,
			indent_level=1,
	)
	
	wrapper = WRAPPER_METHOD_SKELETON.format(method_name=name, wrapper_body=wrapper_body)
	metadata = METADATA_PRESERVATION.format(method_name=name)
	
	return f"{resolution}\n\n{wrapper}\n\n{metadata}"


@indent_code
def get_arg_wrapper_js(entry: RegistryItem) -> str:
	"""
	Generates JavaScript code to wrap arguments if required by the registry entry.

	Args:
		entry (RegistryItem): The registry item containing configuration settings.

	Returns:
		str: The JavaScript code for argument wrapping, or an empty string if not applicable.
	"""
	
	if entry.settings is None:
		return ""
	
	index = entry.settings.get("wrapArgIndex")
	
	if index is None:
		return ""
	
	return ARG_WRAPPER_LOGIC.format(index=index, api=entry.api, name=entry.name or "constructor")


def get_hook_js(path: str, entry: RegistryItem, is_detected: bool, is_spoofed: bool) -> str:
	"""
	Generates the full IIFE JavaScript hook for a given registry entry.

	Args:
		path (str): The unique path identifier for the hook.
		entry (RegistryItem): The registry item configuration.
		is_detected (bool): Whether to include detection/reporting logic.
		is_spoofed (bool): Whether to include spoofing logic.

	Returns:
		str: The generated JavaScript code wrapped in an IIFE guard.
	"""
	
	spoof_path = path if is_spoofed else None
	
	report_js = ""
	arg_wrapper_js = ""
	
	if is_detected:
		name = entry.name if entry.name else "constructor"
		report_js = REPORT_LOGIC.format(api=entry.api, target=entry.target, name=name)
	
		if entry.type_ in ("method", "constructor"):
			arg_wrapper_js = get_arg_wrapper_js(entry=entry)
	
	if entry.type_ == "method":
		hook_body = get_method_hook_body(
				target=entry.target,
				name=entry.name,
				report_js=report_js,
				arg_wrapper_js=arg_wrapper_js,
				spoof_path=spoof_path,
		)
	elif entry.type_ == "prop":
		hook_body = get_prop_hook_body(
				target=entry.target,
				name=entry.name,
				report_js=report_js,
				spoof_path=spoof_path,
		)
	elif entry.type_ == "constructor":
		hook_body = get_constructor_hook_body(
				target=entry.target,
				report_js=report_js,
				arg_wrapper_js=arg_wrapper_js,
		)
	else:
		return ""
	
	return HOOK_IIFE_WRAPPER.format(hook_body=add_code_level(code=hook_body, num=1))
