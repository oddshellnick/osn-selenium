from typing import Any, TYPE_CHECKING
from osn_selenium.webdrivers.BaseDriver._utils import trio_async_wrap


if TYPE_CHECKING:
	from osn_selenium.webdrivers.BaseDriver.webdriver import BrowserWebDriver


class TrioBrowserWebDriverWrapper:
	"""
	Wraps BrowserWebDriver methods for asynchronous execution using Trio.

	This class acts as a proxy to a `BrowserWebDriver` instance. It intercepts
	method calls and executes them in a separate thread using `trio.to_thread.run_sync`,
	allowing synchronous WebDriver operations to be called from asynchronous Trio code
	without blocking the event loop. Properties and non-callable attributes are accessed directly.

	Attributes:
		_webdriver (BrowserWebDriver): The underlying synchronous BrowserWebDriver instance.
		_excluding_functions (list[str]): A list of attribute names on the wrapped object
											  that should *not* be accessible through this wrapper,
											  typically because they are irrelevant or dangerous
											  in an async context handled by the wrapper.
	"""
	
	def __init__(self, _webdriver: "BrowserWebDriver"):
		"""
		Initializes the TrioBrowserWebDriverWrapper.

		Args:
			_webdriver (BrowserWebDriver): The BrowserWebDriver instance to wrap.
		"""
		
		self._webdriver = _webdriver
		
		self._excluding_functions = ["to_wrapper", "execute_async_js_script"]
	
	def __getattr__(self, name) -> Any:
		"""
		Intercepts attribute access to wrap callable methods for asynchronous execution.

		When an attribute (method or property) is accessed on this wrapper:
		1. Checks if the attribute name is in the `_excluding_functions` list. If so, raises AttributeError.
		2. Retrieves the attribute from the underlying `_webdriver` object.
		3. If the attribute is callable (i.e., a method), it returns a new asynchronous
		   function (`wrapped`). When this `wrapped` function is called (`await wrapper.some_method()`),
		   it executes the original synchronous method (`attr`) in a separate thread managed by Trio,
		   using `trio.to_thread.run_sync` and applying the capacity limiter from the wrapped object.
		4. If the attribute is not callable (e.g., a property), it returns the attribute's value directly.

		Args:
			name (str): The name of the attribute being accessed.

		Returns:
			Any: Either an asynchronous wrapper function (awaitable) for a method, or the direct value
				 of a property or non-callable attribute from the underlying `_webdriver` instance.

		Raises:
			AttributeError: If the attribute `name` is listed in `_excluding_functions` or
							if it does not exist on the underlying `_webdriver` object.
		"""
		
		if name in self._excluding_functions:
			raise AttributeError(f"Don't use {name} method in TrioBrowserWebDriverWrapper!")
		else:
			attr = getattr(self._webdriver, name)
		
			if callable(attr):
				return trio_async_wrap(attr, self._webdriver.trio_capacity_limiter)
		
			return attr
