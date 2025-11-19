import trio
from typing import Any, Callable, Dict
from osn_selenium.base_mixin import TrioThreadMixin
from osn_selenium.executors.unified.cdp.service_worker import (
	UnifiedServiceWorkerCDPExecutor
)
from osn_selenium.abstract.executors.cdp.service_worker import (
	AbstractServiceWorkerCDPExecutor
)


__all__ = ["ServiceWorkerCDPExecutor"]


class ServiceWorkerCDPExecutor(
		UnifiedServiceWorkerCDPExecutor,
		TrioThreadMixin,
		AbstractServiceWorkerCDPExecutor
):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedServiceWorkerCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def deliver_push_message(self, origin: str, registration_id: str, data: str) -> None:
		return await self.sync_to_trio(sync_function=self._deliver_push_message_impl)(origin=origin, registration_id=registration_id, data=data)
	
	async def disable(self) -> None:
		return await self.sync_to_trio(sync_function=self._disable_impl)()
	
	async def dispatch_periodic_sync_event(self, origin: str, registration_id: str, tag: str) -> None:
		return await self.sync_to_trio(sync_function=self._dispatch_periodic_sync_event_impl)(origin=origin, registration_id=registration_id, tag=tag)
	
	async def dispatch_sync_event(self, origin: str, registration_id: str, tag: str, last_chance: bool) -> None:
		return await self.sync_to_trio(sync_function=self._dispatch_sync_event_impl)(
				origin=origin,
				registration_id=registration_id,
				tag=tag,
				last_chance=last_chance
		)
	
	async def enable(self) -> None:
		return await self.sync_to_trio(sync_function=self._enable_impl)()
	
	async def set_force_update_on_page_load(self, force_update_on_page_load: bool) -> None:
		return await self.sync_to_trio(sync_function=self._set_force_update_on_page_load_impl)(force_update_on_page_load=force_update_on_page_load)
	
	async def skip_waiting(self, scope_url: str) -> None:
		return await self.sync_to_trio(sync_function=self._skip_waiting_impl)(scope_url=scope_url)
	
	async def start_worker(self, scope_url: str) -> None:
		return await self.sync_to_trio(sync_function=self._start_worker_impl)(scope_url=scope_url)
	
	async def stop_all_workers(self) -> None:
		return await self.sync_to_trio(sync_function=self._stop_all_workers_impl)()
	
	async def stop_worker(self, version_id: str) -> None:
		return await self.sync_to_trio(sync_function=self._stop_worker_impl)(version_id=version_id)
	
	async def unregister(self, scope_url: str) -> None:
		return await self.sync_to_trio(sync_function=self._unregister_impl)(scope_url=scope_url)
	
	async def update_registration(self, scope_url: str) -> None:
		return await self.sync_to_trio(sync_function=self._update_registration_impl)(scope_url=scope_url)
