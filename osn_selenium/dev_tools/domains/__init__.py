from dataclasses import dataclass
from typing import (
	Literal,
	Optional,
	TypedDict,
	Union
)
from osn_selenium.dev_tools.domains.fetch import (
	FetchSettings,
	_Fetch
)


class Domains(TypedDict, total=False):
	"""
	Settings for configuring callbacks for different DevTools event domains.

	This TypedDict aggregates settings for various DevTools event types, allowing for structured configuration
	of event handling within the DevTools integration. Currently, it specifically includes settings for the 'fetch' domain.

	Attributes:
		fetch (_Fetch): Configuration settings for the Fetch domain events.
			This includes settings to enable/disable fetch event handling and specific configurations for 'requestPaused' events.
	"""
	
	fetch: _Fetch


@dataclass
class DomainsSettings:
	"""
	A dataclass container for configuration settings across different DevTools domains.

	This class provides a structured way to define the desired behavior for various
	CDP domains like Fetch, Network, etc., when the DevTools context is active.

	Attributes:
		fetch (Optional[FetchSettings]): Configuration settings for the Fetch domain. If None, the Fetch domain will not be enabled or handled. Defaults to None.
	"""
	
	fetch: Optional[FetchSettings] = None
	
	def to_dict(self) -> Domains:
		"""
		Converts the dataclass instance to its dictionary representation.

		This method is used internally to transform the structured settings from the
		dataclass into the `Domains` TypedDict format expected by the DevTools manager.

		Returns:
			Domains: A dictionary containing the settings for each configured domain.
		"""
		
		kwargs = {}
		
		if self.fetch is not None:
			kwargs["fetch"] = self.fetch.to_dict()
		
		return Domains(**kwargs)


domains_type = Literal["fetch"]
domains_classes_type = Union[_Fetch]
