import pathlib
from types import UnionType
from osn_selenium.exceptions.path import PathValidationError
from typing import (
	Iterable,
	Optional,
	Set,
	Union,
	get_args,
	get_origin
)
from osn_selenium._typehints import (
	PATH_TYPEHINT,
	TYPES_FOR_FLATTENING_TYPEHINT
)


__all__ = ["flatten_types", "validate_path"]


def validate_path(path: Optional[PATH_TYPEHINT]) -> Optional[pathlib.Path]:
	"""
	Validates the provided path and converts it to a pathlib.Path object.

	Args:
		path (Optional[PATH_TYPEHINT]): The path to be validated and converted.

	Returns:
		Optional[pathlib.Path]: A Path object if valid, or None if the input was None.

	Raises:
		PathValidationError: If the path conversion fails due to an exception.
	"""
	
	try:
		if path is None:
			return None
	
		return pathlib.Path(path)
	except (Exception,) as exception:
		raise PathValidationError(path=path, exception=exception)


def flatten_types(
		types_: Union[TYPES_FOR_FLATTENING_TYPEHINT, Iterable[TYPES_FOR_FLATTENING_TYPEHINT]]
) -> Set[str]:
	"""
	Recursively extracts type names from a type, a union of types, or a collection of types.

	Args:
		types_ (Union[Type, Iterable[Type]]): The type definition or collection of types to flatten.

	Returns:
		Set[str]: A set of strings representing the names of the types found.
	"""
	
	types_of_level = set()
	
	if isinstance(types_, Iterable) and not isinstance(types_, str):
		for t in types_:
			types_of_level.update(flatten_types(t))
	
		return types_of_level
	
	if isinstance(types_, str):
		types_of_level.add(types_)
	
	origin = get_origin(types_)
	args = get_args(types_)
	
	is_union = origin is Union or isinstance(types_, UnionType)
	
	if is_union:
		for arg in args:
			types_of_level.update(flatten_types(arg))
	else:
		if types_ is None or types_ is type(None):
			types_of_level.add("NoneType")
		elif hasattr(types_, "__name__"):
			types_of_level.add(types_.__name__)
		else:
			types_of_level.add(str(types_))
	
	return types_of_level
