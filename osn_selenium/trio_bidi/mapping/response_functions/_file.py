from typing import Any, Dict
from selenium.webdriver.remote.command import Command
from osn_selenium.trio_bidi.mapping.response_functions._args_helpers import (
	map_js_primitive_response
)
from osn_selenium.trio_bidi._typehints import (
	MAP_RESPONSE_FUNCTION_TYPEHINT,
	REQUEST_PARAMS_TYPEHINT
)


__all__ = ["MAPPED_RESPONSE_FILE_COMMANDS"]


def _map_upload_file_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps BiDi file upload result to W3C response format.

	Args:
		bidi_result (Dict[str, Any]): BiDi internal response.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C response with the file path.
	"""
	
	return map_js_primitive_response(bidi_result=bidi_result, request_params=request_params)


MAPPED_RESPONSE_FILE_COMMANDS: Dict[str, MAP_RESPONSE_FUNCTION_TYPEHINT] = {Command.UPLOAD_FILE: _map_upload_file_response}
