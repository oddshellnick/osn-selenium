from typing import Any, Dict
from selenium.webdriver.remote.command import Command
from osn_selenium.trio_bidi.mapping.request_functions._args_helpers import (
	build_script_call_request,
	convert_w3c_to_bidi_js
)
from osn_selenium.trio_bidi._typehints import (
	CURRENT_BROWSING_CONTEXT_TYPEHINT,
	MAP_REQUEST_FUNCTION_TYPEHINT,
	REQUEST_PARAMS_TYPEHINT
)


__all__ = ["MAPPED_REQUEST_SCRIPT_COMMANDS"]


def _map_w3c_execute_script_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps synchronous script execution to BiDi 'script.callFunction'.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Script and arguments.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	script = params.get("script", "")
	args = params.get("args", [])
	bidi_args = [convert_w3c_to_bidi_js(w3c_value=arg) for arg in args]
	
	return build_script_call_request(
			context_id=context_id,
			function=f"function() {{ {script} }}",
			args=bidi_args,
			ownership="none",
	)


def _map_w3c_execute_script_async_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps asynchronous script execution to a Promise-based BiDi 'script.callFunction'.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Script and arguments.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The BiDi request.
	"""
	
	script = params.get("script", "")
	args = params.get("args", [])
	bidi_args = [convert_w3c_to_bidi_js(w3c_value=arg) for arg in args]
	
	wrapper_script = f"""
function() {{
	return new Promise((resolve) => {{
		const args = Array.from(arguments);
		const callback = (result) => resolve(result);
		args.push(callback);
		(function() {{ {script} }}).apply(null, args);
	}});
}}
"""
	
	return build_script_call_request(
			context_id=context_id,
			function=wrapper_script,
			args=bidi_args,
			ownership="none",
	)


MAPPED_REQUEST_SCRIPT_COMMANDS: Dict[str, MAP_REQUEST_FUNCTION_TYPEHINT] = {
	Command.W3C_EXECUTE_SCRIPT: _map_w3c_execute_script_request,
	Command.W3C_EXECUTE_SCRIPT_ASYNC: _map_w3c_execute_script_async_request,
}
