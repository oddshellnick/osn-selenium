from abc import ABC, abstractmethod
from typing import (
	Iterable,
	List,
	Optional
)
from osn_selenium._typehints import DEVICES_TYPEHINT
from osn_selenium.abstract.instances.action_chains import AbstractActionChains
from osn_selenium.abstract.instances.web_driver_wait import (
	AbstractWebDriverWait
)


__all__ = ["AbstractCoreActionsMixin"]


class AbstractCoreActionsMixin(ABC):
	"""Mixin responsible for user actions chains."""
	
	@abstractmethod
	def action_chains(
			self,
			duration: int = 250,
			devices: Optional[List[DEVICES_TYPEHINT]] = None
	) -> AbstractActionChains:
		"""
		Creates a new ActionChains instance for building complex user interactions.

		Args:
			duration (int): The default duration for pointer actions in milliseconds.
			devices (Optional[List[DEVICES_TYPEHINT]]): A list of input devices to use.

		Returns:
			AbstractActionChains: A new ActionChains instance.
		"""
		
		...
	
	@abstractmethod
	def web_driver_wait(
			self,
			timeout: float,
			poll_frequency: float = 0.5,
			ignored_exceptions: Optional[Iterable[BaseException]] = None,
	) -> AbstractWebDriverWait:
		"""
		Creates a new WebDriverWait instance.

		Args:
			timeout (float): How long to wait for the condition to be true.
			poll_frequency (float): How often to check the condition. Defaults to 0.5.
			ignored_exceptions (Optional[Iterable[BaseException]]): Exceptions to ignore while waiting.

		Returns:
			AbstractWebDriverWait: A new WebDriverWait instance.
		"""
		
		...
