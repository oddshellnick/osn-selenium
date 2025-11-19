import pathlib
from typing import Optional
from pydantic import ValidationError
from osn_selenium.javascript.models import JS_Scripts
from osn_selenium.exceptions.javascript import (
	JavaScriptResourceError
)


__all__ = ["get_js_scripts"]

_CACHED_JS_SCRIPTS: Optional[JS_Scripts] = None


def get_js_scripts() -> JS_Scripts:
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
	
		try:
			_CACHED_JS_SCRIPTS = JS_Scripts.model_validate(scripts)
		except ValidationError as exception:
			missing_fields = [error["loc"][0] for error in exception.errors()]
	
			raise JavaScriptResourceError(missing_script=missing_fields)
	
	return _CACHED_JS_SCRIPTS
