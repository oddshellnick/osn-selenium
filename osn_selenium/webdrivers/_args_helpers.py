import math
import trio
from osn_selenium.instances.protocols import AnyInstanceWrapper
from typing import (
	Any,
	Callable,
	Dict,
	Optional,
	Union
)
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
from osn_selenium.instances.trio_bidi.web_element import (
	WebElement as TrioBiDiWebElement
)
from osn_selenium.instances.trio_threads.web_element import (
	WebElement as TrioThreadWebElement
)
from osn_selenium.webdrivers.protocols import (
	SyncWebDriver,
	TrioBiDiWebDriver,
	TrioThreadWebDriver
)
from osn_selenium.instances.convert import (
	get_sync_instance_wrapper,
	get_trio_bidi_instance_wrapper,
	get_trio_thread_instance_wrapper
)


__all__ = [
	"build_cdp_kwargs",
	"get_wrap_args_function",
	"unwrap_args",
	"wrap_sync_args",
	"wrap_trio_bidi_args",
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


def wrap_trio_bidi_args(
		args: Any,
		lock: trio.Lock,
		limiter: trio.CapacityLimiter,
		trio_token: Optional[trio.lowlevel.TrioToken] = None,
		bidi_buffer_size: Union[int, float] = math.inf,
) -> Any:
	"""
	Recursively wraps Selenium WebElements into TrioBiDiWebElement instances.

	Args:
		args (Any): Data structure containing potential Selenium WebElements.
		lock (trio.Lock): Trio lock for synchronization.
		limiter (trio.CapacityLimiter): Trio capacity limiter.
		trio_token (Optional[trio.lowlevel.TrioToken]): The Trio token for the current event loop.
		bidi_buffer_size (Union[int, float]): Buffer size for the BiDi task channel.

	Returns:
		Any: Data structure with wrapped elements.
	"""
	
	if isinstance(args, list):
		return [
			wrap_trio_bidi_args(
					arg,
					lock=lock,
					limiter=limiter,
					trio_token=trio_token,
					bidi_buffer_size=bidi_buffer_size,
			) for arg in args
		]
	
	if isinstance(args, set):
		return {
			wrap_trio_bidi_args(
					arg,
					lock=lock,
					limiter=limiter,
					trio_token=trio_token,
					bidi_buffer_size=bidi_buffer_size,
			) for arg in args
		}
	
	if isinstance(args, tuple):
		return (
				wrap_trio_bidi_args(
						arg,
						lock=lock,
						limiter=limiter,
						trio_token=trio_token,
						bidi_buffer_size=bidi_buffer_size,
				) for arg in args
		)
	
	if isinstance(args, dict):
		return {
			wrap_trio_bidi_args(
					key,
					lock=lock,
					limiter=limiter,
					trio_token=trio_token,
					bidi_buffer_size=bidi_buffer_size,
			): wrap_trio_bidi_args(
					value,
					lock=lock,
					limiter=limiter,
					trio_token=trio_token,
					bidi_buffer_size=bidi_buffer_size,
			)
			for key, value in args.items()
		}
	
	if isinstance(args, SeleniumWebElement):
		return get_trio_bidi_instance_wrapper(
				wrapper_class=TrioBiDiWebElement,
				legacy_object=args,
				lock=lock,
				limiter=limiter,
				trio_token=trio_token,
				bidi_buffer_size=bidi_buffer_size,
		)
	
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
	
	if isinstance(driver, TrioBiDiWebDriver) and driver.architecture == "trio_bidi":
		def wrapper(args: Any) -> Any:
			return wrap_trio_bidi_args(
					args,
					lock=driver.lock,
					limiter=driver.capacity_limiter,
					trio_token=driver.trio_token,
					bidi_buffer_size=driver.trio_bidi_buffer_size,
			)
	
		return wrapper
	
	raise ProtocolComplianceError(
			instance=driver,
			expected_protocols=(SyncWebDriver, TrioThreadWebDriver, TrioBiDiWebDriver)
	)


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
