from typing import Any, Callable, Dict


__all__ = ["UnifiedServiceWorkerCDPExecutor"]


class UnifiedServiceWorkerCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _deliver_push_message_impl(self, origin: str, registration_id: str, data: str) -> None:
		return self._execute_function(
				"ServiceWorker.deliverPushMessage",
				{"origin": origin, "registration_id": registration_id, "data": data}
		)
	
	def _disable_impl(self) -> None:
		return self._execute_function("ServiceWorker.disable", {})
	
	def _dispatch_periodic_sync_event_impl(self, origin: str, registration_id: str, tag: str) -> None:
		return self._execute_function(
				"ServiceWorker.dispatchPeriodicSyncEvent",
				{"origin": origin, "registration_id": registration_id, "tag": tag}
		)
	
	def _dispatch_sync_event_impl(self, origin: str, registration_id: str, tag: str, last_chance: bool) -> None:
		return self._execute_function(
				"ServiceWorker.dispatchSyncEvent",
				{
					"origin": origin,
					"registration_id": registration_id,
					"tag": tag,
					"last_chance": last_chance
				}
		)
	
	def _enable_impl(self) -> None:
		return self._execute_function("ServiceWorker.enable", {})
	
	def _set_force_update_on_page_load_impl(self, force_update_on_page_load: bool) -> None:
		return self._execute_function(
				"ServiceWorker.setForceUpdateOnPageLoad",
				{"force_update_on_page_load": force_update_on_page_load}
		)
	
	def _skip_waiting_impl(self, scope_url: str) -> None:
		return self._execute_function("ServiceWorker.skipWaiting", {"scope_url": scope_url})
	
	def _start_worker_impl(self, scope_url: str) -> None:
		return self._execute_function("ServiceWorker.startWorker", {"scope_url": scope_url})
	
	def _stop_all_workers_impl(self) -> None:
		return self._execute_function("ServiceWorker.stopAllWorkers", {})
	
	def _stop_worker_impl(self, version_id: str) -> None:
		return self._execute_function("ServiceWorker.stopWorker", {"version_id": version_id})
	
	def _unregister_impl(self, scope_url: str) -> None:
		return self._execute_function("ServiceWorker.unregister", {"scope_url": scope_url})
	
	def _update_registration_impl(self, scope_url: str) -> None:
		return self._execute_function("ServiceWorker.updateRegistration", {"scope_url": scope_url})
