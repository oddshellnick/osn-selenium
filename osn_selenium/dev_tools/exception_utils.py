import json
import logging
import traceback
from typing import (
	Any,
	Dict,
	List,
	Optional
)


def extract_exception_trace(exception: BaseException) -> str:
	"""
	Extracts a comprehensive traceback string for an exception, including handling for `ExceptionGroup`s.

	This function recursively flattens `ExceptionGroup`s to ensure all nested exceptions
	have their tracebacks included in the final output string.

	Args:
		exception (BaseException): The exception object to extract the trace from.

	Returns:
		str: A multi-line string containing the formatted traceback(s) for the given exception
			 and any nested exceptions within an `ExceptionGroup`.

	EXAMPLES
	________
	>>> try:
	...	 raise ValueError("Simple error occurred")
	... except ValueError as e:
	...	 trace = extract_exception_trace(e)
	...	 # The first line typically indicates the start of a traceback
	...	 print(trace.splitlines()[0].strip())
	>>> try:
	...	 raise ExceptionGroup(
	...		 "Multiple issues",
	...		 [
	...			 TypeError("Invalid type provided"),
	...			 ValueError("Value out of range")
	...		 ]
	...	 )
	... except ExceptionGroup as eg:
	...	 trace = extract_exception_trace(eg)
	...	 # Check if tracebacks for both nested exceptions are present
	...	 print("TypeError" in trace and "ValueError" in trace)
	"""
	
	def format_exception(exception_: BaseException) -> str:
		"""
		Formats a single exception's traceback into a string.

		Args:
			exception_ (BaseException): The exception to format.

		Returns:
			str: The formatted exception string.
		"""
		
		return "".join(
				traceback.format_exception(exception_.__class__, exception_, exception_.__traceback__)
		)
	
	def flatten_exceptions(exception_: BaseException) -> List[BaseException]:
		"""
		Recursively flattens an ExceptionGroup into a List of individual exceptions.

		Args:
			exception_ (BaseException): The exception to flatten.

		Returns:
			List[BaseException]: A list of flattened exceptions.
		"""
		
		if isinstance(exception_, ExceptionGroup):
			inner_exceptions = exception_.exceptions
		else:
			return [exception_]
		
		result = []
		
		for exception__ in inner_exceptions:
			result.extend(flatten_exceptions(exception__))
		
		return result
	
	return "\n".join(format_exception(exc) for exc in flatten_exceptions(exception))


def log_exception(exception: BaseException, extra_data: Optional[Dict[str, Any]] = None):
	"""
	Logs the full traceback of an exception at the ERROR level.

	This function uses `extract_exception_trace` to get a comprehensive traceback string
	and then logs it using the standard logging module.

	Args:
		exception (BaseException): The exception object to log.
		extra_data (Optional[Dict[str, Any]]): Additional data to log with the exception.
	"""
	
	if extra_data is None:
		exception_data = extract_exception_trace(exception)
	else:
		trace = extract_exception_trace(exception)
		max_len = max(len(line) for line in trace.splitlines())
	
		exception_data = "{bound}\n{exception}\nWith extra data:\n{extra_data}\n{bound}".format(
				bound="=" * max_len,
				exception=trace,
				extra_data=json.dumps(extra_data, indent=4, ensure_ascii=False)
		)
	
	logging.log(logging.ERROR, exception_data)


class ExceptionThrown:
	"""
	A wrapper class to indicate that an exception was thrown during an operation.

	This is used in `execute_cdp_command` when `error_mode` is "log" or "pass"
	to return an object indicating an error occurred without re-raising it immediately.

	Attributes:
		exception (BaseException): The exception that was caught.
		traceback (str): The formatted traceback string of the exception.
	"""
	
	def __init__(self, exception: BaseException):
		"""
		Initializes the ExceptionThrown wrapper.

		Args:
			exception (BaseException): The exception to wrap.
		"""
		
		self.exception = exception
		self.traceback = extract_exception_trace(exception)
