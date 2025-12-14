from abc import ABC, abstractmethod
from typing import (
	Any,
	List,
	Optional,
	Tuple
)


class AbstractAuditsCDPExecutor(ABC):
	@abstractmethod
	def check_contrast(self, report_aaa: Optional[bool] = None) -> None:
		...
	
	@abstractmethod
	def check_forms_issues(self) -> List[Any]:
		...
	
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def enable(self) -> None:
		...
	
	@abstractmethod
	def get_encoded_response(
			self,
			request_id: str,
			encoding: str,
			quality: Optional[float] = None,
			size_only: Optional[bool] = None
	) -> Tuple[Optional[str], int, int]:
		...
