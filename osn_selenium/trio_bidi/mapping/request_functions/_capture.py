from typing import Any, Dict
from selenium.webdriver.remote.command import Command
from osn_selenium.trio_bidi.mapping._js_snippets import CAPTURE
from osn_selenium.trio_bidi._typehints import (
	MAP_REQUEST_FUNCTION_TYPEHINT,
	REQUEST_PARAMS_TYPEHINT
)
from osn_selenium.trio_bidi.mapping.request_functions._args_helpers import (
	build_script_evaluate_request
)


__all__ = ["MAPPED_REQUEST_CAPTURE_COMMANDS"]


def _map_screenshot_request(params: REQUEST_PARAMS_TYPEHINT, context_id: str) -> Dict[str, Any]:
	"""
	Maps the screenshot command to BiDi 'captureScreenshot'.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Request parameters.
		context_id (str): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	return {
		"method": "browsingContext.captureScreenshot",
		"params": {"context": context_id}
	}


def _map_print_page_request(params: REQUEST_PARAMS_TYPEHINT, context_id: str) -> Dict[str, Any]:
	"""
	Maps the print command to BiDi 'browsingContext.print'.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Print parameters.
		context_id (str): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	return {
		"method": "browsingContext.print",
		"params": {"context": context_id, **params}
	}


def _map_get_page_source_request(params: REQUEST_PARAMS_TYPEHINT, context_id: str) -> Dict[str, Any]:
	"""
	Maps the get page source command to a JS evaluation.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Request parameters.
		context_id (str): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	return build_script_evaluate_request(context_id=context_id, expression=CAPTURE.GET_PAGE_SOURCE)


MAPPED_REQUEST_CAPTURE_COMMANDS: Dict[str, MAP_REQUEST_FUNCTION_TYPEHINT] = {
	Command.SCREENSHOT: _map_screenshot_request,
	Command.GET_PAGE_SOURCE: _map_get_page_source_request,
	Command.PRINT_PAGE: _map_print_page_request,
}
