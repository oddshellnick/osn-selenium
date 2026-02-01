from typing import Any, Dict
from selenium.webdriver.remote.command import Command
from osn_selenium.trio_bidi.mapping.response_functions._args_helpers import map_void_response
from osn_selenium.trio_bidi._typehints import (
	MAP_RESPONSE_FUNCTION_TYPEHINT,
	REQUEST_PARAMS_TYPEHINT
)
from osn_selenium.trio_bidi.mapping.response_functions._args_validators import (
	validate_javascript_error
)


__all__ = ["MAPPED_RESPONSE_WINDOW_COMMANDS"]


def _map_w3c_get_window_handles_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps BiDi context tree into a list of W3C window handles.

	Args:
		bidi_result (Dict[str, Any]): BiDi result containing 'contexts'.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C response with a list of handles.
	"""
	
	contexts = bidi_result.get("contexts", [])
	handles = [ctx["context"] for ctx in contexts]
	
	return {"value": handles}


def _map_w3c_get_current_window_handle_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps specific BiDi context ID to W3C window handle response.

	Args:
		bidi_result (Dict[str, Any]): BiDi result containing single context info.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C response with the handle string.
	"""
	
	return {"value": bidi_result["contexts"][0]["context"]}


def _map_set_screen_orientation_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps screen orientation script execution result to void response.

	Args:
		bidi_result (Dict[str, Any]): BiDi response.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C void response.
	"""
	
	javascript_error_validation = validate_javascript_error(bidi_result=bidi_result, request_params=request_params)
	if javascript_error_validation is not None:
		return javascript_error_validation
	
	return map_void_response(bidi_result=bidi_result, request_params=request_params)


def _map_get_screen_orientation_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps BiDi screen orientation script result into W3C orientation dictionary.

	Args:
		bidi_result (Dict[str, Any]): BiDi result containing raw orientation string.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C response with orientation info.
	"""
	
	javascript_error_validation = validate_javascript_error(bidi_result=bidi_result, request_params=request_params)
	if javascript_error_validation is not None:
		return javascript_error_validation
	
	raw_value = bidi_result.get("result", {}).get("value", "").upper()
	
	if "LANDSCAPE" in raw_value:
		orientation = "LANDSCAPE"
	elif "PORTRAIT" in raw_value:
		orientation = "PORTRAIT"
	else:
		orientation = "LANDSCAPE"
	
	return {"value": {"orientation": orientation}}


def _map_close_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps window closing result to W3C void response.

	Args:
		bidi_result (Dict[str, Any]): BiDi response.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C void response.
	"""
	
	return map_void_response(bidi_result=bidi_result, request_params=request_params)


MAPPED_RESPONSE_WINDOW_COMMANDS: Dict[str, MAP_RESPONSE_FUNCTION_TYPEHINT] = {
	Command.W3C_GET_WINDOW_HANDLES: _map_w3c_get_window_handles_response,
	Command.W3C_GET_CURRENT_WINDOW_HANDLE: _map_w3c_get_current_window_handle_response,
	Command.CLOSE: _map_close_response,
	Command.GET_SCREEN_ORIENTATION: _map_get_screen_orientation_response,
	Command.SET_SCREEN_ORIENTATION: _map_set_screen_orientation_response,
}

# TODO create mappings for Command.GET_WINDOW_RECT, Command.SET_WINDOW_RECT, Command.W3C_MAXIMIZE_WINDOW, Command.MINIMIZE_WINDOW, Command.FULLSCREEN_WINDOW
