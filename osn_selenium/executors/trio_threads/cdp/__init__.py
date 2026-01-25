import trio
from osn_selenium.base_mixin import TrioThreadMixin
from typing import (
	Any,
	Callable,
	Dict,
	TYPE_CHECKING
)
from osn_selenium.abstract.executors.cdp import AbstractCDPExecutor


__all__ = ["CDPExecutor"]

if TYPE_CHECKING:
	from osn_selenium.executors.trio_threads.cdp.accessibility import AccessibilityCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.animation import AnimationCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.audits import AuditsCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.autofill import AutofillCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.background_service import BackgroundServiceCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.bluetooth_emulation import BluetoothEmulationCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.browser import BrowserCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.css import CssCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.cache_storage import CacheStorageCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.cast import CastCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.console import ConsoleCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.dom import DomCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.dom_debugger import DomDebuggerCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.dom_snapshot import DomSnapshotCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.dom_storage import DomStorageCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.debugger import DebuggerCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.device_access import DeviceAccessCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.device_orientation import DeviceOrientationCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.emulation import EmulationCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.event_breakpoints import EventBreakpointsCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.extensions import ExtensionsCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.fed_cm import FedCmCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.fetch import FetchCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.file_system import FileSystemCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.headless_experimental import HeadlessExperimentalCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.heap_profiler import HeapProfilerCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.io import IoCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.indexed_db import IndexedDbCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.input import InputCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.inspector import InspectorCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.layer_tree import LayerTreeCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.log import LogCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.media import MediaCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.memory import MemoryCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.network import NetworkCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.overlay import OverlayCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.pwa import PwaCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.page import PageCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.performance import PerformanceCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.performance_timeline import PerformanceTimelineCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.preload import PreloadCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.profiler import ProfilerCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.runtime import RuntimeCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.schema import SchemaCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.security import SecurityCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.service_worker import ServiceWorkerCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.storage import StorageCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.system_info import SystemInfoCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.target import TargetCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.tethering import TetheringCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.tracing import TracingCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.web_audio import WebAudioCDPExecutor
	from osn_selenium.executors.trio_threads.cdp.web_authn import WebAuthnCDPExecutor


class CDPExecutor(TrioThreadMixin, AbstractCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		super().__init__(lock=lock, limiter=limiter)
		
		self._execute_function = execute_function
		self._accessibility = None
		self._animation = None
		self._audits = None
		self._autofill = None
		self._background_service = None
		self._bluetooth_emulation = None
		self._browser = None
		self._css = None
		self._cache_storage = None
		self._cast = None
		self._console = None
		self._dom = None
		self._dom_debugger = None
		self._dom_snapshot = None
		self._dom_storage = None
		self._debugger = None
		self._device_access = None
		self._device_orientation = None
		self._emulation = None
		self._event_breakpoints = None
		self._extensions = None
		self._fed_cm = None
		self._fetch = None
		self._file_system = None
		self._headless_experimental = None
		self._heap_profiler = None
		self._io = None
		self._indexed_db = None
		self._input = None
		self._inspector = None
		self._layer_tree = None
		self._log = None
		self._media = None
		self._memory = None
		self._network = None
		self._overlay = None
		self._pwa = None
		self._page = None
		self._performance = None
		self._performance_timeline = None
		self._preload = None
		self._profiler = None
		self._runtime = None
		self._schema = None
		self._security = None
		self._service_worker = None
		self._storage = None
		self._system_info = None
		self._target = None
		self._tethering = None
		self._tracing = None
		self._web_audio = None
		self._web_authn = None
	
	@property
	def accessibility(self) -> "AccessibilityCDPExecutor":
		if self._accessibility is None:
			from osn_selenium.executors.trio_threads.cdp.accessibility import AccessibilityCDPExecutor
			self._accessibility = AccessibilityCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._accessibility
	
	@property
	def animation(self) -> "AnimationCDPExecutor":
		if self._animation is None:
			from osn_selenium.executors.trio_threads.cdp.animation import AnimationCDPExecutor
			self._animation = AnimationCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._animation
	
	@property
	def audits(self) -> "AuditsCDPExecutor":
		if self._audits is None:
			from osn_selenium.executors.trio_threads.cdp.audits import AuditsCDPExecutor
			self._audits = AuditsCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._audits
	
	@property
	def autofill(self) -> "AutofillCDPExecutor":
		if self._autofill is None:
			from osn_selenium.executors.trio_threads.cdp.autofill import AutofillCDPExecutor
			self._autofill = AutofillCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._autofill
	
	@property
	def background_service(self) -> "BackgroundServiceCDPExecutor":
		if self._background_service is None:
			from osn_selenium.executors.trio_threads.cdp.background_service import BackgroundServiceCDPExecutor
			self._background_service = BackgroundServiceCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._background_service
	
	@property
	def bluetooth_emulation(self) -> "BluetoothEmulationCDPExecutor":
		if self._bluetooth_emulation is None:
			from osn_selenium.executors.trio_threads.cdp.bluetooth_emulation import BluetoothEmulationCDPExecutor
			self._bluetooth_emulation = BluetoothEmulationCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._bluetooth_emulation
	
	@property
	def browser(self) -> "BrowserCDPExecutor":
		if self._browser is None:
			from osn_selenium.executors.trio_threads.cdp.browser import BrowserCDPExecutor
			self._browser = BrowserCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._browser
	
	@property
	def cache_storage(self) -> "CacheStorageCDPExecutor":
		if self._cache_storage is None:
			from osn_selenium.executors.trio_threads.cdp.cache_storage import CacheStorageCDPExecutor
			self._cache_storage = CacheStorageCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._cache_storage
	
	@property
	def cast(self) -> "CastCDPExecutor":
		if self._cast is None:
			from osn_selenium.executors.trio_threads.cdp.cast import CastCDPExecutor
			self._cast = CastCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._cast
	
	@property
	def console(self) -> "ConsoleCDPExecutor":
		if self._console is None:
			from osn_selenium.executors.trio_threads.cdp.console import ConsoleCDPExecutor
			self._console = ConsoleCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._console
	
	@property
	def css(self) -> "CssCDPExecutor":
		if self._css is None:
			from osn_selenium.executors.trio_threads.cdp.css import CssCDPExecutor
			self._css = CssCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._css
	
	@property
	def debugger(self) -> "DebuggerCDPExecutor":
		if self._debugger is None:
			from osn_selenium.executors.trio_threads.cdp.debugger import DebuggerCDPExecutor
			self._debugger = DebuggerCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._debugger
	
	@property
	def device_access(self) -> "DeviceAccessCDPExecutor":
		if self._device_access is None:
			from osn_selenium.executors.trio_threads.cdp.device_access import DeviceAccessCDPExecutor
			self._device_access = DeviceAccessCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._device_access
	
	@property
	def device_orientation(self) -> "DeviceOrientationCDPExecutor":
		if self._device_orientation is None:
			from osn_selenium.executors.trio_threads.cdp.device_orientation import DeviceOrientationCDPExecutor
			self._device_orientation = DeviceOrientationCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._device_orientation
	
	@property
	def dom(self) -> "DomCDPExecutor":
		if self._dom is None:
			from osn_selenium.executors.trio_threads.cdp.dom import DomCDPExecutor
			self._dom = DomCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._dom
	
	@property
	def dom_debugger(self) -> "DomDebuggerCDPExecutor":
		if self._dom_debugger is None:
			from osn_selenium.executors.trio_threads.cdp.dom_debugger import DomDebuggerCDPExecutor
			self._dom_debugger = DomDebuggerCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._dom_debugger
	
	@property
	def dom_snapshot(self) -> "DomSnapshotCDPExecutor":
		if self._dom_snapshot is None:
			from osn_selenium.executors.trio_threads.cdp.dom_snapshot import DomSnapshotCDPExecutor
			self._dom_snapshot = DomSnapshotCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._dom_snapshot
	
	@property
	def dom_storage(self) -> "DomStorageCDPExecutor":
		if self._dom_storage is None:
			from osn_selenium.executors.trio_threads.cdp.dom_storage import DomStorageCDPExecutor
			self._dom_storage = DomStorageCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._dom_storage
	
	@property
	def emulation(self) -> "EmulationCDPExecutor":
		if self._emulation is None:
			from osn_selenium.executors.trio_threads.cdp.emulation import EmulationCDPExecutor
			self._emulation = EmulationCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._emulation
	
	@property
	def event_breakpoints(self) -> "EventBreakpointsCDPExecutor":
		if self._event_breakpoints is None:
			from osn_selenium.executors.trio_threads.cdp.event_breakpoints import EventBreakpointsCDPExecutor
			self._event_breakpoints = EventBreakpointsCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._event_breakpoints
	
	async def execute(self, cmd: str, cmd_args: Dict[str, Any]) -> Any:
		return (await self._execute_function(cmd, cmd_args))["value"]
	
	@property
	def extensions(self) -> "ExtensionsCDPExecutor":
		if self._extensions is None:
			from osn_selenium.executors.trio_threads.cdp.extensions import ExtensionsCDPExecutor
			self._extensions = ExtensionsCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._extensions
	
	@property
	def fed_cm(self) -> "FedCmCDPExecutor":
		if self._fed_cm is None:
			from osn_selenium.executors.trio_threads.cdp.fed_cm import FedCmCDPExecutor
			self._fed_cm = FedCmCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._fed_cm
	
	@property
	def fetch(self) -> "FetchCDPExecutor":
		if self._fetch is None:
			from osn_selenium.executors.trio_threads.cdp.fetch import FetchCDPExecutor
			self._fetch = FetchCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._fetch
	
	@property
	def file_system(self) -> "FileSystemCDPExecutor":
		if self._file_system is None:
			from osn_selenium.executors.trio_threads.cdp.file_system import FileSystemCDPExecutor
			self._file_system = FileSystemCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._file_system
	
	@property
	def headless_experimental(self) -> "HeadlessExperimentalCDPExecutor":
		if self._headless_experimental is None:
			from osn_selenium.executors.trio_threads.cdp.headless_experimental import HeadlessExperimentalCDPExecutor
			self._headless_experimental = HeadlessExperimentalCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._headless_experimental
	
	@property
	def heap_profiler(self) -> "HeapProfilerCDPExecutor":
		if self._heap_profiler is None:
			from osn_selenium.executors.trio_threads.cdp.heap_profiler import HeapProfilerCDPExecutor
			self._heap_profiler = HeapProfilerCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._heap_profiler
	
	@property
	def indexed_db(self) -> "IndexedDbCDPExecutor":
		if self._indexed_db is None:
			from osn_selenium.executors.trio_threads.cdp.indexed_db import IndexedDbCDPExecutor
			self._indexed_db = IndexedDbCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._indexed_db
	
	@property
	def input(self) -> "InputCDPExecutor":
		if self._input is None:
			from osn_selenium.executors.trio_threads.cdp.input import InputCDPExecutor
			self._input = InputCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._input
	
	@property
	def inspector(self) -> "InspectorCDPExecutor":
		if self._inspector is None:
			from osn_selenium.executors.trio_threads.cdp.inspector import InspectorCDPExecutor
			self._inspector = InspectorCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._inspector
	
	@property
	def io(self) -> "IoCDPExecutor":
		if self._io is None:
			from osn_selenium.executors.trio_threads.cdp.io import IoCDPExecutor
			self._io = IoCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._io
	
	@property
	def layer_tree(self) -> "LayerTreeCDPExecutor":
		if self._layer_tree is None:
			from osn_selenium.executors.trio_threads.cdp.layer_tree import LayerTreeCDPExecutor
			self._layer_tree = LayerTreeCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._layer_tree
	
	@property
	def log(self) -> "LogCDPExecutor":
		if self._log is None:
			from osn_selenium.executors.trio_threads.cdp.log import LogCDPExecutor
			self._log = LogCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._log
	
	@property
	def media(self) -> "MediaCDPExecutor":
		if self._media is None:
			from osn_selenium.executors.trio_threads.cdp.media import MediaCDPExecutor
			self._media = MediaCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._media
	
	@property
	def memory(self) -> "MemoryCDPExecutor":
		if self._memory is None:
			from osn_selenium.executors.trio_threads.cdp.memory import MemoryCDPExecutor
			self._memory = MemoryCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._memory
	
	@property
	def network(self) -> "NetworkCDPExecutor":
		if self._network is None:
			from osn_selenium.executors.trio_threads.cdp.network import NetworkCDPExecutor
			self._network = NetworkCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._network
	
	@property
	def overlay(self) -> "OverlayCDPExecutor":
		if self._overlay is None:
			from osn_selenium.executors.trio_threads.cdp.overlay import OverlayCDPExecutor
			self._overlay = OverlayCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._overlay
	
	@property
	def page(self) -> "PageCDPExecutor":
		if self._page is None:
			from osn_selenium.executors.trio_threads.cdp.page import PageCDPExecutor
			self._page = PageCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._page
	
	@property
	def performance(self) -> "PerformanceCDPExecutor":
		if self._performance is None:
			from osn_selenium.executors.trio_threads.cdp.performance import PerformanceCDPExecutor
			self._performance = PerformanceCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._performance
	
	@property
	def performance_timeline(self) -> "PerformanceTimelineCDPExecutor":
		if self._performance_timeline is None:
			from osn_selenium.executors.trio_threads.cdp.performance_timeline import PerformanceTimelineCDPExecutor
			self._performance_timeline = PerformanceTimelineCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._performance_timeline
	
	@property
	def preload(self) -> "PreloadCDPExecutor":
		if self._preload is None:
			from osn_selenium.executors.trio_threads.cdp.preload import PreloadCDPExecutor
			self._preload = PreloadCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._preload
	
	@property
	def profiler(self) -> "ProfilerCDPExecutor":
		if self._profiler is None:
			from osn_selenium.executors.trio_threads.cdp.profiler import ProfilerCDPExecutor
			self._profiler = ProfilerCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._profiler
	
	@property
	def pwa(self) -> "PwaCDPExecutor":
		if self._pwa is None:
			from osn_selenium.executors.trio_threads.cdp.pwa import PwaCDPExecutor
			self._pwa = PwaCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._pwa
	
	@property
	def runtime(self) -> "RuntimeCDPExecutor":
		if self._runtime is None:
			from osn_selenium.executors.trio_threads.cdp.runtime import RuntimeCDPExecutor
			self._runtime = RuntimeCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._runtime
	
	@property
	def schema(self) -> "SchemaCDPExecutor":
		if self._schema is None:
			from osn_selenium.executors.trio_threads.cdp.schema import SchemaCDPExecutor
			self._schema = SchemaCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._schema
	
	@property
	def security(self) -> "SecurityCDPExecutor":
		if self._security is None:
			from osn_selenium.executors.trio_threads.cdp.security import SecurityCDPExecutor
			self._security = SecurityCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._security
	
	@property
	def service_worker(self) -> "ServiceWorkerCDPExecutor":
		if self._service_worker is None:
			from osn_selenium.executors.trio_threads.cdp.service_worker import ServiceWorkerCDPExecutor
			self._service_worker = ServiceWorkerCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._service_worker
	
	@property
	def storage(self) -> "StorageCDPExecutor":
		if self._storage is None:
			from osn_selenium.executors.trio_threads.cdp.storage import StorageCDPExecutor
			self._storage = StorageCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._storage
	
	@property
	def system_info(self) -> "SystemInfoCDPExecutor":
		if self._system_info is None:
			from osn_selenium.executors.trio_threads.cdp.system_info import SystemInfoCDPExecutor
			self._system_info = SystemInfoCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._system_info
	
	@property
	def target(self) -> "TargetCDPExecutor":
		if self._target is None:
			from osn_selenium.executors.trio_threads.cdp.target import TargetCDPExecutor
			self._target = TargetCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._target
	
	@property
	def tethering(self) -> "TetheringCDPExecutor":
		if self._tethering is None:
			from osn_selenium.executors.trio_threads.cdp.tethering import TetheringCDPExecutor
			self._tethering = TetheringCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._tethering
	
	@property
	def tracing(self) -> "TracingCDPExecutor":
		if self._tracing is None:
			from osn_selenium.executors.trio_threads.cdp.tracing import TracingCDPExecutor
			self._tracing = TracingCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._tracing
	
	@property
	def web_audio(self) -> "WebAudioCDPExecutor":
		if self._web_audio is None:
			from osn_selenium.executors.trio_threads.cdp.web_audio import WebAudioCDPExecutor
			self._web_audio = WebAudioCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._web_audio
	
	@property
	def web_authn(self) -> "WebAuthnCDPExecutor":
		if self._web_authn is None:
			from osn_selenium.executors.trio_threads.cdp.web_authn import WebAuthnCDPExecutor
			self._web_authn = WebAuthnCDPExecutor(
					execute_function=self._execute_function,
					lock=self._lock,
					limiter=self._capacity_limiter
			)
		
		return self._web_authn
