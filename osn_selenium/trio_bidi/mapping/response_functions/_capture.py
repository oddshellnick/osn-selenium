from typing import Any, Dict
from selenium.webdriver.remote.command import Command
from osn_selenium.trio_bidi.mapping.response_functions._args_helpers import (
	map_js_primitive_response
)
from osn_selenium.trio_bidi._typehints import (
	MAP_RESPONSE_FUNCTION_TYPEHINT,
	REQUEST_PARAMS_TYPEHINT
)
from osn_selenium.trio_bidi.mapping.response_functions._args_validators import (
	validate_javascript_error
)


__all__ = ["MAPPED_RESPONSE_CAPTURE_COMMANDS"]


def _map_screenshot_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Extracts base64 screenshot data from BiDi result.

	Args:
		bidi_result (Dict[str, Any]): BiDi response containing 'data'.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C response with base64 data.
	"""
	
	return {"value": bidi_result.get("data")}


def _map_print_page_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Extracts base64 PDF data from BiDi print result.

	Args:
		bidi_result (Dict[str, Any]): BiDi response containing 'data'.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C response with base64 data.
	"""
	
	return {"value": bidi_result.get("data")}


def _map_get_page_source_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps BiDi script evaluation result to page source string.

	Args:
		bidi_result (Dict[str, Any]): BiDi response with JS evaluation result.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C response with HTML string.
	"""
	
	javascript_error_validation = validate_javascript_error(bidi_result=bidi_result, request_params=request_params)
	if javascript_error_validation is not None:
		return javascript_error_validation
	
	return map_js_primitive_response(bidi_result, request_params)


MAPPED_RESPONSE_CAPTURE_COMMANDS: Dict[str, MAP_RESPONSE_FUNCTION_TYPEHINT] = {
	Command.SCREENSHOT: _map_screenshot_response,
	Command.GET_PAGE_SOURCE: _map_get_page_source_response,
	Command.PRINT_PAGE: _map_print_page_response,
}
