from typing import Any, Dict
from selenium.webdriver.remote.command import Command
from osn_selenium.trio_bidi.mapping.response_functions._args_helpers import build_w3c_element
from osn_selenium.trio_bidi._typehints import (
	MAP_RESPONSE_FUNCTION_TYPEHINT,
	REQUEST_PARAMS_TYPEHINT
)
from osn_selenium.trio_bidi.mapping.response_functions._args_validators import (
	validate_no_such_element
)


__all__ = ["MAPPED_RESPONSE_ELEMENT_COMMANDS"]


def _map_find_elements_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Converts BiDi nodes into a list of W3C element references.

	Args:
		bidi_result (Dict[str, Any]): BiDi result containing 'nodes'.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C response containing a list of element dicts.
	"""
	
	nodes = bidi_result.get("nodes", [])
	value = [build_w3c_element(node["sharedId"]) for node in nodes]
	
	return {"value": value}


def _map_find_element_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Converts BiDi first node into a single W3C element reference, validating existence.

	Args:
		bidi_result (Dict[str, Any]): BiDi result containing 'nodes'.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C response containing an element dict or error.
	"""
	
	nodes = bidi_result.get("nodes", [])
	
	no_such_element_validation = validate_no_such_element(nodes=nodes, request_params=request_params)
	if no_such_element_validation is not None:
		return no_such_element_validation
	
	return {"value": build_w3c_element(nodes[0]["sharedId"])}


MAPPED_RESPONSE_ELEMENT_COMMANDS: Dict[str, MAP_RESPONSE_FUNCTION_TYPEHINT] = {
	Command.FIND_ELEMENT: _map_find_element_response,
	Command.FIND_ELEMENTS: _map_find_elements_response
}
