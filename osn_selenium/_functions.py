import pathlib

from osn_selenium.utils import JS_Scripts


def read_js_scripts() -> JS_Scripts:
	"""
	Reads JavaScript scripts from files and returns them in a JS_Scripts object.

	This function locates all `.js` files within the 'js_scripts' directory, which is expected to be located two levels above the current file's directory.
	It reads the content of each JavaScript file, using UTF-8 encoding, and stores these scripts in a dictionary-like `_JS_Scripts` object.
	The filenames (without the `.js` extension) are used as keys in the `_JS_Scripts` object to access the script content.

	Returns:
		JS_Scripts: An object of type _JS_Scripts, containing the content of each JavaScript file as attributes.
	"""

	scripts = {}

	for script_file in (pathlib.Path(__file__).parent / "js_scripts").iterdir():
		scripts[script_file.stem] = open(script_file, "r", encoding="utf-8").read()

	return JS_Scripts(
			check_element_in_viewport=scripts["check_element_in_viewport"],
			get_document_scroll_size=scripts["get_document_scroll_size"],
			get_element_css=scripts["get_element_css"],
			get_element_rect_in_viewport=scripts["get_element_rect_in_viewport"],
			get_random_element_point_in_viewport=scripts["get_random_element_point_in_viewport"],
			get_viewport_position=scripts["get_viewport_position"],
			get_viewport_rect=scripts["get_viewport_rect"],
			get_viewport_size=scripts["get_viewport_size"],
			open_new_tab=scripts["open_new_tab"],
			stop_window_loading=scripts["stop_window_loading"],
	)
