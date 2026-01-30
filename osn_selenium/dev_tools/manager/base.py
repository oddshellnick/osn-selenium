import trio
from contextlib import (
	AbstractAsyncContextManager
)
from osn_selenium.dev_tools.target import DevToolsTarget
from osn_selenium.dev_tools.logger.main import MainLogger
from osn_selenium.dev_tools.domains import DomainsSettings
from osn_selenium.dev_tools._wrappers import DevToolsPackage
from osn_selenium.dev_tools.settings import DevToolsSettings
from typing import (
	Any,
	Dict,
	Optional,
	TYPE_CHECKING
)
from osn_selenium.dev_tools._system_utils import prepare_log_dir
from selenium.webdriver.remote.bidi_connection import BidiConnection
from osn_selenium.dev_tools.logger.models import (
	CDPLogLevelStats,
	CDPMainLogEntry,
	CDPTargetTypeStats,
	FingerprintAPIStats,
	FingerprintLogLevelStats,
	FingerprintMainLogEntry
)


__all__ = ["BaseMixin"]

if TYPE_CHECKING:
	from osn_selenium.webdrivers.trio_threads.core import CoreWebDriver


class BaseMixin:
	"""
	Base class for handling DevTools functionalities in Selenium WebDriver.

	Provides an interface to interact with Chrome DevTools Protocol (CDP)
	for advanced browser control and monitoring. This class supports event handling
	and allows for dynamic modifications of browser behavior, such as network request interception,
	by using an asynchronous context manager.

	Attributes:
		targets_lock (trio.Lock): A lock used for synchronizing access to shared resources, like the List of handled targets.
		exit_event (Optional[trio.Event]): Trio Event to signal exiting of DevTools event handling.
	"""
	
	def __init__(
			self,
			parent_webdriver: "CoreWebDriver",
			devtools_settings: Optional[DevToolsSettings] = None
	):
		"""
		Initializes the DevTools manager.

		Args:
			parent_webdriver (CoreWebDriver): The WebDriver instance to which this DevTools manager is attached.
			devtools_settings (Optional[DevToolsSettings]): Configuration settings for DevTools.
				If None, default settings will be used.
		"""
		
		if devtools_settings is None:
			devtools_settings = DevToolsSettings()
		
		self._webdriver = parent_webdriver
		self._logger_settings = devtools_settings.logger_settings
		self._domains_settings = devtools_settings.domains_settings
		self._fingerprint_settings = devtools_settings.fingerprint_settings
		self._new_targets_buffer_size = devtools_settings.new_targets_buffer_size
		self._target_background_task = devtools_settings.target_background_task
		
		self._new_targets_filter = [
			filter_.model_dump(exclude_none=True, by_alias=True)
			for filter_ in devtools_settings.new_targets_filter
		] if devtools_settings.new_targets_filter is not None else None
		
		self._bidi_connection: Optional[AbstractAsyncContextManager[BidiConnection, Any]] = None
		self._bidi_connection_object: Optional[BidiConnection] = None
		self._devtools_package: Optional[DevToolsPackage] = None
		self._websocket_url: Optional[str] = None
		self._nursery: Optional[AbstractAsyncContextManager[trio.Nursery, Optional[bool]]] = None
		self._nursery_object: Optional[trio.Nursery] = None
		self._handling_targets: Dict[str, DevToolsTarget] = {}
		self.targets_lock = trio.Lock()
		self.exit_event: Optional[trio.Event] = None
		self._is_active = False
		self._is_closing = False
		self._num_cdp_logs = 0
		self._num_fingerprint_logs = 0
		self._cdp_targets_types_stats: Dict[str, CDPTargetTypeStats] = {}
		self._cdp_log_level_stats: Dict[str, CDPLogLevelStats] = {}
		self._main_logger_cdp_send_channel: Optional[trio.MemorySendChannel[CDPMainLogEntry]] = None
		self._fingerprint_categories_stats: Dict[str, FingerprintAPIStats] = {}
		self._fingerprint_log_level_stats: Dict[str, FingerprintLogLevelStats] = {}
		self._main_logger_fingerprint_send_channel: Optional[trio.MemorySendChannel[FingerprintMainLogEntry]] = None
		self._main_logger: Optional[MainLogger] = None
		self._fingerprint_injection_script: Optional[str] = None
		
		prepare_log_dir(logger_settings=devtools_settings.logger_settings)
	
	@property
	def is_active(self) -> bool:
		"""
		Checks if DevTools is currently active.

		Returns:
			bool: True if DevTools event handler context manager is active, False otherwise.
		"""
		
		return self._is_active
	
	@property
	def websocket_url(self) -> Optional[str]:
		"""
		Gets the WebSocket URL for the DevTools session.

		This URL is used to establish a direct Chrome DevTools Protocol (CDP) connection
		to the browser, enabling low-level control and event listening.

		Returns:
			Optional[str]: The WebSocket URL, or None if it has not been retrieved yet.
		"""
		
		return self._websocket_url
