from typing import (
	Any,
	Callable,
	Coroutine,
	Dict
)
from osn_selenium.abstract.executors.cdp.serviceworker import (
	AbstractServiceWorkerCDPExecutor
)


class AsyncServiceWorkerCDPExecutor(AbstractServiceWorkerCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def deliver_push_message(self, origin: str, registration_id: str, data: str) -> None:
		return await self._execute_function("ServiceWorker.deliverPushMessage", locals())
	
	async def disable(self) -> None:
		return await self._execute_function("ServiceWorker.disable", locals())
	
	async def dispatch_periodic_sync_event(self, origin: str, registration_id: str, tag: str) -> None:
		return await self._execute_function("ServiceWorker.dispatchPeriodicSyncEvent", locals())
	
	async def dispatch_sync_event(self, origin: str, registration_id: str, tag: str, last_chance: bool) -> None:
		return await self._execute_function("ServiceWorker.dispatchSyncEvent", locals())
	
	async def enable(self) -> None:
		return await self._execute_function("ServiceWorker.enable", locals())
	
	async def set_force_update_on_page_load(self, force_update_on_page_load: bool) -> None:
		return await self._execute_function("ServiceWorker.setForceUpdateOnPageLoad", locals())
	
	async def skip_waiting(self, scope_url: str) -> None:
		return await self._execute_function("ServiceWorker.skipWaiting", locals())
	
	async def start_worker(self, scope_url: str) -> None:
		return await self._execute_function("ServiceWorker.startWorker", locals())
	
	async def stop_all_workers(self) -> None:
		return await self._execute_function("ServiceWorker.stopAllWorkers", locals())
	
	async def stop_worker(self, version_id: str) -> None:
		return await self._execute_function("ServiceWorker.stopWorker", locals())
	
	async def unregister(self, scope_url: str) -> None:
		return await self._execute_function("ServiceWorker.unregister", locals())
	
	async def update_registration(self, scope_url: str) -> None:
		return await self._execute_function("ServiceWorker.updateRegistration", locals())
