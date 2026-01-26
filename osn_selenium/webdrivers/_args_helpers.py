import trio
from typing import Any, Callable, Dict
from osn_selenium.instances.protocols import AnyInstanceWrapper
from osn_selenium.exceptions.protocol import (
	ProtocolComplianceError
)
from osn_selenium.webdrivers._typehints import (
	ANY_WEBDRIVER_PROTOCOL_TYPEHINT
)
from osn_selenium.instances.sync.web_element import (
	WebElement as SyncWebElement
)
from selenium.webdriver.remote.webelement import (
	WebElement as SeleniumWebElement
)
from osn_selenium.webdrivers.protocols import (
	SyncWebDriver,
	TrioThreadWebDriver
)
from osn_selenium.instances.trio_threads.web_element import (
	WebElement as TrioThreadWebElement
)
from osn_selenium.instances.convert import (
	get_sync_instance_wrapper,
	get_trio_thread_instance_wrapper
)


__all__ = [
	"build_cdp_kwargs",
	"get_wrap_args_function",
	"unwrap_args",
	"wrap_sync_args",
	"wrap_trio_thread_args"
]


def unwrap_args(args: Any) -> Any:
	"""
	Recursively unwraps objects by extracting the legacy Selenium object from wrappers.

	Args:
		args (Any): Data structure containing potential instance wrappers.

	Returns:
		Any: Data structure with raw Selenium objects.
	"""
	
	if isinstance(args, list):
		return [unwrap_args(arg) for arg in args]
	
	if isinstance(args, set):
		return {unwrap_args(arg) for arg in args}
	
	if isinstance(args, tuple):
		return (unwrap_args(arg) for arg in args)
	
	if isinstance(args, dict):
		return {unwrap_args(key): unwrap_args(value) for key, value in args.items()}
	
	if isinstance(args, AnyInstanceWrapper):
		return args.legacy
	
	return args


def wrap_trio_thread_args(args: Any, lock: trio.Lock, limiter: trio.CapacityLimiter) -> Any:
	"""
	Recursively wraps Selenium WebElements into TrioThreadWebElement instances.

	Args:
		args (Any): Data structure containing potential Selenium WebElements.
		lock (trio.Lock): Trio lock for synchronization.
		limiter (trio.CapacityLimiter): Trio capacity limiter.

	Returns:
		Any: Data structure with wrapped elements.
	"""
	
	if isinstance(args, list):
		return [wrap_trio_thread_args(arg, lock=lock, limiter=limiter) for arg in args]
	
	if isinstance(args, set):
		return {wrap_trio_thread_args(arg, lock=lock, limiter=limiter) for arg in args}
	
	if isinstance(args, tuple):
		return (wrap_trio_thread_args(arg, lock=lock, limiter=limiter) for arg in args)
	
	if isinstance(args, dict):
		return {
			wrap_trio_thread_args(key, lock=lock, limiter=limiter): wrap_trio_thread_args(value, lock=lock, limiter=limiter)
			for key, value in args.items()
		}
	
	if isinstance(args, SeleniumWebElement):
		return get_trio_thread_instance_wrapper(
				wrapper_class=TrioThreadWebElement,
				legacy_object=args,
				lock=lock,
				limiter=limiter,
		)
	
	return args


def wrap_sync_args(args: Any) -> Any:
	"""
	Recursively wraps Selenium WebElements into SyncWebElement instances.

	Args:
		args (Any): Data structure containing potential Selenium WebElements.

	Returns:
		Any: Data structure with wrapped elements.
	"""
	
	if isinstance(args, list):
		return [wrap_sync_args(arg) for arg in args]
	
	if isinstance(args, set):
		return {wrap_sync_args(arg) for arg in args}
	
	if isinstance(args, tuple):
		return (wrap_sync_args(arg) for arg in args)
	
	if isinstance(args, dict):
		return {wrap_sync_args(key): wrap_sync_args(value) for key, value in args.items()}
	
	if isinstance(args, SeleniumWebElement):
		return get_sync_instance_wrapper(wrapper_class=SyncWebElement, legacy_object=args)
	
	return args


def get_wrap_args_function(driver: ANY_WEBDRIVER_PROTOCOL_TYPEHINT) -> Callable[[Any], Any]:
	"""
	Determines the appropriate argument wrapping function based on the driver's architecture.

	Args:
		driver (ANY_WEBDRIVER_PROTOCOL): The driver instance.

	Returns:
		Callable[[Any], Any]: A function to wrap elements.

	Raises:
		ExpectedTypeError: If the driver instance type is not supported.
	"""
	
	if isinstance(driver, SyncWebDriver) and driver.architecture == "sync":
		def wrapper(args: Any) -> Any:
			return wrap_sync_args(args)
	
		return wrapper
	
	if isinstance(driver, TrioThreadWebDriver) and driver.architecture == "trio_threads":
		def wrapper(args: Any) -> Any:
			return wrap_trio_thread_args(args, lock=driver.lock, limiter=driver.capacity_limiter)
	
		return wrapper
	
	raise ProtocolComplianceError(instance=driver, expected_protocols=(SyncWebDriver, TrioThreadWebDriver))


def build_cdp_kwargs(**kwargs: Any) -> Dict[str, Any]:
	"""
	Builds a dictionary of keyword arguments for a CDP command, excluding None values.

	Args:
		**kwargs (Any): Keyword arguments to filter.

	Returns:
		Dict[str, Any]: A dictionary containing only the non-None keyword arguments.
	"""
	
	dict_ = {}
	
	for key, value in kwargs.items():
		if value is not None:
			dict_[key] = value
	
	return dict_
