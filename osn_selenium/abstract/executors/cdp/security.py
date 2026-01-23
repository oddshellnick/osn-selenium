from abc import ABC, abstractmethod


__all__ = ["AbstractSecurityCDPExecutor"]


class AbstractSecurityCDPExecutor(ABC):
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def enable(self) -> None:
		...
	
	@abstractmethod
	def handle_certificate_error(self, event_id: int, action: str) -> None:
		...
	
	@abstractmethod
	def set_ignore_certificate_errors(self, ignore: bool) -> None:
		...
	
	@abstractmethod
	def set_override_certificate_errors(self, override: bool) -> None:
		...
