import pathlib
from osn_selenium.javascript.types import JS_Scripts
from typing import (
	Any,
	Iterable,
	Mapping,
	Optional
)


__all__ = ["convert_to_js_value", "inject_data_in_js_script", "read_js_scripts"]

_CACHED_JS_SCRIPTS: Optional[JS_Scripts] = None


def read_js_scripts() -> JS_Scripts:
	"""
	Reads JavaScript scripts from files and returns them in a JS_Scripts object.

	This function locates all `.js` files within the 'scripts' directory, which is expected
	to be located in the same parent directory as this module. It reads the content of each
	JavaScript file using UTF-8 encoding and stores these scripts in a `JS_Scripts` model.
	The filenames (without the `.js` extension) are used as keys.

	Returns:
		JS_Scripts: An object containing the content of each JavaScript file as attributes.
	"""
	
	global _CACHED_JS_SCRIPTS
	
	if _CACHED_JS_SCRIPTS is None:
		scripts = {}
		path_to_js_scripts = pathlib.Path(__file__).parent / "scripts"
	
		for script_file in path_to_js_scripts.iterdir():
			scripts[script_file.stem] = script_file.read_text(encoding="utf-8")
	
		_CACHED_JS_SCRIPTS = JS_Scripts.model_validate(scripts)
	
	return _CACHED_JS_SCRIPTS


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
