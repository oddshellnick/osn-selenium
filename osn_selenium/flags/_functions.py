from pathlib import Path
from typing import Union
from osn_selenium.flags.models.values import ArgumentValue


def build_first_start_argument(browser_exe: Union[str, Path]) -> str:
	"""
	Builds the first command line argument to start a browser executable.

	This function constructs the initial command line argument needed to execute a browser,
	handling different operating systems and executable path formats.

	Args:
		browser_exe (Union[str, Path]): Path to the browser executable or just the executable name.

	Returns:
		str: The constructed command line argument string.

	Raises:
		TypeError: If `browser_exe` is not of type str or Path.
	"""
	
	if isinstance(browser_exe, str):
		return browser_exe
	
	if isinstance(browser_exe, Path):
		return f"\"{str(browser_exe.resolve())}\""
	
	raise TypeError(f"browser_exe must be str or Path, not {type(browser_exe).__name__}.")


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
