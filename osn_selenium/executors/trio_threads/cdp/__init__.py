from typing import (
	Any,
	Callable,
	Coroutine,
	Dict
)
from osn_selenium.abstract.executors.cdp import AbstractCDPExecutor
from osn_selenium.executors.trio_threads.cdp.io import IoCDPExecutor
from osn_selenium.executors.trio_threads.cdp.css import CssCDPExecutor
from osn_selenium.executors.trio_threads.cdp.dom import DomCDPExecutor
from osn_selenium.executors.trio_threads.cdp.log import LogCDPExecutor
from osn_selenium.executors.trio_threads.cdp.pwa import PwaCDPExecutor
from osn_selenium.executors.trio_threads.cdp.cast import CastCDPExecutor
from osn_selenium.executors.trio_threads.cdp.page import PageCDPExecutor
from osn_selenium.executors.trio_threads.cdp.fetch import FetchCDPExecutor
from osn_selenium.executors.trio_threads.cdp.input import InputCDPExecutor
from osn_selenium.executors.trio_threads.cdp.media import MediaCDPExecutor
from osn_selenium.executors.trio_threads.cdp.fed_cm import FedCmCDPExecutor
from osn_selenium.executors.trio_threads.cdp.audits import AuditsCDPExecutor
from osn_selenium.executors.trio_threads.cdp.memory import MemoryCDPExecutor
from osn_selenium.executors.trio_threads.cdp.schema import SchemaCDPExecutor
from osn_selenium.executors.trio_threads.cdp.target import TargetCDPExecutor
from osn_selenium.executors.trio_threads.cdp.browser import BrowserCDPExecutor
from osn_selenium.executors.trio_threads.cdp.console import ConsoleCDPExecutor
from osn_selenium.executors.trio_threads.cdp.network import NetworkCDPExecutor
from osn_selenium.executors.trio_threads.cdp.overlay import OverlayCDPExecutor
from osn_selenium.executors.trio_threads.cdp.preload import PreloadCDPExecutor
from osn_selenium.executors.trio_threads.cdp.runtime import RuntimeCDPExecutor
from osn_selenium.executors.trio_threads.cdp.storage import StorageCDPExecutor
from osn_selenium.executors.trio_threads.cdp.tracing import TracingCDPExecutor
from osn_selenium.executors.trio_threads.cdp.autofill import AutofillCDPExecutor
from osn_selenium.executors.trio_threads.cdp.debugger import DebuggerCDPExecutor
from osn_selenium.executors.trio_threads.cdp.profiler import ProfilerCDPExecutor
from osn_selenium.executors.trio_threads.cdp.security import SecurityCDPExecutor
from osn_selenium.executors.trio_threads.cdp.web_audio import WebAudioCDPExecutor
from osn_selenium.executors.trio_threads.cdp.web_authn import WebAuthnCDPExecutor
from osn_selenium.executors.trio_threads.cdp.animation import AnimationCDPExecutor
from osn_selenium.executors.trio_threads.cdp.emulation import EmulationCDPExecutor
from osn_selenium.executors.trio_threads.cdp.inspector import InspectorCDPExecutor
from osn_selenium.executors.trio_threads.cdp.tethering import TetheringCDPExecutor
from osn_selenium.executors.trio_threads.cdp.indexed_db import IndexedDbCDPExecutor
from osn_selenium.executors.trio_threads.cdp.layer_tree import LayerTreeCDPExecutor
from osn_selenium.executors.trio_threads.cdp.extensions import (
	ExtensionsCDPExecutor
)
from osn_selenium.executors.trio_threads.cdp.dom_storage import (
	DomStorageCDPExecutor
)
from osn_selenium.executors.trio_threads.cdp.file_system import (
	FileSystemCDPExecutor
)
from osn_selenium.executors.trio_threads.cdp.system_info import (
	SystemInfoCDPExecutor
)
from osn_selenium.executors.trio_threads.cdp.performance import (
	PerformanceCDPExecutor
)
from osn_selenium.executors.trio_threads.cdp.dom_debugger import (
	DomDebuggerCDPExecutor
)
from osn_selenium.executors.trio_threads.cdp.dom_snapshot import (
	DomSnapshotCDPExecutor
)
from osn_selenium.executors.trio_threads.cdp.cache_storage import (
	CacheStorageCDPExecutor
)
from osn_selenium.executors.trio_threads.cdp.device_access import (
	DeviceAccessCDPExecutor
)
from osn_selenium.executors.trio_threads.cdp.heap_profiler import (
	HeapProfilerCDPExecutor
)
from osn_selenium.executors.trio_threads.cdp.accessibility import (
	AccessibilityCDPExecutor
)
from osn_selenium.executors.trio_threads.cdp.service_worker import (
	ServiceWorkerCDPExecutor
)
from osn_selenium.executors.trio_threads.cdp.event_breakpoints import (
	EventBreakpointsCDPExecutor
)
from osn_selenium.executors.trio_threads.cdp.background_service import (
	BackgroundServiceCDPExecutor
)
from osn_selenium.executors.trio_threads.cdp.device_orientation import (
	DeviceOrientationCDPExecutor
)
from osn_selenium.executors.trio_threads.cdp.bluetooth_emulation import (
	BluetoothEmulationCDPExecutor
)
from osn_selenium.executors.trio_threads.cdp.performance_timeline import (
	PerformanceTimelineCDPExecutor
)
from osn_selenium.executors.trio_threads.cdp.headless_experimental import (
	HeadlessExperimentalCDPExecutor
)


class CDPExecutor(AbstractCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
		
		self._accessibility = AccessibilityCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._animation = AnimationCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._audits = AuditsCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._autofill = AutofillCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._background_service = BackgroundServiceCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._bluetooth_emulation = BluetoothEmulationCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._browser = BrowserCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._css = CssCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._cache_storage = CacheStorageCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._cast = CastCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._console = ConsoleCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._dom = DomCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._dom_debugger = DomDebuggerCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._dom_snapshot = DomSnapshotCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._dom_storage = DomStorageCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._debugger = DebuggerCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._device_access = DeviceAccessCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._device_orientation = DeviceOrientationCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._emulation = EmulationCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._event_breakpoints = EventBreakpointsCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._extensions = ExtensionsCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._fed_cm = FedCmCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._fetch = FetchCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._file_system = FileSystemCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._headless_experimental = HeadlessExperimentalCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._heap_profiler = HeapProfilerCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._io = IoCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._indexed_db = IndexedDbCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._input = InputCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._inspector = InspectorCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._layer_tree = LayerTreeCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._log = LogCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._media = MediaCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._memory = MemoryCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._network = NetworkCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._overlay = OverlayCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._pwa = PwaCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._page = PageCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._performance = PerformanceCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._performance_timeline = PerformanceTimelineCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._preload = PreloadCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._profiler = ProfilerCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._runtime = RuntimeCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._schema = SchemaCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._security = SecurityCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._service_worker = ServiceWorkerCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._storage = StorageCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._system_info = SystemInfoCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._target = TargetCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._tethering = TetheringCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._tracing = TracingCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._web_audio = WebAudioCDPExecutor(execute_function=self._prepare_and_execute)
		
		self._web_authn = WebAuthnCDPExecutor(execute_function=self._prepare_and_execute)
	
	async def execute(self, cmd: str, cmd_args: Dict[str, Any]) -> Any:
		return (await self._execute_function(cmd, cmd_args))["value"]
	
	async def _prepare_and_execute(self, command_name: str, locals_: Dict[str, Any]) -> Any:
		locals_.pop("self")
		return await self.execute(cmd=command_name, cmd_args=locals_)
	
	@property
	def accessibility(self) -> AccessibilityCDPExecutor:
		return self._accessibility
	
	@property
	def animation(self) -> AnimationCDPExecutor:
		return self._animation
	
	@property
	def audits(self) -> AuditsCDPExecutor:
		return self._audits
	
	@property
	def autofill(self) -> AutofillCDPExecutor:
		return self._autofill
	
	@property
	def background_service(self) -> BackgroundServiceCDPExecutor:
		return self._background_service
	
	@property
	def bluetooth_emulation(self) -> BluetoothEmulationCDPExecutor:
		return self._bluetooth_emulation
	
	@property
	def browser(self) -> BrowserCDPExecutor:
		return self._browser
	
	@property
	def cache_storage(self) -> CacheStorageCDPExecutor:
		return self._cache_storage
	
	@property
	def cast(self) -> CastCDPExecutor:
		return self._cast
	
	@property
	def console(self) -> ConsoleCDPExecutor:
		return self._console
	
	@property
	def css(self) -> CssCDPExecutor:
		return self._css
	
	@property
	def debugger(self) -> DebuggerCDPExecutor:
		return self._debugger
	
	@property
	def device_access(self) -> DeviceAccessCDPExecutor:
		return self._device_access
	
	@property
	def device_orientation(self) -> DeviceOrientationCDPExecutor:
		return self._device_orientation
	
	@property
	def dom(self) -> DomCDPExecutor:
		return self._dom
	
	@property
	def dom_debugger(self) -> DomDebuggerCDPExecutor:
		return self._dom_debugger
	
	@property
	def dom_snapshot(self) -> DomSnapshotCDPExecutor:
		return self._dom_snapshot
	
	@property
	def dom_storage(self) -> DomStorageCDPExecutor:
		return self._dom_storage
	
	@property
	def emulation(self) -> EmulationCDPExecutor:
		return self._emulation
	
	@property
	def event_breakpoints(self) -> EventBreakpointsCDPExecutor:
		return self._event_breakpoints
	
	@property
	def extensions(self) -> ExtensionsCDPExecutor:
		return self._extensions
	
	@property
	def fed_cm(self) -> FedCmCDPExecutor:
		return self._fed_cm
	
	@property
	def fetch(self) -> FetchCDPExecutor:
		return self._fetch
	
	@property
	def file_system(self) -> FileSystemCDPExecutor:
		return self._file_system
	
	@property
	def headless_experimental(self) -> HeadlessExperimentalCDPExecutor:
		return self._headless_experimental
	
	@property
	def heap_profiler(self) -> HeapProfilerCDPExecutor:
		return self._heap_profiler
	
	@property
	def indexed_db(self) -> IndexedDbCDPExecutor:
		return self._indexed_db
	
	@property
	def input(self) -> InputCDPExecutor:
		return self._input
	
	@property
	def inspector(self) -> InspectorCDPExecutor:
		return self._inspector
	
	@property
	def io(self) -> IoCDPExecutor:
		return self._io
	
	@property
	def layer_tree(self) -> LayerTreeCDPExecutor:
		return self._layer_tree
	
	@property
	def log(self) -> LogCDPExecutor:
		return self._log
	
	@property
	def media(self) -> MediaCDPExecutor:
		return self._media
	
	@property
	def memory(self) -> MemoryCDPExecutor:
		return self._memory
	
	@property
	def network(self) -> NetworkCDPExecutor:
		return self._network
	
	@property
	def overlay(self) -> OverlayCDPExecutor:
		return self._overlay
	
	@property
	def page(self) -> PageCDPExecutor:
		return self._page
	
	@property
	def performance(self) -> PerformanceCDPExecutor:
		return self._performance
	
	@property
	def performance_timeline(self) -> PerformanceTimelineCDPExecutor:
		return self._performance_timeline
	
	@property
	def preload(self) -> PreloadCDPExecutor:
		return self._preload
	
	@property
	def profiler(self) -> ProfilerCDPExecutor:
		return self._profiler
	
	@property
	def pwa(self) -> PwaCDPExecutor:
		return self._pwa
	
	@property
	def runtime(self) -> RuntimeCDPExecutor:
		return self._runtime
	
	@property
	def schema(self) -> SchemaCDPExecutor:
		return self._schema
	
	@property
	def security(self) -> SecurityCDPExecutor:
		return self._security
	
	@property
	def service_worker(self) -> ServiceWorkerCDPExecutor:
		return self._service_worker
	
	@property
	def storage(self) -> StorageCDPExecutor:
		return self._storage
	
	@property
	def system_info(self) -> SystemInfoCDPExecutor:
		return self._system_info
	
	@property
	def target(self) -> TargetCDPExecutor:
		return self._target
	
	@property
	def tethering(self) -> TetheringCDPExecutor:
		return self._tethering
	
	@property
	def tracing(self) -> TracingCDPExecutor:
		return self._tracing
	
	@property
	def web_audio(self) -> WebAudioCDPExecutor:
		return self._web_audio
	
	@property
	def web_authn(self) -> WebAuthnCDPExecutor:
		return self._web_authn
