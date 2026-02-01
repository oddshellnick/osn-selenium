from typing import Any, Dict
from selenium.webdriver.remote.command import Command
from osn_selenium.trio_bidi._typehints import (
	MAP_RESPONSE_FUNCTION_TYPEHINT,
	REQUEST_PARAMS_TYPEHINT
)
from osn_selenium.trio_bidi.mapping.response_functions._args_helpers import (
	map_js_primitive_response,
	map_void_response
)


__all__ = ["MAPPED_RESPONSE_ALERT_COMMANDS"]


def _map_w3c_set_alert_value_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps BiDi response for setting alert value to W3C void response.

	Args:
		bidi_result (Dict[str, Any]): BiDi response result.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C void response.
	"""
	
	return map_void_response(bidi_result=bidi_result, request_params=request_params)


def _map_w3c_get_alert_text_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps BiDi response for alert text to W3C primitive response.

	Args:
		bidi_result (Dict[str, Any]): BiDi response result.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C response with the alert text.
	"""
	
	return map_js_primitive_response(bidi_result=bidi_result, request_params=request_params)


def _map_w3c_dismiss_alert_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps BiDi response for dismissing alert to W3C void response.

	Args:
		bidi_result (Dict[str, Any]): BiDi response result.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C void response.
	"""
	
	return map_void_response(bidi_result=bidi_result, request_params=request_params)


def _map_w3c_accept_alert_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps BiDi response for accepting alert to W3C void response.

	Args:
		bidi_result (Dict[str, Any]): BiDi response result.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C void response.
	"""
	
	return map_void_response(bidi_result=bidi_result, request_params=request_params)


MAPPED_RESPONSE_ALERT_COMMANDS: Dict[str, MAP_RESPONSE_FUNCTION_TYPEHINT] = {
	Command.W3C_GET_ALERT_TEXT: _map_w3c_get_alert_text_response,
	Command.W3C_ACCEPT_ALERT: _map_w3c_accept_alert_response,
	Command.W3C_DISMISS_ALERT: _map_w3c_dismiss_alert_response,
	Command.W3C_SET_ALERT_VALUE: _map_w3c_set_alert_value_response,
}
