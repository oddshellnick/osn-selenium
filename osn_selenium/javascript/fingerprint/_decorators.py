import functools
from typing import (
	Any,
	Callable,
	ParamSpec,
	TypeVar
)
from osn_selenium.javascript.fingerprint._functions import add_code_level


__all__ = ["indent_code"]

_METHOD_INPUT = ParamSpec("_METHOD_INPUT")
_METHOD_OUTPUT = TypeVar("_METHOD_OUTPUT")
_METHOD = TypeVar("_METHOD", bound=Callable[..., Any])


def indent_code(func: _METHOD) -> _METHOD:
	"""
	Decorator that indents the result of a function which returns a string code block.

	If the result is empty, it returns an empty string. Otherwise, it adds one level
	of indentation (tab) to the result.

	Args:
		func (_METHOD): The function to wrap.

	Returns:
		_METHOD: The wrapped function.
	"""
	
	@functools.wraps(func)
	def wrapper(*args: _METHOD_INPUT.args, **kwargs: _METHOD_INPUT.kwargs) -> _METHOD_OUTPUT:
		result = func(*args, **kwargs)
		
		if not result:
			return ""
		
		return add_code_level(code=result, num=1)
	
	return wrapper
