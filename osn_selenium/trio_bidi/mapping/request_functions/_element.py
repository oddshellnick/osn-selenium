from typing import Any, Dict
from selenium.webdriver.remote.command import Command
from osn_selenium.trio_bidi.mapping.request_functions._args_helpers import (
	build_locate_nodes_request
)
from osn_selenium.trio_bidi._typehints import (
	CURRENT_BROWSING_CONTEXT_TYPEHINT,
	MAP_REQUEST_FUNCTION_TYPEHINT,
	REQUEST_PARAMS_TYPEHINT
)


__all__ = ["MAPPED_REQUEST_ELEMENT_COMMANDS"]


def _map_find_elements_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps the 'find elements' command to BiDi 'locateNodes'.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Strategy and value.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	return build_locate_nodes_request(context_id=context_id, params=params)


def _map_find_element_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps the 'find element' command to BiDi 'locateNodes' with max count of 1.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Strategy and value.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	return build_locate_nodes_request(context_id=context_id, params=params, max_nodes=1)


MAPPED_REQUEST_ELEMENT_COMMANDS: Dict[str, MAP_REQUEST_FUNCTION_TYPEHINT] = {
	Command.FIND_ELEMENT: _map_find_element_request,
	Command.FIND_ELEMENTS: _map_find_elements_request
}
