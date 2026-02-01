from typing import Any, Dict
from selenium.webdriver.remote.command import Command
from osn_selenium.trio_bidi.mapping._js_snippets import NAVIGATION
from osn_selenium.trio_bidi.mapping.request_functions._args_helpers import (
	build_script_evaluate_request
)
from osn_selenium.trio_bidi._typehints import (
	CURRENT_BROWSING_CONTEXT_TYPEHINT,
	MAP_REQUEST_FUNCTION_TYPEHINT,
	REQUEST_PARAMS_TYPEHINT
)


__all__ = ["MAPPED_REQUEST_NAVIGATION_COMMANDS"]


def _map_refresh_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps the refresh command to BiDi 'browsingContext.reload'.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Request parameters.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	return {
		"method": "browsingContext.reload",
		"params": {"context": context_id, "ignoreCache": True, "wait": "interactive"}
	}


def _map_get_title_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps the get title command to a JS evaluation.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Request parameters.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	return build_script_evaluate_request(context_id=context_id, expression=NAVIGATION.GET_TITLE)


def _map_get_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps the navigate command to BiDi 'browsingContext.navigate'.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Parameters containing 'url'.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	return {
		"method": "browsingContext.navigate",
		"params": {"context": context_id, "url": params["url"], "wait": "interactive"}
	}


def _map_get_current_url_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps the get current URL command to BiDi 'browsingContext.getTree'.

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


def _map_forward_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps the forward history command to BiDi history traversal.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Request parameters.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	return {
		"method": "browsingContext.traverseHistory",
		"params": {"context": context_id, "delta": 1}
	}


def _map_back_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps the back history command to BiDi history traversal.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Request parameters.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	return {
		"method": "browsingContext.traverseHistory",
		"params": {"context": context_id, "delta": -1}
	}


MAPPED_REQUEST_NAVIGATION_COMMANDS: Dict[str, MAP_REQUEST_FUNCTION_TYPEHINT] = {
	Command.GET: _map_get_request,
	Command.GET_CURRENT_URL: _map_get_current_url_request,
	Command.REFRESH: _map_refresh_request,
	Command.GO_BACK: _map_back_request,
	Command.GO_FORWARD: _map_forward_request,
	Command.GET_TITLE: _map_get_title_request,
}
