from typing import Any, Dict
from selenium.webdriver.remote.command import Command
from osn_selenium.trio_bidi._typehints import (
	MAP_RESPONSE_FUNCTION_TYPEHINT,
	REQUEST_PARAMS_TYPEHINT
)
from osn_selenium.trio_bidi.mapping.response_functions._args_helpers import (
	inject_osn_switch_context_to_response,
	map_void_response
)


__all__ = ["MAPPED_RESPONSE_SWITCH_TO_COMMANDS"]


def _map_switch_to_window_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps window switching result, injecting the new context ID into response.

	Args:
		bidi_result (Dict[str, Any]): BiDi context tree info.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C response with context switch metadata.
	"""
	
	return inject_osn_switch_context_to_response(
			response=map_void_response(bidi_result=bidi_result, request_params=request_params),
			context_id=bidi_result["contexts"][0]["context"]
	)


def _map_new_window_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps window creation result, providing the new handle and injecting context switch.

	Args:
		bidi_result (Dict[str, Any]): BiDi creation result.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C response with the handle and context switch metadata.
	"""
	
	return inject_osn_switch_context_to_response(
			response={"value": {"handle": bidi_result["context"], "type": "tab"}},
			context_id=bidi_result["context"]
	)


MAPPED_RESPONSE_SWITCH_TO_COMMANDS: Dict[str, MAP_RESPONSE_FUNCTION_TYPEHINT] = {
	Command.SWITCH_TO_WINDOW: _map_switch_to_window_response,
	Command.NEW_WINDOW: _map_new_window_response,
}

# TODO create mappings for Command.SWITCH_TO_FRAME, Command.SWITCH_TO_PARENT_FRAME and Command.W3C_GET_ACTIVE_ELEMENT
