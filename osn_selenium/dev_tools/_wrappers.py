import inspect
from types import ModuleType
from typing import (
	Any,
	Generator,
	Iterable,
	Union
)


__all__ = ["DevToolsPackage"]


def _yield_package_item_way(name: Union[str, Iterable[str]]) -> Generator[str, Any, None]:
	"""
	Yields parts of a package path from a string or iterable of strings.

	Args:
		name (Union[str, Iterable[str]]): The name or path components to yield.

	Returns:
		Generator[str, Any, None]: A generator yielding each part of the path.

	Raises:
		TypeError: If `name` is not a string or an iterable of strings.
	"""
	
	if (
			not isinstance(name, str) and (
					not isinstance(name, Iterable) or not all(isinstance(item, str) for item in name)
			)
	):
		raise TypeError(
				f"Wrong name type ({type(name).__name__})! Must be str or Iterable[str]!"
		)
	
	way = name if isinstance(name, Iterable) and not isinstance(name, str) else [name]
	
	for item in way:
		for part in item.split("."):
			yield part


class DevToolsPackage:
	"""
	Wrapper around the DevTools module to safely retrieve nested attributes/classes.

	Attributes:
		_package (ModuleType): The root DevTools module package.
	"""
	
	def __init__(self, package: ModuleType):
		"""
		Initializes the DevToolsPackage wrapper.

		Args:
			package (ModuleType): The root module to wrap.

		Raises:
			TypeError: If the provided package is not a module.
		"""
		
		if not inspect.ismodule(package):
			raise TypeError(f"Expected a module, got {type(package).__name__}.")
		
		self._package = package
	
	def get(self, name: Union[str, Iterable[str]]) -> Any:
		"""
		Retrieves a nested attribute or class from the package by dot-separated path.

		Args:
			name (Union[str, Iterable[str]]): The dot-separated path string or iterable of strings
				representing the path to the desired object.

		Returns:
			Any: The retrieved object (module, class, or function).

		Raises:
			AttributeError: If any part of the path is not found in the package structure.
		"""
		
		object_ = self._package
		used_parts = [object_.__name__]
		
		for part in _yield_package_item_way(name=name):
			if not hasattr(object_, part):
				package_str = ".".join(used_parts)
				raise AttributeError(f"Attribute '{part}' not found in '{package_str}'")
		
			object_ = getattr(object_, part)
			used_parts.append(part)
		
		return object_
