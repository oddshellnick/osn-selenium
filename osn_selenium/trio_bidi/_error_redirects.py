from typing import Any, Dict
from selenium.webdriver.remote.command import Command
from selenium.webdriver.remote.errorhandler import ErrorCode
from osn_selenium.trio_bidi._error_mappings import (
	create_w3c_error_response,
	map_bidi_error_to_w3c
)


__all__ = ["redirect_error_response"]


class _Redirect_:
	"""
	Internal container for logic to redirect certain error types to others based on the command.
	"""
	
	class InvalidArgument_:
		"""
		Logic for InvalidArgument redirection.
		"""
		
		to_NoAlertPresent_Commands = [
			Command.W3C_GET_ALERT_TEXT,
			Command.W3C_ACCEPT_ALERT,
			Command.W3C_DISMISS_ALERT,
			Command.W3C_SET_ALERT_VALUE
		]
		
		@staticmethod
		def to_NoAlertPresent(error_response: Dict[str, Any]) -> Dict[str, Any]:
			"""
			Redirects INVALID_ARGUMENT to NO_ALERT_OPEN if related to alerts/prompts.

			Args:
				error_response (Dict[str, Any]): The initial W3C error response.

			Returns:
				Dict[str, Any]: The redirected error response.
			"""
			
			value = error_response.get("value", {})
			
			if value.get("error") == ErrorCode.INVALID_ARGUMENT[1]:
				message = value.get("message", "").lower()
			
				if "alert" in message or "prompt" in message or "no such alert" in message:
					status_code, error_string = ErrorCode.NO_ALERT_OPEN
			
					return create_w3c_error_response(
							status_code=status_code,
							error_string=error_string,
							message="no such alert"
					)
			
			return error_response
	
	class NoSuchElement_:
		"""
		Logic for NoSuchElement redirection.
		"""
		
		to_DetachedShadowRoot_Commands = [
			Command.FIND_ELEMENT_FROM_SHADOW_ROOT,
			Command.FIND_ELEMENTS_FROM_SHADOW_ROOT,
		]
		
		to_StaleElementReference_Commands = [
			Command.GET_ELEMENT_TAG_NAME,
			Command.GET_ELEMENT_TEXT,
			Command.CLICK_ELEMENT,
			Command.CLEAR_ELEMENT,
			Command.GET_ELEMENT_PROPERTY,
			Command.GET_ELEMENT_ATTRIBUTE,
			Command.IS_ELEMENT_SELECTED,
			Command.IS_ELEMENT_ENABLED,
			Command.SEND_KEYS_TO_ELEMENT,
			Command.GET_SHADOW_ROOT,
			Command.GET_ELEMENT_RECT,
			Command.GET_ELEMENT_VALUE_OF_CSS_PROPERTY,
			Command.GET_ELEMENT_ARIA_ROLE,
			Command.GET_ELEMENT_ARIA_LABEL,
			Command.ELEMENT_SCREENSHOT,
			Command.FIND_CHILD_ELEMENT,
			Command.FIND_CHILD_ELEMENTS,
		]
		
		@staticmethod
		def to_DetachedShadowRoot(error_response: Dict[str, Any]) -> Dict[str, Any]:
			"""
			Redirects NO_SUCH_ELEMENT to DETACHED_SHADOW_ROOT.

			Args:
				error_response (Dict[str, Any]): The initial W3C error response.

			Returns:
				Dict[str, Any]: The redirected error response.
			"""
			
			if error_response.get("status") == ErrorCode.NO_SUCH_ELEMENT[0]:
				status_code, error_string = ErrorCode.DETACHED_SHADOW_ROOT
				message = "detached shadow root: shadow root is no longer attached to the document"
			
				return create_w3c_error_response(status_code=status_code, error_string=error_string, message=message)
			
			return error_response
		
		@staticmethod
		def to_StaleElementReference(error_response: Dict[str, Any]) -> Dict[str, Any]:
			"""
			Redirects NO_SUCH_ELEMENT to STALE_ELEMENT_REFERENCE.

			Args:
				error_response (Dict[str, Any]): The initial W3C error response.

			Returns:
				Dict[str, Any]: The redirected error response.
			"""
			
			if error_response.get("status") == ErrorCode.NO_SUCH_ELEMENT[0]:
				status_code, error_string = ErrorCode.STALE_ELEMENT_REFERENCE
				message = "stale element reference: element is not attached to the page document"
			
				return create_w3c_error_response(status_code=status_code, error_string=error_string, message=message)
			
			return error_response
	
	class NoSuchFrame_:
		"""
		Logic for NoSuchFrame redirection.
		"""
		
		to_NoSuchWindow_Commands = [
			Command.SWITCH_TO_WINDOW,
			Command.GET_CURRENT_URL,
			Command.GET_TITLE,
			Command.CLOSE,
			Command.SCREENSHOT,
			Command.PRINT_PAGE,
			Command.GET_PAGE_SOURCE,
			Command.SET_SCREEN_ORIENTATION,
			Command.GET_SCREEN_ORIENTATION,
		]
		
		@staticmethod
		def to_NoSuchWindow(error_response: Dict[str, Any]):
			"""
			Redirects NO_SUCH_FRAME to NO_SUCH_WINDOW.

			Args:
				error_response (Dict[str, Any]): The initial W3C error response.

			Returns:
				Dict[str, Any]: The redirected error response.
			"""
			
			value = error_response.get("value", {})
			
			if value.get("error") == ErrorCode.NO_SUCH_FRAME[1]:
				status_code, error_string = ErrorCode.NO_SUCH_WINDOW
				message = "no such window"
			
				return create_w3c_error_response(status_code=status_code, error_string=error_string, message=message)
			
			return error_response


def redirect_error_response(command: str, bidi_response: Dict[str, Any]) -> Dict[str, Any]:
	"""
	Main entry point for mapping BiDi errors to W3C and applying redirection logic.

	Args:
		command (str): The original W3C command.
		bidi_response (Dict[str, Any]): The raw error data from BiDi.

	Returns:
		Dict[str, Any]: The finalized W3C error response.
	"""
	
	error_response = map_bidi_error_to_w3c(bidi_error_data=bidi_response)
	
	if command in _Redirect_.NoSuchFrame_.to_NoSuchWindow_Commands:
		return _Redirect_.NoSuchFrame_.to_NoSuchWindow(error_response=error_response)
	
	if command in _Redirect_.InvalidArgument_.to_NoAlertPresent_Commands:
		return _Redirect_.InvalidArgument_.to_NoAlertPresent(error_response=error_response)
	
	if command in _Redirect_.NoSuchElement_.to_StaleElementReference_Commands:
		return _Redirect_.NoSuchElement_.to_StaleElementReference(error_response=error_response)
	
	if command in _Redirect_.NoSuchElement_.to_DetachedShadowRoot_Commands:
		return _Redirect_.NoSuchElement_.to_DetachedShadowRoot(error_response=error_response)
	
	return error_response
