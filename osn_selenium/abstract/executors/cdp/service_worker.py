from abc import ABC, abstractmethod


__all__ = ["AbstractServiceWorkerCDPExecutor"]


class AbstractServiceWorkerCDPExecutor(ABC):
	@abstractmethod
	def deliver_push_message(self, origin: str, registration_id: str, data: str) -> None:
		...
	
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def dispatch_periodic_sync_event(self, origin: str, registration_id: str, tag: str) -> None:
		...
	
	@abstractmethod
	def dispatch_sync_event(self, origin: str, registration_id: str, tag: str, last_chance: bool) -> None:
		...
	
	@abstractmethod
	def enable(self) -> None:
		...
	
	@abstractmethod
	def set_force_update_on_page_load(self, force_update_on_page_load: bool) -> None:
		...
	
	@abstractmethod
	def skip_waiting(self, scope_url: str) -> None:
		...
	
	@abstractmethod
	def start_worker(self, scope_url: str) -> None:
		...
	
	@abstractmethod
	def stop_all_workers(self) -> None:
		...
	
	@abstractmethod
	def stop_worker(self, version_id: str) -> None:
		...
	
	@abstractmethod
	def unregister(self, scope_url: str) -> None:
		...
	
	@abstractmethod
	def update_registration(self, scope_url: str) -> None:
		...
