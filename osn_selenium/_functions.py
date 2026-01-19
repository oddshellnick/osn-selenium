import types
from typing import Any, get_args, get_origin, Set, Union


def flatten_types(types_: Any) -> Set[str]:
    """
    Recursively extracts type names from a type, a union of types, or a collection of types.

    Args:
        types_ (Union[Any, Iterable[Any]]): The type definition or collection of types to flatten.

    Returns:
        Set[str]: A set of strings representing the names of the types found.
    """

    types_of_level = set()

    if isinstance(types_, (list, tuple, set)):
        for t in types_:
            types_of_level.update(flatten_types(t))

        return types_of_level

    origin = get_origin(types_)
    args = get_args(types_)

    is_union = origin is Union or (hasattr(types, "UnionType") and isinstance(types_, types.UnionType))

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
