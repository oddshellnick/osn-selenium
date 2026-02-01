from typing import Any, Dict
from selenium.webdriver.remote.command import Command
from osn_selenium.trio_bidi._internal_mappings import UPLOAD_INTERNAL_FILE
from osn_selenium.trio_bidi._typehints import (
	CURRENT_BROWSING_CONTEXT_TYPEHINT,
	MAP_REQUEST_FUNCTION_TYPEHINT,
	REQUEST_PARAMS_TYPEHINT
)


__all__ = ["MAPPED_REQUEST_FILE_COMMANDS"]


def _map_upload_file_request(
		params: REQUEST_PARAMS_TYPEHINT,
		context_id: CURRENT_BROWSING_CONTEXT_TYPEHINT
) -> Dict[str, Any]:
	"""
	Maps the file upload command to an internal bridge command.

	Args:
		params (REQUEST_PARAMS_TYPEHINT): Request parameters.
		context_id (CURRENT_BROWSING_CONTEXT_TYPEHINT): The browsing context ID.

	Returns:
		Dict[str, Any]: The internal BiDi request.
	"""
	
	return {"method": UPLOAD_INTERNAL_FILE, "params": {}}


MAPPED_REQUEST_FILE_COMMANDS: Dict[str, MAP_REQUEST_FUNCTION_TYPEHINT] = {Command.UPLOAD_FILE: _map_upload_file_request}
