from typing import Any, Callable, Dict
from osn_selenium.abstract.executors.cdp.serviceworker import (
	AbstractServiceWorkerCDPExecutor
)


class ServiceWorkerCDPExecutor(AbstractServiceWorkerCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def deliver_push_message(self, origin: str, registration_id: str, data: str) -> None:
		return self._execute_function("ServiceWorker.deliverPushMessage", locals())
	
	def disable(self) -> None:
		return self._execute_function("ServiceWorker.disable", locals())
	
	def dispatch_periodic_sync_event(self, origin: str, registration_id: str, tag: str) -> None:
		return self._execute_function("ServiceWorker.dispatchPeriodicSyncEvent", locals())
	
	def dispatch_sync_event(self, origin: str, registration_id: str, tag: str, last_chance: bool) -> None:
		return self._execute_function("ServiceWorker.dispatchSyncEvent", locals())
	
	def enable(self) -> None:
		return self._execute_function("ServiceWorker.enable", locals())
	
	def set_force_update_on_page_load(self, force_update_on_page_load: bool) -> None:
		return self._execute_function("ServiceWorker.setForceUpdateOnPageLoad", locals())
	
	def skip_waiting(self, scope_url: str) -> None:
		return self._execute_function("ServiceWorker.skipWaiting", locals())
	
	def start_worker(self, scope_url: str) -> None:
		return self._execute_function("ServiceWorker.startWorker", locals())
	
	def stop_all_workers(self) -> None:
		return self._execute_function("ServiceWorker.stopAllWorkers", locals())
	
	def stop_worker(self, version_id: str) -> None:
		return self._execute_function("ServiceWorker.stopWorker", locals())
	
	def unregister(self, scope_url: str) -> None:
		return self._execute_function("ServiceWorker.unregister", locals())
	
	def update_registration(self, scope_url: str) -> None:
		return self._execute_function("ServiceWorker.updateRegistration", locals())
