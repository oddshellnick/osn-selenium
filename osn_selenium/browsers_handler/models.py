import pathlib
from osn_selenium._base_models import DictModel


__all__ = ["Browser"]


class Browser(DictModel):
	"""
	Represents a browser installed on the system.

	This class is a TypedDict, which provides a way to define the structure of a dictionary with specific keys and value types.
	It is used to store information about a browser, such as its name, installation path, and version.

	Attributes:
		name (str): The name of the browser (e.g., "Chrome", "Firefox").
		path (pathlib.Path): The file path to the browser executable.
		version (str): The version number of the browser.
	"""
	
	name: str
	path: pathlib.Path
	version: str
