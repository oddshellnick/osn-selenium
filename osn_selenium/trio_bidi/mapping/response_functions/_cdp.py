from typing import Any, Dict
from osn_selenium.trio_bidi._typehints import (
	MAP_RESPONSE_FUNCTION_TYPEHINT,
	REQUEST_PARAMS_TYPEHINT
)


__all__ = ["MAPPED_RESPONSE_CDP_COMMANDS"]


def _execute_cdp_command(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps the result of a CDP command back to the W3C response format.

	Args:
		bidi_result (Dict[str, Any]): The result received from BiDi.
		request_params (Optional[Dict[str, Any]]): The original request parameters.

	Returns:
		Dict[str, Any]: The W3C-compatible result wrapper.
	"""
	
	return {"value": bidi_result.get("result")}


MAPPED_RESPONSE_CDP_COMMANDS: Dict[str, MAP_RESPONSE_FUNCTION_TYPEHINT] = {"executeCdpCommand": _execute_cdp_command}
