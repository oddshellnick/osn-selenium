from osn_selenium._functions import validate_path
from osn_selenium._typehints import PATH_TYPEHINT
from osn_selenium.flags.models.values import ArgumentValue


__all__ = ["argument_to_flag", "build_first_start_argument"]


def build_first_start_argument(browser_exe: PATH_TYPEHINT) -> str:
	"""
	Builds the first command line argument to start a browser executable.

	This function constructs the initial command line argument needed to execute a browser,
	handling different operating systems and executable path formats.

	Args:
		browser_exe (PATH_TYPEHINT): Path to the browser executable or just the executable name.

	Returns:
		str: The constructed command line argument string.

	Raises:
		TypeError: If `browser_exe` is not of type str or Path.
	"""
	
	path = validate_path(path=browser_exe).resolve()
	
	return f"\"{str(path)}\""


def argument_to_flag(argument: ArgumentValue) -> str:
	"""
	Format a command-line argument.

	Args:
		argument (ArgumentValue): Argument to format.

	Returns:
		str: Formatted argument.
	"""
	
	if "{value}" in argument.command_line:
		return argument.command_line.format(value=argument.value)
	
	return argument.command_line
