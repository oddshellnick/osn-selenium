from typing import Any, List
from abc import ABC, abstractmethod


class AbstractSchemaCDPExecutor(ABC):
	@abstractmethod
	def get_domains(self) -> List[Any]:
		...
