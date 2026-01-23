from typing import Any, Callable, Dict
from osn_selenium.executors.unified.cdp.service_worker import (
	UnifiedServiceWorkerCDPExecutor
)
from osn_selenium.abstract.executors.cdp.service_worker import (
	AbstractServiceWorkerCDPExecutor
)


__all__ = ["ServiceWorkerCDPExecutor"]


class ServiceWorkerCDPExecutor(UnifiedServiceWorkerCDPExecutor, AbstractServiceWorkerCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedServiceWorkerCDPExecutor.__init__(self, execute_function=execute_function)
	
	def deliver_push_message(self, origin: str, registration_id: str, data: str) -> None:
		return self._deliver_push_message_impl(origin=origin, registration_id=registration_id, data=data)
	
	def disable(self) -> None:
		return self._disable_impl()
	
	def dispatch_periodic_sync_event(self, origin: str, registration_id: str, tag: str) -> None:
		return self._dispatch_periodic_sync_event_impl(origin=origin, registration_id=registration_id, tag=tag)
	
	def dispatch_sync_event(self, origin: str, registration_id: str, tag: str, last_chance: bool) -> None:
		return self._dispatch_sync_event_impl(
				origin=origin,
				registration_id=registration_id,
				tag=tag,
				last_chance=last_chance
		)
	
	def enable(self) -> None:
		return self._enable_impl()
	
	def set_force_update_on_page_load(self, force_update_on_page_load: bool) -> None:
		return self._set_force_update_on_page_load_impl(force_update_on_page_load=force_update_on_page_load)
	
	def skip_waiting(self, scope_url: str) -> None:
		return self._skip_waiting_impl(scope_url=scope_url)
	
	def start_worker(self, scope_url: str) -> None:
		return self._start_worker_impl(scope_url=scope_url)
	
	def stop_all_workers(self) -> None:
		return self._stop_all_workers_impl()
	
	def stop_worker(self, version_id: str) -> None:
		return self._stop_worker_impl(version_id=version_id)
	
	def unregister(self, scope_url: str) -> None:
		return self._unregister_impl(scope_url=scope_url)
	
	def update_registration(self, scope_url: str) -> None:
		return self._update_registration_impl(scope_url=scope_url)
