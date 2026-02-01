from typing import Any, Dict
from selenium.webdriver.remote.command import Command
from osn_selenium.trio_bidi.mapping._js_snippets import WINDOW
from osn_selenium.trio_bidi.mapping.request_functions._args_helpers import (
	build_script_evaluate_request
)
from osn_selenium.trio_bidi._typehints import (
	CURRENT_BROWSING_CONTEXT_TYPEHINT,
	MAP_REQUEST_FUNCTION_TYPEHINT,
	REQUEST_PARAMS_TYPEHINT
)


__all__ = ["MAPPED_REQUEST_WINDOW_COMMANDS"]


def _map_w3c_get_window_handles_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps command to get all window handles.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Request parameters.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	return {"method": "browsingContext.getTree", "params": {}}


def _map_w3c_get_current_window_handle_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps command to get current window handle.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Request parameters.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	return {
		"method": "browsingContext.getTree",
		"params": {"root": context_id, "maxDepth": 0}
	}


def _map_set_screen_orientation_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps set screen orientation via JS evaluation.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Parameters containing 'orientation'.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	orientation = params.get("orientation").lower()
	
	return build_script_evaluate_request(
			context_id=context_id,
			expression=WINDOW.SET_ORIENTATION.format(orientation=orientation),
	)


def _map_get_screen_orientation_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps get screen orientation via JS evaluation.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Request parameters.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	return build_script_evaluate_request(context_id=context_id, expression=WINDOW.GET_ORIENTATION)


def _map_close_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps window close command.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Parameters containing 'handle'.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	target_context = params.get("handle") or context_id
	
	return {"method": "browsingContext.close", "params": {"context": target_context}}


MAPPED_REQUEST_WINDOW_COMMANDS: Dict[str, MAP_REQUEST_FUNCTION_TYPEHINT] = {
	Command.W3C_GET_WINDOW_HANDLES: _map_w3c_get_window_handles_request,
	Command.W3C_GET_CURRENT_WINDOW_HANDLE: _map_w3c_get_current_window_handle_request,
	Command.CLOSE: _map_close_request,
	Command.GET_SCREEN_ORIENTATION: _map_get_screen_orientation_request,
	Command.SET_SCREEN_ORIENTATION: _map_set_screen_orientation_request,
}

# TODO create mappings for Command.GET_WINDOW_RECT, Command.SET_WINDOW_RECT, Command.W3C_MAXIMIZE_WINDOW, Command.MINIMIZE_WINDOW, Command.FULLSCREEN_WINDOW
