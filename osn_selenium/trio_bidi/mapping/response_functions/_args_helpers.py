from typing import Any, Dict
from osn_selenium.trio_bidi._internal_mappings import (
	OSN_SWITCH_CONTEXT_KEY
)
from osn_selenium.trio_bidi._typehints import (
	CURRENT_BROWSING_CONTEXT_TYPEHINT
)
from osn_selenium.trio_bidi.mapping._utils import (
	ELEMENT_KEY,
	SHADOW_ROOT_KEY
)


__all__ = [
	"build_w3c_element",
	"build_w3c_shadow_root",
	"convert_bidi_to_w3c_js",
	"inject_osn_switch_context_to_response",
	"map_js_primitive_response",
	"map_js_response",
	"map_rect_response",
	"map_void_response"
]


def map_void_response(bidi_result: Dict[str, Any], request_params: Any) -> Dict[str, Any]:
	"""
	Returns a standard W3C void response (value: null).

	Args:
		bidi_result (Dict[str, Any]): BiDi result dictionary.
		request_params (Any): Original request parameters.

	Returns:
		Dict[str, Any]: W3C response with null value.
	"""
	
	return {"value": None}


def map_rect_response(bidi_result: Dict[str, Any], request_params: Any) -> Dict[str, Any]:
	"""
	Maps BiDi geometric result to W3C rect format.

	Args:
		bidi_result (Dict[str, Any]): BiDi result containing geometry data.
		request_params (Any): Original request parameters.

	Returns:
		Dict[str, Any]: W3C response with x, y, width, height.
	"""
	
	return {
		"value": {
			"x": bidi_result.get("x", 0),
			"y": bidi_result.get("y", 0),
			"width": bidi_result.get("width", 0),
			"height": bidi_result.get("height", 0)
		}
	}


def convert_bidi_to_w3c_js(bidi_value: Dict[str, Any]) -> Any:
	"""
	Recursively converts a BiDi RemoteValue/LocalValue into a Python representation compatible with W3C.

	Args:
		bidi_value (Dict[str, Any]): The BiDi value dictionary to convert.

	Returns:
		Any: The converted value (dict, list, primitive, or element reference).
	"""
	
	if not isinstance(bidi_value, dict):
		return bidi_value
	
	rv_type = bidi_value.get("type")
	
	if rv_type in ("string", "number", "boolean"):
		return bidi_value.get("value")
	
	if rv_type == "null":
		return None
	
	if rv_type == "window":
		return bidi_value.get("value", {}).get("context")
	
	if rv_type == "node":
		shared_id = bidi_value.get("sharedId") or bidi_value.get("value", {}).get("sharedId")
		return {ELEMENT_KEY: shared_id}
	
	if rv_type == "array":
		return [convert_bidi_to_w3c_js(item) for item in bidi_value.get("value", [])]
	
	if rv_type == "object":
		result = {}
	
		for pair in bidi_value.get("value", []):
			k = convert_bidi_to_w3c_js(pair[0])
			v = convert_bidi_to_w3c_js(pair[1])
	
			result[k] = v
	
		return result
	
	return None


def map_js_response(bidi_result: Dict[str, Any], request_params: Any) -> Dict[str, Any]:
	"""
	Maps any BiDi RemoteValue to a W3C compatible Python object.

	Args:
		bidi_result (Dict[str, Any]): BiDi result containing 'result'.
		request_params (Any): Original request parameters.

	Returns:
		Dict[str, Any]: W3C response with converted value.
	"""
	
	remote_value = bidi_result.get("result", {})
	
	return {"value": convert_bidi_to_w3c_js(bidi_value=remote_value)}


def map_js_primitive_response(bidi_result: Dict[str, Any], request_params: Any) -> Dict[str, Any]:
	"""
	Maps a BiDi script result containing a simple value to W3C format.

	Args:
		bidi_result (Dict[str, Any]): BiDi result containing 'result.value'.
		request_params (Any): Original request parameters.

	Returns:
		Dict[str, Any]: W3C response with the primitive value.
	"""
	
	return {"value": bidi_result.get("result", {}).get("value")}


def inject_osn_switch_context_to_response(response: Dict[str, Any], context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT) -> Dict[str, Any]:
	"""
	Injects a special key into the response to notify the driver of a context switch.

	Args:
		response (Dict[str, Any]): The W3C response dictionary.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The target browsing context ID.

	Returns:
		Dict[str, Any]: Modified response dictionary.
	"""
	
	response[OSN_SWITCH_CONTEXT_KEY] = context_id
	
	return response


def build_w3c_shadow_root(id_: str) -> Dict[str, Any]:
	"""
	Wraps a shared ID into a W3C shadow root reference.

	Args:
		id_ (str): The shadow root shared ID.

	Returns:
		Dict[str, Any]: W3C shadow root dictionary.
	"""
	
	return {SHADOW_ROOT_KEY: id_}


def build_w3c_element(id_: str) -> Dict[str, Any]:
	"""
	Wraps a shared ID into a W3C element reference.

	Args:
		id_ (str): The element shared ID.

	Returns:
		Dict[str, Any]: W3C element dictionary.
	"""
	
	return {ELEMENT_KEY: id_}
