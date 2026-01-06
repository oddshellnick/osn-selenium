from typing import List, Optional
from abc import ABC, abstractmethod
from osn_selenium.types import DEVICES_TYPEHINT
from osn_selenium.abstract.instances.action_chains import (
	AbstractActionChains,
	AbstractHumanLikeActionChains
)


class AbstractActionsMixin(ABC):
	"""Mixin responsible for user actions chains."""
	
	@abstractmethod
	def action_chain(
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
	def hm_action_chain(
			self,
			duration: int = 250,
			devices: Optional[List[DEVICES_TYPEHINT]] = None,
	) -> AbstractHumanLikeActionChains:
		"""
		Creates a new HumanLikeActionChains instance for building complex user interactions.

		Args:
			duration (int): The default duration for pointer actions in milliseconds.
			devices (Optional[List[DEVICES_TYPEHINT]]): A list of input devices to use.

		Returns:
			AbstractHumanLikeActionChains: A new HumanLikeActionChains instance.
		"""
		
		...
