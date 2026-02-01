from typing import Any, Dict
from osn_selenium.exceptions.bidi_bridge import (
	CommandNotMappedToBiDiError
)
from osn_selenium.trio_bidi.mapping.response_functions._cdp import (
	MAPPED_RESPONSE_CDP_COMMANDS
)
from osn_selenium.trio_bidi.mapping.response_functions._file import (
	MAPPED_RESPONSE_FILE_COMMANDS
)
from osn_selenium.trio_bidi.mapping.response_functions._alert import (
	MAPPED_RESPONSE_ALERT_COMMANDS
)
from osn_selenium.trio_bidi.mapping.response_functions._script import (
	MAPPED_RESPONSE_SCRIPT_COMMANDS
)
from osn_selenium.trio_bidi.mapping.response_functions._window import (
	MAPPED_RESPONSE_WINDOW_COMMANDS
)
from osn_selenium.trio_bidi._typehints import (
	MAP_RESPONSE_FUNCTION_TYPEHINT,
	REQUEST_PARAMS_TYPEHINT
)
from osn_selenium.trio_bidi.mapping.response_functions._capture import (
	MAPPED_RESPONSE_CAPTURE_COMMANDS
)
from osn_selenium.trio_bidi.mapping.response_functions._element import (
	MAPPED_RESPONSE_ELEMENT_COMMANDS
)
from osn_selenium.trio_bidi.mapping.response_functions._switch_to import (
	MAPPED_RESPONSE_SWITCH_TO_COMMANDS
)
from osn_selenium.trio_bidi.mapping.response_functions._navigation import (
	MAPPED_RESPONSE_NAVIGATION_COMMANDS
)
from osn_selenium.trio_bidi.mapping.response_functions._web_element import (
	MAPPED_RESPONSE_WEB_ELEMENT_COMMANDS
)
from osn_selenium.trio_bidi.mapping.response_functions._shadow_root import (
	MAPPED_RESPONSE_SHADOW_ROOT_COMMANDS
)


__all__ = ["map_response"]

_MAPPED_RESPONSE_COMMANDS: Dict[str, MAP_RESPONSE_FUNCTION_TYPEHINT] = {
	**MAPPED_RESPONSE_ALERT_COMMANDS,
	**MAPPED_RESPONSE_CAPTURE_COMMANDS,
	**MAPPED_RESPONSE_CDP_COMMANDS,
	**MAPPED_RESPONSE_ELEMENT_COMMANDS,
	**MAPPED_RESPONSE_FILE_COMMANDS,
	**MAPPED_RESPONSE_NAVIGATION_COMMANDS,
	**MAPPED_RESPONSE_SCRIPT_COMMANDS,
	**MAPPED_RESPONSE_SHADOW_ROOT_COMMANDS,
	**MAPPED_RESPONSE_SWITCH_TO_COMMANDS,
	**MAPPED_RESPONSE_WEB_ELEMENT_COMMANDS,
	**MAPPED_RESPONSE_WINDOW_COMMANDS,
}


def map_response(
		command: str,
		bidi_result: Dict[str, Any],
		request_params: REQUEST_PARAMS_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps a BiDi response result back to the W3C WebDriver response format.

	Args:
		command (str): The original W3C command name.
		bidi_result (Dict[str, Any]): The result dictionary received from BiDi.
		request_params (REQUEST_PARAMS_TYPEHINT): The parameters sent with the original request.

	Returns:
		Dict[str, Any]: The formatted W3C response dictionary.

	Raises:
		CommandNotMappedToBiDiError: If the command does not have a registered response mapper.
	"""
	
	function = _MAPPED_RESPONSE_COMMANDS.get(command, None)
	
	if function is not None:
		return function(bidi_result, request_params)
	
	raise CommandNotMappedToBiDiError(command=command)
