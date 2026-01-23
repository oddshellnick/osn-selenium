from typing import (
	Any,
	Iterable,
	Mapping
)


__all__ = ["convert_to_js_value", "inject_data_in_js_script"]


def convert_to_js_value(value: Any) -> str:
	"""
	Converts a Python value to its JavaScript string representation.

	Args:
		value (Any): The value to convert. Can be a boolean, string, mapping, iterable, or None.

	Returns:
		str: The JavaScript string representation of the value.
	"""
	
	if isinstance(value, (str, bytes)):
		return f'"{value}"'
	
	if isinstance(value, bool):
		return "true" if value else "false"
	
	if value is None:
		return "null"
	
	if isinstance(value, Mapping):
		return f"{{{', '.join(f'{k}: {convert_to_js_value(value=v)}' for k, v in value.items())}}}"
	
	if isinstance(value, Iterable):
		return f"[{', '.join(convert_to_js_value(value=v) for v in value)}]"
	
	return str(value)


def inject_data_in_js_script(script: str, data: Mapping[str, Any], convert_to_js: bool = True) -> str:
	"""
	Injects data into a JavaScript template string by replacing placeholders.

	Args:
		script (str): The JavaScript template string.
		data (Mapping[str, Any]): A dictionary mapping placeholders to values.
		convert_to_js (bool): If True, converts values to JS syntax before replacement.

	Returns:
		str: The modified JavaScript string with data injected.
	"""
	
	injected_script = script
	
	for placeholder, value in data.items():
		if convert_to_js:
			replacement = convert_to_js_value(value)
		else:
			replacement = str(value)
	
		injected_script = injected_script.replace(placeholder, replacement)
	
	return injected_script
