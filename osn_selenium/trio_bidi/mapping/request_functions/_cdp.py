from typing import Any, Dict
from osn_selenium.trio_bidi._typehints import (
	CURRENT_BROWSING_CONTEXT_TYPEHINT,
	MAP_REQUEST_FUNCTION_TYPEHINT,
	REQUEST_PARAMS_TYPEHINT
)


__all__ = ["MAPPED_REQUEST_CDP_COMMANDS"]


def _execute_cdp_command(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT,
) -> Dict[str, Any]:
	"""
	Maps a generic CDP send command to the BiDi Chrome-specific protocol.

	Args:
		params (Optional[Dict[str, Any]]): Parameters containing 'cmd' and 'params'.
		context_id (Optional[str]): The target browsing context ID.

	Returns:
		Dict[str, Any]: The mapped BiDi request.
	"""
	
	cdp_method = params.get("cmd", "")
	cdp_params = params.get("params", {})
	
	return {
		"method": "goog:cdp.sendCommand",
		"params": {
			"method": cdp_method,
			"params": cdp_params,
			"browsingContext": context_id,
		}
	}


MAPPED_REQUEST_CDP_COMMANDS: Dict[str, MAP_REQUEST_FUNCTION_TYPEHINT] = {"executeCdpCommand": _execute_cdp_command}
