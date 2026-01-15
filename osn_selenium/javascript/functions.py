import pathlib
from typing import (
    Any,
    Iterable,
    Mapping,
    Optional
)

from osn_selenium.javascript.types import JS_Scripts

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


def _convert_to_js_value(value: Any) -> str:
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
        return f"{{ {', '.join(f'{k}: {_convert_to_js_value(value=v)}' for k, v in value.items())} }}"

    if isinstance(value, Iterable):
        return f"[ {', '.join(_convert_to_js_value(value=v) for v in value)} ]"

    return str(value)


def inject_settings_in_js_script(script: str, settings: Mapping[str, Any]) -> str:
    """
    Injects configuration settings into a JavaScript script template.

    This function replaces a specific placeholder in the script with a JavaScript object
    constructed from the provided settings dictionary.

    Args:
        script (str): The JavaScript source code containing the `__SETTINGS__PLACEHOLDER__`.
        settings (Mapping[str, Any]): A dictionary of settings to inject into the script.

    Returns:
        str: The modified JavaScript code with settings injected.
    """

    settings_placeholder = _convert_to_js_value(value=settings)

    return script.replace("__SETTINGS__PLACEHOLDER__", settings_placeholder)
