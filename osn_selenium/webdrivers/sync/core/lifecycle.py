from osn_selenium.models import WindowRect
from typing import (
	Any,
	Dict,
	Optional,
	Union
)
from osn_selenium.flags.models.base import BrowserFlags
from selenium.webdriver.remote.remote_connection import RemoteConnection
from osn_selenium.webdrivers.unified.core.lifecycle import (
	UnifiedCoreLifecycleMixin
)
from osn_selenium.abstract.webdriver.core.lifecycle import (
	AbstractCoreLifecycleMixin
)


__all__ = ["CoreLifecycleMixin"]


class CoreLifecycleMixin(UnifiedCoreLifecycleMixin, AbstractCoreLifecycleMixin):
	"""
	Mixin for managing the lifecycle of the Core WebDriver.

	Handles the creation, startup, shutdown, and restarting processes of the
	underlying browser instance, ensuring clean session management.
	"""
	
	def close_webdriver(self) -> None:
		self._close_webdriver_impl()
	
	def quit(self) -> None:
		self._quit_impl()
	
	def remote_connect_driver(self, command_executor: Union[str, RemoteConnection]) -> None:
		self._remote_connect_driver_impl(command_executor=command_executor)
	
	def restart_webdriver(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		self._restart_webdriver_impl(flags=flags, window_rect=window_rect)
	
	def start_client(self) -> None:
		self._start_client_impl()
	
	def start_session(self, capabilities: Dict[str, Any]) -> None:
		self._start_session_impl(capabilities=capabilities)
	
	def start_webdriver(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		self._start_webdriver_impl(flags=flags, window_rect=window_rect)
	
	def stop_client(self) -> None:
		self._stop_client_impl()
