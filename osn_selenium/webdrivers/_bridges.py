from typing import Any, Callable, Dict
from osn_selenium.webdrivers._typehints import (
	ANY_WEBDRIVER_PROTOCOL_TYPEHINT
)
from osn_selenium.webdrivers._args_helpers import (
	get_wrap_args_function,
	unwrap_args
)


__all__ = ["get_cdp_executor_bridge", "get_js_executor_bridge"]


def get_js_executor_bridge(driver: ANY_WEBDRIVER_PROTOCOL_TYPEHINT) -> Callable[[str, Any], Any]:
	"""
	Creates a bridge function for executing JavaScript in the browser.

	Args:
		driver (ANY_WEBDRIVER_PROTOCOL): The driver instance.

	Returns:
		Callable[[str, Any], Any]: A wrapper for execute_script.
	"""
	
	def wrapper(script: str, *args: Any) -> Any:
		args = unwrap_args(args)
		
		result = driver.driver.execute_script(script, *args)
		
		return wrapper_function(result)
	
	wrapper_function = get_wrap_args_function(driver=driver)
	
	return wrapper


def get_cdp_executor_bridge(driver: ANY_WEBDRIVER_PROTOCOL_TYPEHINT) -> Callable[[str, Dict[str, Any]], Any]:
	"""
	Creates a bridge function for executing CDP commands in the browser.

	Args:
		driver (ANY_WEBDRIVER_PROTOCOL): The driver instance.

	Returns:
		Callable[[str, Dict[str, Any]], Any]: A wrapper for execute_cdp_cmd.
	"""
	
	def wrapper(cmd: str, cmd_args: Dict[str, Any]) -> Any:
		cmd_args = unwrap_args(cmd_args)
		
		result = driver.driver.execute_cdp_cmd(cmd, cmd_args)
		
		return wrapper_function(result)
	
	wrapper_function = get_wrap_args_function(driver=driver)
	
	return wrapper
