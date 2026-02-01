from typing import Any, Dict
from selenium.webdriver.remote.command import Command
from osn_selenium.trio_bidi._typehints import (
	MAP_RESPONSE_FUNCTION_TYPEHINT,
	REQUEST_PARAMS_TYPEHINT
)
from osn_selenium.trio_bidi.mapping.response_functions._args_validators import (
	validate_javascript_error
)
from osn_selenium.trio_bidi.mapping.response_functions._args_helpers import (
	map_js_primitive_response,
	map_void_response
)


__all__ = ["MAPPED_RESPONSE_NAVIGATION_COMMANDS"]


def _map_refresh_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps BiDi reload result to W3C void response.

	Args:
		bidi_result (Dict[str, Any]): BiDi response.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C void response.
	"""
	
	return map_void_response(bidi_result=bidi_result, request_params=request_params)


def _map_get_title_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps BiDi title script result to W3C title response.

	Args:
		bidi_result (Dict[str, Any]): BiDi response with title value.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C response with title string.
	"""
	
	javascript_error_validation = validate_javascript_error(bidi_result=bidi_result, request_params=request_params)
	if javascript_error_validation is not None:
		return javascript_error_validation
	
	return map_js_primitive_response(bidi_result=bidi_result, request_params=request_params)


def _map_get_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps BiDi navigate result to W3C void response.

	Args:
		bidi_result (Dict[str, Any]): BiDi response.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C void response.
	"""
	
	return map_void_response(bidi_result=bidi_result, request_params=request_params)


def _map_get_current_url_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps BiDi getTree result to W3C current URL response.

	Args:
		bidi_result (Dict[str, Any]): BiDi response containing browsing context info.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C response with the current URL string.
	"""
	
	return {"value": bidi_result["contexts"][0]["url"]}


def _map_forward_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps BiDi history traverse result to W3C void response.

	Args:
		bidi_result (Dict[str, Any]): BiDi response.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C void response.
	"""
	
	return map_void_response(bidi_result=bidi_result, request_params=request_params)


def _map_back_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps BiDi history traverse result to W3C void response.

	Args:
		bidi_result (Dict[str, Any]): BiDi response.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C void response.
	"""
	
	return map_void_response(bidi_result=bidi_result, request_params=request_params)


MAPPED_RESPONSE_NAVIGATION_COMMANDS: Dict[str, MAP_RESPONSE_FUNCTION_TYPEHINT] = {
	Command.GET: _map_get_response,
	Command.GET_CURRENT_URL: _map_get_current_url_response,
	Command.REFRESH: _map_refresh_response,
	Command.GO_BACK: _map_back_response,
	Command.GO_FORWARD: _map_forward_response,
	Command.GET_TITLE: _map_get_title_response,
}
