from typing import Any, Dict
from abc import ABC, abstractmethod


__all__ = ["AbstractBlinkNetworkMixin"]


class AbstractBlinkNetworkMixin(ABC):
	"""
	Abstract mixin defining the interface for network emulation and condition management.

	Provides methods to simulate network conditions such as latency, throughput, and
	offline status in a Blink-based browser.
	"""
	
	@abstractmethod
	def delete_network_conditions(self) -> None:
		"""
		Resets the network conditions to the default state (no emulation/throttling).
		"""
		
		...
	
	@abstractmethod
	def get_network_conditions(self) -> Dict[str, Any]:
		"""
		Retrieves the currently active network emulation conditions.

		Returns:
			Dict[str, Any]: A dictionary containing the current network settings.
		"""
		
		...
	
	@abstractmethod
	def set_network_conditions(self, **network_conditions: Dict[str, Any]) -> None:
		"""
		Sets the network emulation conditions.

		Args:
			**network_conditions (Dict[str, Any]): Key-value pairs defining the network conditions
				(e.g., offline status, latency, download_throughput, upload_throughput).
		"""
		
		...
