from typing import Any, Dict, List
from abc import ABC, abstractmethod


__all__ = ["AbstractBlinkCastingMixin"]


class AbstractBlinkCastingMixin(ABC):
	"""
	Abstract mixin defining the interface for casting/mirroring functionality
	in Blink-based browsers.

	Provides methods to discover sinks (receivers) and control tab or desktop mirroring sessions.
	"""
	
	@abstractmethod
	def get_sinks(self) -> List[Dict[str, Any]]:
		"""
		Retrieves a list of available casting sinks (receivers).

		Returns:
			List[Dict[str, Any]]: A list of dictionaries, where each dictionary represents
			a discovered sink and its properties.
		"""
		
		...
	
	@abstractmethod
	def set_sink_to_use(self, sink_name: str) -> Dict[str, Any]:
		"""
		Selects a specific sink to be used for future casting operations.

		Args:
			sink_name (str): The name of the sink to select.

		Returns:
			Dict[str, Any]: A dictionary containing the command response or status.
		"""
		
		...
	
	@abstractmethod
	def start_desktop_mirroring(self, sink_name: str) -> Dict[str, Any]:
		"""
		Starts mirroring the entire desktop to the specified sink.

		Args:
			sink_name (str): The name of the sink to cast the desktop to.

		Returns:
			Dict[str, Any]: A dictionary containing the command response or status.
		"""
		
		...
	
	@abstractmethod
	def start_tab_mirroring(self, sink_name: str) -> Dict[str, Any]:
		"""
		Starts mirroring the current browser tab to the specified sink.

		Args:
			sink_name (str): The name of the sink to cast the tab to.

		Returns:
			Dict[str, Any]: A dictionary containing the command response or status.
		"""
		
		...
	
	@abstractmethod
	def stop_casting(self, sink_name: str) -> Dict[str, Any]:
		"""
		Stops the active casting session on the specified sink.

		Args:
			sink_name (str): The name of the sink (receiver) to stop casting to.

		Returns:
			Dict[str, Any]: A dictionary containing the command response or status.
		"""
		
		...
