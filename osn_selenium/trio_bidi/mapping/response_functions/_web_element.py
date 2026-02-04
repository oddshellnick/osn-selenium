from typing import Any, Dict
from selenium.webdriver.remote.command import Command
from osn_selenium.trio_bidi._typehints import (
	MAP_RESPONSE_FUNCTION_TYPEHINT,
	REQUEST_PARAMS_TYPEHINT
)
from osn_selenium.trio_bidi.mapping.response_functions._args_validators import (
	validate_element_exceptions,
	validate_no_such_element
)
from osn_selenium.trio_bidi.mapping.response_functions._args_helpers import (
	build_w3c_element,
	build_w3c_shadow_root,
	map_js_primitive_response,
	map_js_response,
	map_void_response
)


__all__ = ["MAPPED_RESPONSE_WEB_ELEMENT_COMMANDS"]


def _map_send_keys_to_element_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps keyboard input result to W3C void response.

	Args:
		bidi_result (Dict[str, Any]): BiDi response.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C void response.
	"""
	
	element_exceptions_validation = validate_element_exceptions(bidi_result=bidi_result, request_params=request_params)
	if element_exceptions_validation is not None:
		return element_exceptions_validation
	
	return map_void_response(bidi_result=bidi_result, request_params=request_params)


def _map_is_element_selected_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps element selection check result.

	Args:
		bidi_result (Dict[str, Any]): BiDi script result.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C boolean response.
	"""
	
	element_exceptions_validation = validate_element_exceptions(bidi_result=bidi_result, request_params=request_params)
	if element_exceptions_validation is not None:
		return element_exceptions_validation
	
	return map_js_primitive_response(bidi_result=bidi_result, request_params=request_params)


def _map_is_element_enabled_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps element enablement check result.

	Args:
		bidi_result (Dict[str, Any]): BiDi script result.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C boolean response.
	"""
	
	element_exceptions_validation = validate_element_exceptions(bidi_result=bidi_result, request_params=request_params)
	if element_exceptions_validation is not None:
		return element_exceptions_validation
	
	return map_js_primitive_response(bidi_result=bidi_result, request_params=request_params)


def _map_get_shadow_root_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps BiDi shadow root node result to W3C shadow root reference.

	Args:
		bidi_result (Dict[str, Any]): BiDi script result containing node.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C shadow root dictionary.
	"""
	
	element_exceptions_validation = validate_element_exceptions(bidi_result=bidi_result, request_params=request_params)
	if element_exceptions_validation is not None:
		return element_exceptions_validation
	
	remote_value = bidi_result.get("result", {})
	shared_id = remote_value.get("sharedId")
	
	return {"value": build_w3c_shadow_root(shared_id)}


def _map_get_element_text_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps element text script result to W3C format.

	Args:
		bidi_result (Dict[str, Any]): BiDi script result.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C string response.
	"""
	
	element_exceptions_validation = validate_element_exceptions(bidi_result=bidi_result, request_params=request_params)
	if element_exceptions_validation is not None:
		return element_exceptions_validation
	
	return map_js_primitive_response(bidi_result=bidi_result, request_params=request_params)


def _map_get_element_tag_name_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps element tag name script result to W3C format.

	Args:
		bidi_result (Dict[str, Any]): BiDi script result.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C string response.
	"""
	
	element_exceptions_validation = validate_element_exceptions(bidi_result=bidi_result, request_params=request_params)
	if element_exceptions_validation is not None:
		return element_exceptions_validation
	
	return map_js_primitive_response(bidi_result=bidi_result, request_params=request_params)


def _map_get_element_rect_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps element bounding rect script result to W3C rect format.

	Args:
		bidi_result (Dict[str, Any]): BiDi script result containing rect object.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C response with x, y, width, height.
	"""
	
	element_exceptions_validation = validate_element_exceptions(bidi_result=bidi_result, request_params=request_params)
	if element_exceptions_validation is not None:
		return element_exceptions_validation
	
	return map_js_response(bidi_result=bidi_result, request_params=request_params)


def _map_get_element_property_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps element property script result to W3C format.

	Args:
		bidi_result (Dict[str, Any]): BiDi script result.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C response with property value.
	"""
	
	element_exceptions_validation = validate_element_exceptions(bidi_result=bidi_result, request_params=request_params)
	if element_exceptions_validation is not None:
		return element_exceptions_validation
	
	return map_js_primitive_response(bidi_result=bidi_result, request_params=request_params)


def _map_get_element_css_value_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps computed CSS value script result to W3C format.

	Args:
		bidi_result (Dict[str, Any]): BiDi script result.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C string response.
	"""
	
	element_exceptions_validation = validate_element_exceptions(bidi_result=bidi_result, request_params=request_params)
	if element_exceptions_validation is not None:
		return element_exceptions_validation
	
	return map_js_primitive_response(bidi_result=bidi_result, request_params=request_params)


def _map_get_element_attribute_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps element attribute script result to W3C format.

	Args:
		bidi_result (Dict[str, Any]): BiDi script result.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C string response.
	"""
	
	element_exceptions_validation = validate_element_exceptions(bidi_result=bidi_result, request_params=request_params)
	if element_exceptions_validation is not None:
		return element_exceptions_validation
	
	return map_js_primitive_response(bidi_result=bidi_result, request_params=request_params)


def _map_get_element_aria_role_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps element ARIA role script result to W3C format.

	Args:
		bidi_result (Dict[str, Any]): BiDi script result.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C string response.
	"""
	
	element_exceptions_validation = validate_element_exceptions(bidi_result=bidi_result, request_params=request_params)
	if element_exceptions_validation is not None:
		return element_exceptions_validation
	
	return map_js_primitive_response(bidi_result=bidi_result, request_params=request_params)


def _map_get_element_aria_label_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps element ARIA label script result to W3C format.

	Args:
		bidi_result (Dict[str, Any]): BiDi script result.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C string response.
	"""
	
	element_exceptions_validation = validate_element_exceptions(bidi_result=bidi_result, request_params=request_params)
	if element_exceptions_validation is not None:
		return element_exceptions_validation
	
	return map_js_primitive_response(bidi_result=bidi_result, request_params=request_params)


def _map_find_child_elements_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps BiDi nodes found as children to W3C list of element references.

	Args:
		bidi_result (Dict[str, Any]): BiDi result containing 'nodes'.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C response with a list of element dicts.
	"""
	
	element_exceptions_validation = validate_element_exceptions(bidi_result=bidi_result, request_params=request_params)
	if element_exceptions_validation is not None:
		return element_exceptions_validation
	
	nodes = bidi_result.get("nodes", [])
	value = [build_w3c_element(node["sharedId"]) for node in nodes]
	
	return {"value": value}


def _map_find_child_element_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps first BiDi node found as child to W3C element reference, validating existence.

	Args:
		bidi_result (Dict[str, Any]): BiDi result containing 'nodes'.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C response with an element dict or error.
	"""
	
	nodes = bidi_result.get("nodes", [])
	
	no_such_element_validation = validate_no_such_element(nodes=nodes, request_params=request_params)
	if no_such_element_validation is not None:
		return no_such_element_validation
	
	return {"value": build_w3c_element(nodes[0]["sharedId"])}


def _map_element_screenshot_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Extracts base64 element screenshot data from BiDi result.

	Args:
		bidi_result (Dict[str, Any]): BiDi response containing 'data'.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C response with base64 data.
	"""
	
	return {"value": bidi_result.get("data")}


def _map_click_element_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps element click script result to W3C void response.

	Args:
		bidi_result (Dict[str, Any]): BiDi response.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C void response.
	"""
	
	element_exceptions_validation = validate_element_exceptions(bidi_result=bidi_result, request_params=request_params)
	if element_exceptions_validation is not None:
		return element_exceptions_validation
	
	return map_void_response(bidi_result=bidi_result, request_params=request_params)


def _map_clear_element_response(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Maps element clear script result to W3C void response.

	Args:
		bidi_result (Dict[str, Any]): BiDi response.
		request_params (REQUEST_PARAMS_TYPEHINT): Original request parameters.

	Returns:
		Dict[str, Any]: W3C void response.
	"""
	
	element_exceptions_validation = validate_element_exceptions(bidi_result=bidi_result, request_params=request_params)
	if element_exceptions_validation is not None:
		return element_exceptions_validation
	
	return map_void_response(bidi_result=bidi_result, request_params=request_params)


MAPPED_RESPONSE_WEB_ELEMENT_COMMANDS: Dict[str, MAP_RESPONSE_FUNCTION_TYPEHINT] = {
	Command.GET_ELEMENT_TAG_NAME: _map_get_element_tag_name_response,
	Command.GET_ELEMENT_TEXT: _map_get_element_text_response,
	Command.CLICK_ELEMENT: _map_click_element_response,
	Command.CLEAR_ELEMENT: _map_clear_element_response,
	Command.GET_ELEMENT_PROPERTY: _map_get_element_property_response,
	Command.GET_ELEMENT_ATTRIBUTE: _map_get_element_attribute_response,
	Command.IS_ELEMENT_SELECTED: _map_is_element_selected_response,
	Command.IS_ELEMENT_ENABLED: _map_is_element_enabled_response,
	Command.SEND_KEYS_TO_ELEMENT: _map_send_keys_to_element_response,
	Command.GET_SHADOW_ROOT: _map_get_shadow_root_response,
	Command.GET_ELEMENT_RECT: _map_get_element_rect_response,
	Command.GET_ELEMENT_VALUE_OF_CSS_PROPERTY: _map_get_element_css_value_response,
	Command.GET_ELEMENT_ARIA_ROLE: _map_get_element_aria_role_response,
	Command.GET_ELEMENT_ARIA_LABEL: _map_get_element_aria_label_response,
	Command.ELEMENT_SCREENSHOT: _map_element_screenshot_response,
	Command.FIND_CHILD_ELEMENT: _map_find_child_element_response,
	Command.FIND_CHILD_ELEMENTS: _map_find_child_elements_response,
}
