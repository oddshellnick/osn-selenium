import pathlib
from typing import Optional
from osn_selenium.types import JS_Scripts


def read_js_scripts() -> JS_Scripts:
	"""
	Reads JavaScript scripts from files and returns them in a JS_Scripts object.

	This function locates all `.js` files within the 'js_scripts' directory, which is expected to be located two levels above the current file's directory.
	It reads the content of each JavaScript file, using UTF-8 encoding, and stores these scripts in a dictionary-like `_JS_Scripts` object.
	The filenames (without the `.js` extension) are used as keys in the `_JS_Scripts` object to access the script content.

	Returns:
		JS_Scripts: An object of type _JS_Scripts, containing the content of each JavaScript file as attributes.
	"""
	
	global _CACHED_JS_SCRIPTS
	
	if _CACHED_JS_SCRIPTS is None:
		scripts = {}
		path_to_js_scripts = pathlib.Path(__file__).parent / "js_scripts"
	
		for script_file in path_to_js_scripts.iterdir():
			scripts[script_file.stem] = script_file.read_text(encoding="utf-8")
	
		_CACHED_JS_SCRIPTS = JS_Scripts.model_validate(scripts)
	
	return _CACHED_JS_SCRIPTS


_CACHED_JS_SCRIPTS: Optional[JS_Scripts] = None
