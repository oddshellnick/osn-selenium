from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Union


__all__ = ["AbstractUtilsMixin"]

if TYPE_CHECKING:
	from osn_selenium.abstract.instances.action_chains import AbstractActionChains


class AbstractUtilsMixin(ABC):
	"""
	Mixin class providing utility methods for action chains.
	"""
	
	@abstractmethod
	def pause(self, seconds: Union[float, int]) -> "AbstractActionChains":
		"""
		Pauses the execution for a specified duration.

		Args:
			seconds (Union[float, int]): The duration to pause in seconds.

		Returns:
			AbstractActionChains: The instance of ActionChains for method chaining.
		"""
		
		...
	
	@abstractmethod
	def perform(self) -> None:
		"""
		Performs all stored actions.
		"""
		
		...
	
	@abstractmethod
	def reset_actions(self) -> None:
		"""
		Clears all actions that are already stored locally and on the remote end.
		"""
		
		...
