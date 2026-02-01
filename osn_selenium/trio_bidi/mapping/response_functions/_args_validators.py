from typing import (
	Any,
	Dict,
	Optional,
	Tuple
)
from selenium.webdriver.remote.errorhandler import ErrorCode
from osn_selenium.trio_bidi._typehints import (
	REQUEST_PARAMS_TYPEHINT
)
from osn_selenium.trio_bidi._error_mappings import (
	create_w3c_error_response
)


__all__ = [
	"validate_element_exceptions",
	"validate_javascript_error",
	"validate_no_such_element"
]


def validate_no_such_element(nodes: Any, request_params: REQUEST_PARAMS_TYPEHINT) -> Optional[Dict[str, Any]]:
	"""
	Checks if nodes list is empty and returns a NO_SUCH_ELEMENT error if so.

	Args:
		nodes (Any): The collection of nodes found.
		request_params (Optional[Dict[str, Any]]): Original request parameters for message details.

	Returns:
		Optional[Dict[str, Any]]: W3C error response if empty, else None.
	"""
	
	if not nodes:
		using = request_params.get("using", "unknown")
		value = request_params.get("value", "unknown")
	
		message = f"no such element: Unable to locate element: {{\"method\":\"{using}\",\"selector\":\"{value}\"}}"
		status_code, error_string = ErrorCode.NO_SUCH_ELEMENT
	
		return create_w3c_error_response(status_code=status_code, error_string=error_string, message=message)
	
	return None


def _get_js_exception_details(bidi_result: Dict[str, Any]) -> Tuple[Optional[str], str]:
	"""
	Extracts text and stacktrace from a BiDi exception result.

	Args:
		bidi_result (Dict[str, Any]): The BiDi response object.

	Returns:
		Tuple[Optional[str], str]: Lowercased error message and formatted stacktrace string.
	"""
	
	if bidi_result.get("type") != "exception":
		return None, ""
	
	details = bidi_result.get("exceptionDetails", {})
	text = details.get("text", "")
	
	stack_frames = details.get("stackTrace", {}).get("callFrames", [])
	stack_lines = []
	
	for frame in stack_frames:
		func = frame.get("functionName") or "anonymous"
		url = frame.get("url") or "unknown"
		line = frame.get("lineNumber", 0)
		col = frame.get("columnNumber", 0)
	
		stack_lines.append(f"    at {func} ({url}:{line}:{col})")
	
	return text.lower(), "\n".join(stack_lines)


def validate_javascript_error(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Optional[Dict[str, Any]]:
	"""
	Checks for script exceptions in BiDi result and converts them to JAVASCRIPT_ERROR.

	Args:
		bidi_result (Dict[str, Any]): Result from script evaluation.
		request_params (Optional[Dict[str, Any]]): Original request parameters.

	Returns:
		Optional[Dict[str, Any]]: W3C error response if exception occurred, else None.
	"""
	
	error_text, stack = _get_js_exception_details(bidi_result=bidi_result)
	
	if error_text:
		status_code, error_string = ErrorCode.JAVASCRIPT_ERROR
		message = f"javascript error: {error_text}"
	
		return create_w3c_error_response(
				status_code=status_code,
				error_string=error_string,
				message=message,
				stacktrace=stack
		)
	
	return None


def validate_element_exceptions(bidi_result: Dict[str, Any], request_params: REQUEST_PARAMS_TYPEHINT) -> Optional[Dict[str, Any]]:
	"""
	Validates script execution results for element-specific exceptions (stale, not interactable, etc.).

	Args:
		bidi_result (Dict[str, Any]): Result from script evaluation.
		request_params (Optional[Dict[str, Any]]): Original request parameters.

	Returns:
		Optional[Dict[str, Any]]: W3C error response if an element-related error occurred, else None.
	"""
	
	error_text, stack = _get_js_exception_details(bidi_result=bidi_result)
	
	if not error_text:
		return None
	
	mapping = {
		"stale element reference": ErrorCode.STALE_ELEMENT_REFERENCE,
		"no such shadow root": ErrorCode.NO_SUCH_SHADOW_ROOT,
		"element not interactable": ErrorCode.ELEMENT_NOT_INTERACTABLE,
		"invalid element state": ErrorCode.INVALID_ELEMENT_STATE,
		"element not selectable": ErrorCode.ELEMENT_IS_NOT_SELECTABLE,
		"element click intercepted": ErrorCode.ELEMENT_CLICK_INTERCEPTED,
		"invalid element coordinates": ErrorCode.INVALID_ELEMENT_COORDINATES,
	}
	
	for key, code_info in mapping.items():
		if key in error_text:
			raw_msg = bidi_result["result"]["exceptionDetails"]["text"]
	
			if key == "stale element reference":
				message = "stale element reference: element is not attached to the page document"
			else:
				message = raw_msg
	
			return create_w3c_error_response(
					status_code=code_info[0]
					if isinstance(code_info, list)
					else 13,
					error_string=code_info[1]
					if isinstance(code_info, list)
					else code_info[0],
					message=message,
					stacktrace=stack,
			)
	
	return validate_javascript_error(bidi_result, request_params)
