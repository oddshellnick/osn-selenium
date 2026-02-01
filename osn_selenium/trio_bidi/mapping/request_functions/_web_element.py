import os
from typing import Any, Dict
from selenium.webdriver.remote.command import Command
from osn_selenium.trio_bidi.mapping._js_snippets import WEB_ELEMENT
from osn_selenium.trio_bidi._typehints import (
	CURRENT_BROWSING_CONTEXT_TYPEHINT,
	MAP_REQUEST_FUNCTION_TYPEHINT,
	REQUEST_PARAMS_TYPEHINT
)
from osn_selenium.trio_bidi.mapping.request_functions._args_helpers import (
	build_locate_nodes_request,
	build_script_call_request,
	get_web_element_argument
)


__all__ = ["MAPPED_REQUEST_WEB_ELEMENT_COMMANDS"]


def _map_send_keys_to_element_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps send keys to element, handling file uploads if needed.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Parameters containing 'text'.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	text_to_type = {"type": "string", "value": params.get("text", "")}
	files = [line for line in text_to_type["value"].split("\n")]
	
	if all(os.path.isfile(file) for file in files):
		return {
			"method": "input.setFiles",
			"params": {
				"context": context_id,
				"element": get_web_element_argument(params),
				"files": files,
			}
		}
	
	return build_script_call_request(
			context_id=context_id,
			function=WEB_ELEMENT.SEND_KEYS_TO,
			args=[get_web_element_argument(params=params), text_to_type],
			ownership="none",
	)


def _map_is_element_selected_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps is element selected via JS call.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Element parameters.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	return build_script_call_request(
			context_id=context_id,
			function=WEB_ELEMENT.IS_SELECTED,
			args=[get_web_element_argument(params=params)],
			ownership="none",
	)


def _map_is_element_enabled_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps is element enabled via JS call.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Element parameters.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	return build_script_call_request(
			context_id=context_id,
			function=WEB_ELEMENT.IS_ENABLED,
			args=[get_web_element_argument(params=params)],
			ownership="none",
	)


def _map_get_shadow_root_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps get shadow root via JS call with 'root' ownership.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Element parameters.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	return build_script_call_request(
			context_id=context_id,
			function=WEB_ELEMENT.GET_SHADOW_ROOT,
			args=[get_web_element_argument(params=params)],
			ownership="root",
	)


def _map_get_element_text_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps get element text via JS call.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Element parameters.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	return build_script_call_request(
			context_id=context_id,
			function=WEB_ELEMENT.GET_TEXT,
			args=[get_web_element_argument(params=params)],
			ownership="none",
	)


def _map_get_element_tag_name_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps get element tag name via JS call.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Element parameters.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	return build_script_call_request(
			context_id=context_id,
			function=WEB_ELEMENT.GET_TAG,
			args=[get_web_element_argument(params=params)],
			ownership="none",
	)


def _map_get_element_rect_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps get element rect via JS call.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Element parameters.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	return build_script_call_request(
			context_id=context_id,
			function=WEB_ELEMENT.GET_RECT,
			args=[get_web_element_argument(params=params)],
			ownership="none",
	)


def _map_get_element_property_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps get element property via JS call.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Element and property name.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	prop_name = {"type": "string", "value": params["name"]}
	
	return build_script_call_request(
			context_id=context_id,
			function=WEB_ELEMENT.GET_PROPERTY,
			args=[get_web_element_argument(params=params), prop_name],
			ownership="none",
	)


def _map_get_element_css_value_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps get computed CSS value via JS call.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Element and CSS property name.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	prop_name = {"type": "string", "value": params["propertyName"]}
	
	return build_script_call_request(
			context_id=context_id,
			function=WEB_ELEMENT.GET_CSS,
			args=[get_web_element_argument(params=params), prop_name],
			ownership="none",
	)


def _map_get_element_attribute_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps get attribute via JS call.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Element and attribute name.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	attr_name = {"type": "string", "value": params["name"]}
	
	return build_script_call_request(
			context_id=context_id,
			function=WEB_ELEMENT.GET_ATTRIBUTE,
			args=[get_web_element_argument(params=params), attr_name],
			ownership="none",
	)


def _map_get_element_aria_role_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps get ARIA role via JS call.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Element parameters.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	return build_script_call_request(
			context_id=context_id,
			function=WEB_ELEMENT.GET_ARIA_ROLE,
			args=[get_web_element_argument(params=params)],
			ownership="none",
	)


def _map_get_element_aria_label_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps get ARIA label via JS call.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Element parameters.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	return build_script_call_request(
			context_id=context_id,
			function=WEB_ELEMENT.GET_ARIA_LABEL,
			args=[get_web_element_argument(params=params)],
			ownership="none",
	)


def _map_find_child_elements_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps find child elements from a parent element.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Strategy, value and parent element ID.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	return build_locate_nodes_request(
			context_id=context_id,
			params=params,
			start_nodes=[get_web_element_argument(params=params)]
	)


def _map_find_child_element_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps find child element from a parent element (max 1).

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Strategy, value and parent element ID.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	return build_locate_nodes_request(
			context_id=context_id,
			params=params,
			max_nodes=1,
			start_nodes=[get_web_element_argument(params=params)]
	)


def _map_element_screenshot_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps element-specific screenshot command.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Element ID.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	return {
		"method": "browsingContext.captureScreenshot",
		"params": {
			"context": context_id,
			"clip": {"type": "element", "element": get_web_element_argument(params=params)}
		}
	}


def _map_click_element_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps element click via JS call.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Element ID.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	return build_script_call_request(
			context_id=context_id,
			function=WEB_ELEMENT.CLICK,
			args=[get_web_element_argument(params=params)],
			ownership="none",
	)


def _map_clear_element_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps element clear via JS call.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Element ID.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	return build_script_call_request(
			context_id=context_id,
			function=WEB_ELEMENT.CLEAR,
			args=[get_web_element_argument(params=params)],
			ownership="none",
	)


MAPPED_REQUEST_WEB_ELEMENT_COMMANDS: Dict[str, MAP_REQUEST_FUNCTION_TYPEHINT] = {
	Command.GET_ELEMENT_TAG_NAME: _map_get_element_tag_name_request,
	Command.GET_ELEMENT_TEXT: _map_get_element_text_request,
	Command.CLICK_ELEMENT: _map_click_element_request,
	Command.CLEAR_ELEMENT: _map_clear_element_request,
	Command.GET_ELEMENT_PROPERTY: _map_get_element_property_request,
	Command.GET_ELEMENT_ATTRIBUTE: _map_get_element_attribute_request,
	Command.IS_ELEMENT_SELECTED: _map_is_element_selected_request,
	Command.IS_ELEMENT_ENABLED: _map_is_element_enabled_request,
	Command.SEND_KEYS_TO_ELEMENT: _map_send_keys_to_element_request,
	Command.GET_SHADOW_ROOT: _map_get_shadow_root_request,
	Command.GET_ELEMENT_RECT: _map_get_element_rect_request,
	Command.GET_ELEMENT_VALUE_OF_CSS_PROPERTY: _map_get_element_css_value_request,
	Command.GET_ELEMENT_ARIA_ROLE: _map_get_element_aria_role_request,
	Command.GET_ELEMENT_ARIA_LABEL: _map_get_element_aria_label_request,
	Command.ELEMENT_SCREENSHOT: _map_element_screenshot_request,
	Command.FIND_CHILD_ELEMENT: _map_find_child_element_request,
	Command.FIND_CHILD_ELEMENTS: _map_find_child_elements_request,
}
