from typing import Any, Dict
from abc import ABC, abstractmethod
from osn_selenium.abstract.executors.cdp.io import (
	AbstractIoCDPExecutor
)
from osn_selenium.abstract.executors.cdp.css import (
	AbstractCssCDPExecutor
)
from osn_selenium.abstract.executors.cdp.dom import (
	AbstractDomCDPExecutor
)
from osn_selenium.abstract.executors.cdp.log import (
	AbstractLogCDPExecutor
)
from osn_selenium.abstract.executors.cdp.pwa import (
	AbstractPwaCDPExecutor
)
from osn_selenium.abstract.executors.cdp.cast import (
	AbstractCastCDPExecutor
)
from osn_selenium.abstract.executors.cdp.page import (
	AbstractPageCDPExecutor
)
from osn_selenium.abstract.executors.cdp.fetch import (
	AbstractFetchCDPExecutor
)
from osn_selenium.abstract.executors.cdp.input import (
	AbstractInputCDPExecutor
)
from osn_selenium.abstract.executors.cdp.media import (
	AbstractMediaCDPExecutor
)
from osn_selenium.abstract.executors.cdp.fed_cm import (
	AbstractFedCmCDPExecutor
)
from osn_selenium.abstract.executors.cdp.audits import (
	AbstractAuditsCDPExecutor
)
from osn_selenium.abstract.executors.cdp.memory import (
	AbstractMemoryCDPExecutor
)
from osn_selenium.abstract.executors.cdp.schema import (
	AbstractSchemaCDPExecutor
)
from osn_selenium.abstract.executors.cdp.target import (
	AbstractTargetCDPExecutor
)
from osn_selenium.abstract.executors.cdp.browser import (
	AbstractBrowserCDPExecutor
)
from osn_selenium.abstract.executors.cdp.console import (
	AbstractConsoleCDPExecutor
)
from osn_selenium.abstract.executors.cdp.network import (
	AbstractNetworkCDPExecutor
)
from osn_selenium.abstract.executors.cdp.overlay import (
	AbstractOverlayCDPExecutor
)
from osn_selenium.abstract.executors.cdp.preload import (
	AbstractPreloadCDPExecutor
)
from osn_selenium.abstract.executors.cdp.runtime import (
	AbstractRuntimeCDPExecutor
)
from osn_selenium.abstract.executors.cdp.storage import (
	AbstractStorageCDPExecutor
)
from osn_selenium.abstract.executors.cdp.tracing import (
	AbstractTracingCDPExecutor
)
from osn_selenium.abstract.executors.cdp.autofill import (
	AbstractAutofillCDPExecutor
)
from osn_selenium.abstract.executors.cdp.debugger import (
	AbstractDebuggerCDPExecutor
)
from osn_selenium.abstract.executors.cdp.profiler import (
	AbstractProfilerCDPExecutor
)
from osn_selenium.abstract.executors.cdp.security import (
	AbstractSecurityCDPExecutor
)
from osn_selenium.abstract.executors.cdp.web_audio import (
	AbstractWebAudioCDPExecutor
)
from osn_selenium.abstract.executors.cdp.web_authn import (
	AbstractWebAuthnCDPExecutor
)
from osn_selenium.abstract.executors.cdp.animation import (
	AbstractAnimationCDPExecutor
)
from osn_selenium.abstract.executors.cdp.emulation import (
	AbstractEmulationCDPExecutor
)
from osn_selenium.abstract.executors.cdp.inspector import (
	AbstractInspectorCDPExecutor
)
from osn_selenium.abstract.executors.cdp.tethering import (
	AbstractTetheringCDPExecutor
)
from osn_selenium.abstract.executors.cdp.indexed_db import (
	AbstractIndexedDbCDPExecutor
)
from osn_selenium.abstract.executors.cdp.layer_tree import (
	AbstractLayerTreeCDPExecutor
)
from osn_selenium.abstract.executors.cdp.extensions import (
	AbstractExtensionsCDPExecutor
)
from osn_selenium.abstract.executors.cdp.dom_storage import (
	AbstractDomStorageCDPExecutor
)
from osn_selenium.abstract.executors.cdp.file_system import (
	AbstractFileSystemCDPExecutor
)
from osn_selenium.abstract.executors.cdp.system_info import (
	AbstractSystemInfoCDPExecutor
)
from osn_selenium.abstract.executors.cdp.performance import (
	AbstractPerformanceCDPExecutor
)
from osn_selenium.abstract.executors.cdp.dom_debugger import (
	AbstractDomDebuggerCDPExecutor
)
from osn_selenium.abstract.executors.cdp.dom_snapshot import (
	AbstractDomSnapshotCDPExecutor
)
from osn_selenium.abstract.executors.cdp.cache_storage import (
	AbstractCacheStorageCDPExecutor
)
from osn_selenium.abstract.executors.cdp.device_access import (
	AbstractDeviceAccessCDPExecutor
)
from osn_selenium.abstract.executors.cdp.heap_profiler import (
	AbstractHeapProfilerCDPExecutor
)
from osn_selenium.abstract.executors.cdp.accessibility import (
	AbstractAccessibilityCDPExecutor
)
from osn_selenium.abstract.executors.cdp.service_worker import (
	AbstractServiceWorkerCDPExecutor
)
from osn_selenium.abstract.executors.cdp.event_breakpoints import (
	AbstractEventBreakpointsCDPExecutor
)
from osn_selenium.abstract.executors.cdp.background_service import (
	AbstractBackgroundServiceCDPExecutor
)
from osn_selenium.abstract.executors.cdp.device_orientation import (
	AbstractDeviceOrientationCDPExecutor
)
from osn_selenium.abstract.executors.cdp.bluetooth_emulation import (
	AbstractBluetoothEmulationCDPExecutor
)
from osn_selenium.abstract.executors.cdp.performance_timeline import (
	AbstractPerformanceTimelineCDPExecutor
)
from osn_selenium.abstract.executors.cdp.headless_experimental import (
	AbstractHeadlessExperimentalCDPExecutor
)


__all__ = ["AbstractCDPExecutor"]


class AbstractCDPExecutor(ABC):
	@property
	@abstractmethod
	def accessibility(self) -> AbstractAccessibilityCDPExecutor:
		...
	
	@property
	@abstractmethod
	def animation(self) -> AbstractAnimationCDPExecutor:
		...
	
	@property
	@abstractmethod
	def audits(self) -> AbstractAuditsCDPExecutor:
		...
	
	@property
	@abstractmethod
	def autofill(self) -> AbstractAutofillCDPExecutor:
		...
	
	@property
	@abstractmethod
	def background_service(self) -> AbstractBackgroundServiceCDPExecutor:
		...
	
	@property
	@abstractmethod
	def bluetooth_emulation(self) -> AbstractBluetoothEmulationCDPExecutor:
		...
	
	@property
	@abstractmethod
	def browser(self) -> AbstractBrowserCDPExecutor:
		...
	
	@property
	@abstractmethod
	def cache_storage(self) -> AbstractCacheStorageCDPExecutor:
		...
	
	@property
	@abstractmethod
	def cast(self) -> AbstractCastCDPExecutor:
		...
	
	@property
	@abstractmethod
	def console(self) -> AbstractConsoleCDPExecutor:
		...
	
	@property
	@abstractmethod
	def css(self) -> AbstractCssCDPExecutor:
		...
	
	@property
	@abstractmethod
	def debugger(self) -> AbstractDebuggerCDPExecutor:
		...
	
	@property
	@abstractmethod
	def device_access(self) -> AbstractDeviceAccessCDPExecutor:
		...
	
	@property
	@abstractmethod
	def device_orientation(self) -> AbstractDeviceOrientationCDPExecutor:
		...
	
	@property
	@abstractmethod
	def dom(self) -> AbstractDomCDPExecutor:
		...
	
	@property
	@abstractmethod
	def dom_debugger(self) -> AbstractDomDebuggerCDPExecutor:
		...
	
	@property
	@abstractmethod
	def dom_snapshot(self) -> AbstractDomSnapshotCDPExecutor:
		...
	
	@property
	@abstractmethod
	def dom_storage(self) -> AbstractDomStorageCDPExecutor:
		...
	
	@property
	@abstractmethod
	def emulation(self) -> AbstractEmulationCDPExecutor:
		...
	
	@property
	@abstractmethod
	def event_breakpoints(self) -> AbstractEventBreakpointsCDPExecutor:
		...
	
	@abstractmethod
	def execute(self, cmd: str, cmd_args: Dict[str, Any]) -> Any:
		...
	
	@property
	@abstractmethod
	def extensions(self) -> AbstractExtensionsCDPExecutor:
		...
	
	@property
	@abstractmethod
	def fed_cm(self) -> AbstractFedCmCDPExecutor:
		...
	
	@property
	@abstractmethod
	def fetch(self) -> AbstractFetchCDPExecutor:
		...
	
	@property
	@abstractmethod
	def file_system(self) -> AbstractFileSystemCDPExecutor:
		...
	
	@property
	@abstractmethod
	def headless_experimental(self) -> AbstractHeadlessExperimentalCDPExecutor:
		...
	
	@property
	@abstractmethod
	def heap_profiler(self) -> AbstractHeapProfilerCDPExecutor:
		...
	
	@property
	@abstractmethod
	def indexed_db(self) -> AbstractIndexedDbCDPExecutor:
		...
	
	@property
	@abstractmethod
	def input(self) -> AbstractInputCDPExecutor:
		...
	
	@property
	@abstractmethod
	def inspector(self) -> AbstractInspectorCDPExecutor:
		...
	
	@property
	@abstractmethod
	def io(self) -> AbstractIoCDPExecutor:
		...
	
	@property
	@abstractmethod
	def layer_tree(self) -> AbstractLayerTreeCDPExecutor:
		...
	
	@property
	@abstractmethod
	def log(self) -> AbstractLogCDPExecutor:
		...
	
	@property
	@abstractmethod
	def media(self) -> AbstractMediaCDPExecutor:
		...
	
	@property
	@abstractmethod
	def memory(self) -> AbstractMemoryCDPExecutor:
		...
	
	@property
	@abstractmethod
	def network(self) -> AbstractNetworkCDPExecutor:
		...
	
	@property
	@abstractmethod
	def overlay(self) -> AbstractOverlayCDPExecutor:
		...
	
	@property
	@abstractmethod
	def page(self) -> AbstractPageCDPExecutor:
		...
	
	@property
	@abstractmethod
	def performance(self) -> AbstractPerformanceCDPExecutor:
		...
	
	@property
	@abstractmethod
	def performance_timeline(self) -> AbstractPerformanceTimelineCDPExecutor:
		...
	
	@property
	@abstractmethod
	def preload(self) -> AbstractPreloadCDPExecutor:
		...
	
	@property
	@abstractmethod
	def profiler(self) -> AbstractProfilerCDPExecutor:
		...
	
	@property
	@abstractmethod
	def pwa(self) -> AbstractPwaCDPExecutor:
		...
	
	@property
	@abstractmethod
	def runtime(self) -> AbstractRuntimeCDPExecutor:
		...
	
	@property
	@abstractmethod
	def schema(self) -> AbstractSchemaCDPExecutor:
		...
	
	@property
	@abstractmethod
	def security(self) -> AbstractSecurityCDPExecutor:
		...
	
	@property
	@abstractmethod
	def service_worker(self) -> AbstractServiceWorkerCDPExecutor:
		...
	
	@property
	@abstractmethod
	def storage(self) -> AbstractStorageCDPExecutor:
		...
	
	@property
	@abstractmethod
	def system_info(self) -> AbstractSystemInfoCDPExecutor:
		...
	
	@property
	@abstractmethod
	def target(self) -> AbstractTargetCDPExecutor:
		...
	
	@property
	@abstractmethod
	def tethering(self) -> AbstractTetheringCDPExecutor:
		...
	
	@property
	@abstractmethod
	def tracing(self) -> AbstractTracingCDPExecutor:
		...
	
	@property
	@abstractmethod
	def web_audio(self) -> AbstractWebAudioCDPExecutor:
		...
	
	@property
	@abstractmethod
	def web_authn(self) -> AbstractWebAuthnCDPExecutor:
		...
