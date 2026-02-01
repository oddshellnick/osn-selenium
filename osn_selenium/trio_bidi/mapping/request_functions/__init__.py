from typing import Any, Dict
from osn_selenium.exceptions.bidi_bridge import (
	CommandNotMappedToBiDiError
)
from osn_selenium.trio_bidi.mapping.request_functions._cdp import (
	MAPPED_REQUEST_CDP_COMMANDS
)
from osn_selenium.trio_bidi.mapping.request_functions._file import (
	MAPPED_REQUEST_FILE_COMMANDS
)
from osn_selenium.trio_bidi.mapping.request_functions._alert import (
	MAPPED_REQUEST_ALERT_COMMANDS
)
from osn_selenium.trio_bidi.mapping.request_functions._script import (
	MAPPED_REQUEST_SCRIPT_COMMANDS
)
from osn_selenium.trio_bidi.mapping.request_functions._window import (
	MAPPED_REQUEST_WINDOW_COMMANDS
)
from osn_selenium.trio_bidi.mapping.request_functions._capture import (
	MAPPED_REQUEST_CAPTURE_COMMANDS
)
from osn_selenium.trio_bidi.mapping.request_functions._element import (
	MAPPED_REQUEST_ELEMENT_COMMANDS
)
from osn_selenium.trio_bidi.mapping.request_functions._switch_to import (
	MAPPED_REQUEST_SWITCH_TO_COMMANDS
)
from osn_selenium.trio_bidi.mapping.request_functions._navigation import (
	MAPPED_REQUEST_NAVIGATION_COMMANDS
)
from osn_selenium.trio_bidi.mapping.request_functions._web_element import (
	MAPPED_REQUEST_WEB_ELEMENT_COMMANDS
)
from osn_selenium.trio_bidi.mapping.request_functions._shadow_root import (
	MAPPED_REQUEST_SHADOW_ROOT_COMMANDS
)
from osn_selenium.trio_bidi._typehints import (
	CURRENT_BROWSING_CONTEXT_TYPEHINT,
	MAP_REQUEST_FUNCTION_TYPEHINT,
	REQUEST_PARAMS_TYPEHINT
)


__all__ = ["map_request"]

_MAPPED_REQUEST_COMMANDS: Dict[str, MAP_REQUEST_FUNCTION_TYPEHINT] = {
	**MAPPED_REQUEST_ALERT_COMMANDS,
	**MAPPED_REQUEST_CAPTURE_COMMANDS,
	**MAPPED_REQUEST_CDP_COMMANDS,
	**MAPPED_REQUEST_ELEMENT_COMMANDS,
	**MAPPED_REQUEST_FILE_COMMANDS,
	**MAPPED_REQUEST_NAVIGATION_COMMANDS,
	**MAPPED_REQUEST_SCRIPT_COMMANDS,
	**MAPPED_REQUEST_SHADOW_ROOT_COMMANDS,
	**MAPPED_REQUEST_SWITCH_TO_COMMANDS,
	**MAPPED_REQUEST_WEB_ELEMENT_COMMANDS,
	**MAPPED_REQUEST_WINDOW_COMMANDS,
}


def map_request(
		command: str,
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps a W3C WebDriver command to its corresponding BiDi protocol request.

	Args:
		command (str): The W3C command name.
		params (REQUEST_PARAMS_TYPEHINT): The parameters associated with the command.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID for the command.

	Returns:
		Dict[str, Any]: The mapped BiDi request dictionary.

	Raises:
		CommandNotMappedToBiDiError: If the command does not have a defined mapping.
	"""
	
	function = _MAPPED_REQUEST_COMMANDS.get(command, None)
	
	if function is not None:
		return function(params, context_id)
	
	raise CommandNotMappedToBiDiError(command=command)
