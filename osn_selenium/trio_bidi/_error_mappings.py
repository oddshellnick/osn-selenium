from typing import Any, Dict
from selenium.webdriver.remote.errorhandler import ErrorCode
from osn_selenium.exceptions.bidi_bridge import BiDiExecutionError


__all__ = [
	"BIDI_TO_W3C_ERROR_MAP",
	"create_w3c_error_response",
	"map_bidi_error_to_w3c"
]

_UNMAPPABLE_ERROR = (-1, "unmappable error")

BIDI_TO_W3C_ERROR_MAP = {
	"invalid argument": ErrorCode.INVALID_ARGUMENT,
	"invalid selector": ErrorCode.INVALID_SELECTOR,
	"invalid session id": ErrorCode.INVALID_SESSION_ID,
	"move target out of bounds": ErrorCode.MOVE_TARGET_OUT_OF_BOUNDS,
	"no such alert": ErrorCode.NO_ALERT_OPEN,
	"no such element": ErrorCode.NO_SUCH_ELEMENT,
	"no such frame": ErrorCode.NO_SUCH_FRAME,
	"no such window": ErrorCode.NO_SUCH_WINDOW,
	"no such cookie": ErrorCode.NO_SUCH_COOKIE,
	"stale element reference": ErrorCode.STALE_ELEMENT_REFERENCE,
	"element not interactable": ErrorCode.ELEMENT_NOT_INTERACTABLE,
	"element click intercepted": ErrorCode.ELEMENT_CLICK_INTERCEPTED,
	"javascript error": ErrorCode.JAVASCRIPT_ERROR,
	"timeout": ErrorCode.TIMEOUT,
	"script timeout": ErrorCode.SCRIPT_TIMEOUT,
	"session not created": ErrorCode.SESSION_NOT_CREATED,
	"unable to capture screen": ErrorCode.UNABLE_TO_CAPTURE_SCREEN,
	"unable to set cookie": ErrorCode.UNABLE_TO_SET_COOKIE,
	"unexpected alert open": ErrorCode.UNEXPECTED_ALERT_OPEN,
	"unknown command": ErrorCode.UNKNOWN_COMMAND,
	"unknown error": ErrorCode.UNKNOWN_ERROR,
	"unsupported operation": ErrorCode.METHOD_NOT_ALLOWED,
	"detached shadow root": ErrorCode.DETACHED_SHADOW_ROOT,
	"no such node": ErrorCode.NO_SUCH_ELEMENT,
	"no such handle": ErrorCode.NO_SUCH_ELEMENT,
	"no such client window": ErrorCode.NO_SUCH_WINDOW,
	"invalid web extension": _UNMAPPABLE_ERROR,
	"unable to set file input": _UNMAPPABLE_ERROR,
	"no such script": _UNMAPPABLE_ERROR,
	"no such history entry": _UNMAPPABLE_ERROR,
	"no such network collector": _UNMAPPABLE_ERROR,
	"no such intercept": _UNMAPPABLE_ERROR,
	"no such network data": _UNMAPPABLE_ERROR,
	"no such request": _UNMAPPABLE_ERROR,
	"no such storage partition": _UNMAPPABLE_ERROR,
	"no such user context": _UNMAPPABLE_ERROR,
	"no such web extension": _UNMAPPABLE_ERROR,
	"unable to close browser": _UNMAPPABLE_ERROR,
	"underspecified storage partition": _UNMAPPABLE_ERROR,
	"unavailable network data": _UNMAPPABLE_ERROR,
}


def create_w3c_error_response(
		status_code: int,
		error_string: str,
		message: str,
		stacktrace: str = ""
) -> Dict[str, Any]:
	"""
	Creates a standardized W3C WebDriver error response dictionary.

	Args:
		status_code (int): The numeric status code for the error.
		error_string (str): The string identifier for the error.
		message (str): The descriptive error message.
		stacktrace (str): The stacktrace associated with the error.

	Returns:
		Dict[str, Any]: Formatted W3C error response.
	"""
	
	return {
		"status": status_code,
		"value": {"error": error_string, "message": message, "stacktrace": stacktrace}
	}


def map_bidi_error_to_w3c(bidi_error_data: Dict[str, Any]) -> Dict[str, Any]:
	"""
	Maps a BiDi protocol error to the corresponding W3C WebDriver error response.

	Args:
		bidi_error_data (Dict[str, Any]): Dictionary containing error details from BiDi.

	Returns:
		Dict[str, Any]: Formatted W3C error response.

	Raises:
		BiDiExecutionError: If error data is malformed or represents an unmappable BiDi error.
	"""
	
	bidi_error = bidi_error_data.get("error", "unknown error")
	message = bidi_error_data.get("message", bidi_error)
	stacktrace = bidi_error_data.get("stacktrace", "")
	
	error_data = BIDI_TO_W3C_ERROR_MAP.get(bidi_error, ErrorCode.UNKNOWN_ERROR)
	
	if len(error_data) == 2:
		status_code, error_string = error_data
	else:
		status_code = 13
		error_string = error_data[0]
	
	try:
		status_code = int(status_code)
		error_string = str(error_string)
	except (ValueError, TypeError):
		raise BiDiExecutionError(error=bidi_error, message=f"Malformed error data: {message}")
	
	if (status_code, error_string) == _UNMAPPABLE_ERROR:
		raise BiDiExecutionError(error=error_string, message=message)
	
	return create_w3c_error_response(
			status_code=status_code,
			error_string=error_string,
			message=message,
			stacktrace=stacktrace,
	)
