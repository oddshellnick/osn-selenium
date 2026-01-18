import functools
from typing import (
	Callable,
	ParamSpec,
	TypeVar
)
from osn_selenium.javascript.fingerprint.functions import add_code_level


METHOD_INPUT = ParamSpec("METHOD_INPUT")
METHOD_OUTPUT = TypeVar("METHOD_OUTPUT")


def indent_code(func: Callable[METHOD_INPUT, METHOD_OUTPUT]) -> Callable[METHOD_INPUT, METHOD_OUTPUT]:
	"""
	Decorator that indents the result of a function which returns a string code block.

	If the result is empty, it returns an empty string. Otherwise, it adds one level
	of indentation (tab) to the result.

	Args:
		func (Callable): The function to wrap.

	Returns:
		Callable: The wrapped function.
	"""
	
	@functools.wraps(func)
	def wrapper(*args: METHOD_INPUT.args, **kwargs: METHOD_INPUT.kwargs) -> METHOD_OUTPUT:
		result = func(*args, **kwargs)
		
		if not result:
			return ""
		
		return add_code_level(code=result, num=1)
	
	return wrapper
