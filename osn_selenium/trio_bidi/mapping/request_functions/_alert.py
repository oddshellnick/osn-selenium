from typing import Any, Dict
from selenium.webdriver.remote.command import Command
from osn_selenium.trio_bidi._internal_mappings import (
	GET_INTERNAL_ALERT_TEXT
)
from osn_selenium.trio_bidi._typehints import (
	CURRENT_BROWSING_CONTEXT_TYPEHINT,
	MAP_REQUEST_FUNCTION_TYPEHINT,
	REQUEST_PARAMS_TYPEHINT
)


__all__ = ["MAPPED_REQUEST_ALERT_COMMANDS"]


def _map_set_alert_value_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps the 'set alert value' command to BiDi 'handleUserPrompt'.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Request parameters containing 'text'.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	return {
		"method": "browsingContext.handleUserPrompt",
		"params": {"context": context_id, "accept": True, "userText": params.get("text")}
	}


def _map_get_alert_text_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps the 'get alert text' command to an internal bridge command.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Request parameters.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The internal BiDi request.
	"""
	
	return {"method": GET_INTERNAL_ALERT_TEXT, "params": {}}


def _map_dismiss_alert_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps the 'dismiss alert' command to BiDi 'handleUserPrompt' with accept=False.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Request parameters.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	return {
		"method": "browsingContext.handleUserPrompt",
		"params": {"context": context_id, "accept": False}
	}


def _map_accept_alert_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps the 'accept alert' command to BiDi 'handleUserPrompt' with accept=True.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Request parameters.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	return {
		"method": "browsingContext.handleUserPrompt",
		"params": {"context": context_id, "accept": True}
	}


MAPPED_REQUEST_ALERT_COMMANDS: Dict[str, MAP_REQUEST_FUNCTION_TYPEHINT] = {
	Command.W3C_GET_ALERT_TEXT: _map_get_alert_text_request,
	Command.W3C_ACCEPT_ALERT: _map_accept_alert_request,
	Command.W3C_DISMISS_ALERT: _map_dismiss_alert_request,
	Command.W3C_SET_ALERT_VALUE: _map_set_alert_value_request,
}
