from typing import Any, Dict
from selenium.webdriver.remote.command import Command
from osn_selenium.trio_bidi.mapping.request_functions._args_helpers import (
	build_locate_nodes_request,
	get_shadow_root_argument
)
from osn_selenium.trio_bidi._typehints import (
	CURRENT_BROWSING_CONTEXT_TYPEHINT,
	MAP_REQUEST_FUNCTION_TYPEHINT,
	REQUEST_PARAMS_TYPEHINT
)


__all__ = ["MAPPED_REQUEST_SHADOW_ROOT_COMMANDS"]


def _map_find_elements_from_shadow_root_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps the find elements from shadow root command to BiDi 'locateNodes'.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Strategy, value and shadow ID.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	return build_locate_nodes_request(
			context_id=context_id,
			params=params,
			start_nodes=[get_shadow_root_argument(params=params)],
	)


def _map_find_element_from_shadow_root_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps the find element from shadow root command to BiDi 'locateNodes' (max 1).

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Strategy, value and shadow ID.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	return build_locate_nodes_request(
			context_id=context_id,
			params=params,
			max_nodes=1,
			start_nodes=[get_shadow_root_argument(params=params)],
	)


MAPPED_REQUEST_SHADOW_ROOT_COMMANDS: Dict[str, MAP_REQUEST_FUNCTION_TYPEHINT] = {
	Command.FIND_ELEMENT_FROM_SHADOW_ROOT: _map_find_element_from_shadow_root_request,
	Command.FIND_ELEMENTS_FROM_SHADOW_ROOT: _map_find_elements_from_shadow_root_request,
}
