from typing import Any, Dict, List
from abc import ABC, abstractmethod


class AbstractSchemaCDPExecutor(ABC):
	@abstractmethod
	def get_domains(self) -> List[Dict[str, Any]]:
		...
