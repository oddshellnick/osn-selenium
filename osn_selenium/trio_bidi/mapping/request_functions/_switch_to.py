from typing import Any, Dict
from selenium.webdriver.remote.command import Command
from osn_selenium.trio_bidi._typehints import (
	CURRENT_BROWSING_CONTEXT_TYPEHINT,
	MAP_REQUEST_FUNCTION_TYPEHINT,
	REQUEST_PARAMS_TYPEHINT
)


__all__ = ["MAPPED_REQUEST_SWITCH_TO_COMMANDS"]


def _map_switch_to_window_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps switch to window command to BiDi 'browsingContext.getTree'.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Parameters containing 'handle'.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The current browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	target_handle = params.get("handle")
	
	return {
		"method": "browsingContext.getTree",
		"params": {"root": target_handle, "maxDepth": 0}
	}


def _map_new_window_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps new window command to BiDi 'browsingContext.create'.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Request parameters.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	return {"method": "browsingContext.create", "params": {"type": "tab"}}


MAPPED_REQUEST_SWITCH_TO_COMMANDS: Dict[str, MAP_REQUEST_FUNCTION_TYPEHINT] = {
	Command.SWITCH_TO_WINDOW: _map_switch_to_window_request,
	Command.NEW_WINDOW: _map_new_window_request,
}

# TODO create mappings for Command.SWITCH_TO_FRAME, Command.SWITCH_TO_PARENT_FRAME and Command.W3C_GET_ACTIVE_ELEMENT
