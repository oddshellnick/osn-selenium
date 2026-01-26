import importlib
from typing import TYPE_CHECKING, Any, Dict, Callable

import trio

from osn_selenium.abstract.executors.cdp import AbstractCDPExecutor
from osn_selenium.exceptions.dependencies import CDPPackageError


__all__ = ["CDPExecutor"]

if TYPE_CHECKING:
	from osn_selenium_cdp_v140.executors.trio_threads import CDP140Executor
	from osn_selenium_cdp_v141.executors.trio_threads import CDP141Executor
	from osn_selenium_cdp_v142.executors.trio_threads import CDP142Executor
	from osn_selenium_cdp_v143.executors.trio_threads import CDP143Executor
	from osn_selenium_cdp_v144.executors.trio_threads import CDP144Executor


class CDPExecutor(AbstractCDPExecutor):
	"""
	Global CDP executor router. 
	Handles lazy loading and version-specific package validation.
	"""

	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any], lock: trio.Lock, limiter: trio.CapacityLimiter):
		self._execute_function = execute_function
		self._lock = lock
		self._limiter = limiter
		self._v140 = None
		self._v141 = None
		self._v142 = None
		self._v143 = None
		self._v144 = None

	def get(self, version: int) -> Any:
		"""
		Dynamically loads and returns the CDP executor for a specific version.

		Args:
			version (int): The CDP version number.

		Returns:
			Any: The version-specific executor instance.

		Raises:
			CDPPackageError: If the version-specific package is not installed.
		"""
	
		try:
			if getattr(self, f"_v{version}", None) is None:
				module = importlib.import_module(f"osn_selenium_cdp_v{version}.executors.trio_threads")
				executor_type = getattr(module, f"CDP{version}Executor")

				setattr(self, f"_v{version}", executor_type(execute_function=self._execute_function, lock=self._lock, limiter=self._limiter))

			return getattr(self, f"_v{version}", None)
		except ImportError:
			raise CDPPackageError(version=version)

	@property
	def v140(self) -> "CDP140Executor":
		"""
		Get or initialize the executor for CDP version 140.
		Raises CDPPackageError if the version-specific package is not installed.
		"""

		return self.get(version=140)

	@property
	def v141(self) -> "CDP141Executor":
		"""
		Get or initialize the executor for CDP version 141.
		Raises CDPPackageError if the version-specific package is not installed.
		"""

		return self.get(version=141)

	@property
	def v142(self) -> "CDP142Executor":
		"""
		Get or initialize the executor for CDP version 142.
		Raises CDPPackageError if the version-specific package is not installed.
		"""

		return self.get(version=142)

	@property
	def v143(self) -> "CDP143Executor":
		"""
		Get or initialize the executor for CDP version 143.
		Raises CDPPackageError if the version-specific package is not installed.
		"""

		return self.get(version=143)

	@property
	def v144(self) -> "CDP144Executor":
		"""
		Get or initialize the executor for CDP version 144.
		Raises CDPPackageError if the version-specific package is not installed.
		"""

		return self.get(version=144)
