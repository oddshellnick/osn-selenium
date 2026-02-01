from typing import Any, Dict
from selenium.webdriver.remote.command import Command
from osn_selenium.trio_bidi.mapping.response_functions._args_helpers import map_js_response
from osn_selenium.trio_bidi._typehints import (
	MAP_RESPONSE_FUNCTION_TYPEHINT,
	REQUEST_PARAMS_TYPEHINT
)
from osn_selenium.trio_bidi.mapping.response_functions._args_validators import (
	validate_javascript_error
)


__all__ = ["MAPPED_RESPONSE_SCRIPT_COMMANDS"]


def _map_w3c_execute_script_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps BiDi callFunction result back to W3C script execution result.

	Args:
		bidi_result (Dict[str, Any]): BiDi response containing 'result'.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C response with the converted Python value.
	"""
	
	javascript_error_validation = validate_javascript_error(bidi_result=bidi_result, request_params=request_params)
	if javascript_error_validation is not None:
		return javascript_error_validation
	
	return map_js_response(bidi_result=bidi_result, request_params=request_params)


def _map_w3c_execute_script_async_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps BiDi async callFunction result back to W3C async script execution result.

	Args:
		bidi_result (Dict[str, Any]): BiDi response containing 'result'.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C response with the converted Python value.
	"""
	
	javascript_error_validation = validate_javascript_error(bidi_result=bidi_result, request_params=request_params)
	if javascript_error_validation is not None:
		return javascript_error_validation
	
	return map_js_response(bidi_result=bidi_result, request_params=request_params)


MAPPED_RESPONSE_SCRIPT_COMMANDS: Dict[str, MAP_RESPONSE_FUNCTION_TYPEHINT] = {
	Command.W3C_EXECUTE_SCRIPT: _map_w3c_execute_script_response,
	Command.W3C_EXECUTE_SCRIPT_ASYNC: _map_w3c_execute_script_async_response,
}
