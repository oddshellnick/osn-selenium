from typing import (
	Any,
	Dict,
	List,
	Optional
)
from osn_selenium.instances.protocols import AnyInstanceWrapper
from osn_selenium.trio_bidi.mapping._constants import BY_MAPPING_DICT
from osn_selenium.trio_bidi.mapping._utils import (
	ELEMENT_KEY,
	SHADOW_ROOT_KEY
)
from selenium.webdriver.remote.webelement import (
	WebElement as SeleniumWebElement
)
from osn_selenium.trio_bidi._typehints import (
	CURRENT_BROWSING_CONTEXT_TYPEHINT,
	REQUEST_PARAMS_TYPEHINT
)


__all__ = [
	"build_bidi_element",
	"build_locate_nodes_request",
	"build_script_call_request",
	"build_script_evaluate_request",
	"convert_w3c_to_bidi_js",
	"get_shadow_root_argument",
	"get_web_element_argument"
]


def build_bidi_element(id_: str) -> Dict[str, Any]:
	"""
	Creates a BiDi element reference.

	Args:
		id_ (str): The shared ID of the element.

	Returns:
		Dict[str, Any]: The BiDi sharedId reference.
	"""
	
	return {"sharedId": id_}


def get_web_element_argument(params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Extracts the element ID from W3C parameters and creates a BiDi reference.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): W3C parameters containing 'id'.

	Returns:
		Dict[str, Any]: The BiDi element reference.
	"""
	
	return build_bidi_element(id_=params["id"])


def get_shadow_root_argument(params: REQUEST_PARAMS_TYPEHINT) -> Dict[str, Any]:
	"""
	Extracts the shadow ID from W3C parameters and creates a BiDi reference.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): W3C parameters containing 'shadowId'.

	Returns:
		Dict[str, Any]: The BiDi element reference.
	"""
	
	return build_bidi_element(id_=params["shadowId"])


def convert_w3c_to_bidi_js(w3c_value: Any) -> Dict[str, Any]:
	"""
	Converts a W3C-style JavaScript argument into a BiDi LocalValue.

	Args:
		w3c_value (Any): The value to convert.

	Returns:
		Dict[str, Any]: The BiDi LocalValue representation.

	EXAMPLES
	________
	>>> convert_w3c_to_bidi_js("hello")
	... {'type': 'string', 'value': 'hello'}
	>>> convert_w3c_to_bidi_js(True)
	... {'type': 'boolean', 'value': True}
	"""
	
	if isinstance(w3c_value, AnyInstanceWrapper):
		w3c_value = w3c_value.legacy
	
	if isinstance(w3c_value, SeleniumWebElement):
		return {"sharedId": w3c_value.id}
	
	if isinstance(w3c_value, dict):
		if ELEMENT_KEY in w3c_value:
			return {"sharedId": w3c_value[ELEMENT_KEY]}
	
		if SHADOW_ROOT_KEY in w3c_value:
			return {"sharedId": w3c_value[SHADOW_ROOT_KEY]}
	
	if w3c_value is None:
		return {"type": "null"}
	
	if isinstance(w3c_value, bool):
		return {"type": "boolean", "value": w3c_value}
	
	if isinstance(w3c_value, (int, float)):
		return {"type": "number", "value": w3c_value}
	
	if isinstance(w3c_value, str):
		return {"type": "string", "value": w3c_value}
	
	if isinstance(w3c_value, (list, tuple, set)):
		return {
			"type": "array",
			"value": [convert_w3c_to_bidi_js(w3c_value=item) for item in w3c_value]
		}
	
	if isinstance(w3c_value, dict):
		return {
			"type": "object",
			"value": [
				[
					convert_w3c_to_bidi_js(w3c_value=key),
					convert_w3c_to_bidi_js(w3c_value=value)
				]
				for key, value in w3c_value.items()
			]
		}
	
	return {"type": "undefined"}


def build_script_evaluate_request(context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT, expression: str) -> Dict[str, Any]:
	"""
	Builds a BiDi 'script.evaluate' request.

	Args:
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.
		expression (str): The JS expression to evaluate.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	return {
		"method": "script.evaluate",
		"params": {
			"expression": expression,
			"target": {"context": context_id},
			"awaitPromise": True,
			"resultOwnership": "none",
		}
	}


def build_script_call_request(
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT,
		function: str,
		args: Optional[List[Any]],
		ownership: str
) -> Dict[str, Any]:
	"""
	Builds a BiDi 'script.callFunction' request.

	Args:
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.
		function (str): The function declaration.
		args (Optional[List[Any]]): List of BiDi LocalValue arguments.
		ownership (str): Result ownership type ('none', 'root').

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	return {
		"method": "script.callFunction",
		"params": {
			"functionDeclaration": function,
			"arguments": args or [],
			"target": {"context": context_id},
			"awaitPromise": True,
			"resultOwnership": ownership,
		}
	}


def build_locate_nodes_request(
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT,
		params: REQUEST_PARAMS_TYPEHINT,
		max_nodes: Optional[int] = None,
		start_nodes: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
	"""
	Builds a BiDi 'browsingContext.locateNodes' request.

	Args:
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.
		params (REQUEST_PARAMS_TYPEHINT): W3C search parameters ('using', 'value').
		max_nodes (Optional[int]): Maximum number of nodes to return.
		start_nodes (Optional[List[Dict[str, Any]]]): BiDi element references to start search from.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	strategy = BY_MAPPING_DICT.get(params["using"], params["using"])
	
	bidi_params: Dict[str, Any] = {
		"context": context_id,
		"locator": {"type": strategy, "value": params["value"]}
	}
	
	if max_nodes:
		bidi_params["maxNodeCount"] = max_nodes
	
	if start_nodes:
		bidi_params["startNodes"] = start_nodes
	
	return {"method": "browsingContext.locateNodes", "params": bidi_params}
