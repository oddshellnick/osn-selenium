import inspect
from pydantic import Field
from types import ModuleType
from osn_selenium.types import DictModel
from osn_selenium.dev_tools._functions import (
	yield_package_item_way
)
from typing import (
	Any,
	Iterable,
	List,
	Optional,
	Set,
	Tuple,
	Union
)


class TargetsFilters(DictModel):
	"""
	Configuration model for filtering target types (inclusion/exclusion).

	Attributes:
		excluded (List[str]): List of target types to exclude.
		included (List[str]): List of target types to include.
		entire (bool): Default behavior if a type is not explicitly listed.
	"""
	
	excluded: List[str] = Field(default_factory=list)
	included: List[str] = Field(default_factory=list)
	
	entire: bool = False


class TargetFilter(DictModel):
	"""
	Dataclass to define a filter for discovering new browser targets.

	Used in `DevToolsSettings` to specify which types of targets (e.g., "page", "iframe")
	should be automatically attached to or excluded.

	Attributes:
		type_ (Optional[str]): The type of target to filter by (e.g., "page", "iframe").
			If None, this filter applies regardless of type. Aliased as 'type'.
		exclude (Optional[bool]): If True, targets matching `type_` will be excluded.
			If False or None, targets matching `type_` will be included.
	"""
	
	type_: Optional[str] = Field(default=None, alias="type")
	exclude: Optional[bool] = None


class TargetData(DictModel):
	"""
	Dataclass to hold essential information about a browser target.

	Attributes:
		target_id (Optional[str]): The unique identifier for the target.
		type_ (Optional[str]): The type of the target (e.g., "page", "iframe", "worker").
		title (Optional[str]): The title of the target (e.g., the page title).
		url (Optional[str]): The URL of the target.
		attached (Optional[bool]): Indicates if the DevTools session is currently attached to this target.
		can_access_opener (Optional[bool]): Whether the target can access its opener.
		opener_id (Optional[str]): The ID of the opener target.
		opener_frame_id (Optional[str]): The ID of the opener frame.
		browser_context_id (Optional[str]): The browser context ID associated with the target.
		subtype (Optional[str]): Subtype of the target.
	"""
	
	target_id: Optional[str] = None
	type_: Optional[str] = None
	title: Optional[str] = None
	url: Optional[str] = None
	attached: Optional[bool] = None
	can_access_opener: Optional[bool] = None
	opener_id: Optional[str] = None
	opener_frame_id: Optional[str] = None
	browser_context_id: Optional[str] = None
	subtype: Optional[str] = None


class FingerprintData(DictModel):
	"""
	Dataclass representing detected fingerprinting activity.

	Attributes:
		api (str): The API that was accessed.
		method (str): The specific method within the API.
		stacktrace (Optional[str]): The stack trace where the access occurred.
	"""
	
	api: str
	method: str
	stacktrace: Optional[str]


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

		EXAMPLES
		________
		>>> # Assuming self._package has structure a.b.c
		>>> pkg.get("a.b")
		... <module 'a.b'>
		>>> pkg.get(["a", "b", "c"])
		... <object c>
		"""
		
		object_ = self._package
		used_parts = [object_.__name__]
		
		for part in yield_package_item_way(name=name):
			if not hasattr(object_, part):
				raise AttributeError(f"Attribute '{part}' not found in '{'.'.join(used_parts)}'")
		
			object_ = getattr(object_, part)
			used_parts.append(part)
		
		return object_
