from osn_selenium._base_models import ExtraDictModel
from typing import (
	Literal,
	Optional,
	Union
)
from osn_selenium.dev_tools.domains.fetch import FetchSettings


__all__ = ["DomainsSettings", "domains_classes_type", "domains_type"]


class DomainsSettings(ExtraDictModel):
	"""
	A dataclass container for configuration settings across different DevTools domains.

	This class provides a structured way to define the desired behavior for various
	CDP domains like Fetch, Network, etc., when the DevTools context is active.

	Attributes:
		fetch (Optional[FetchSettings]): Configuration settings for the Fetch domain. If None, the Fetch domain will not be enabled or handled. Defaults to None.
	"""
	
	fetch: Optional[FetchSettings] = None


domains_type = Literal["fetch"]
domains_classes_type = Union[FetchSettings]

DomainsSettings.model_rebuild()
