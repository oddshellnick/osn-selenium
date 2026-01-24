from osn_selenium.models import WindowRect
from typing import (
	Any,
	Dict,
	Optional,
	Union
)
from osn_selenium.flags.models.base import BrowserFlags
from osn_selenium.webdrivers._decorators import requires_driver
from selenium.webdriver.remote.remote_connection import RemoteConnection
from osn_selenium.exceptions.logic import (
	AbstractImplementationError
)
from selenium.webdriver.remote.webdriver import (
	WebDriver as legacyWebDriver
)
from osn_selenium.webdrivers.unified.core.settings import (
	UnifiedCoreSettingsMixin
)
from osn_selenium.webdrivers.unified.core.timeouts import (
	UnifiedCoreTimeoutsMixin
)


__all__ = ["UnifiedCoreLifecycleMixin"]


class UnifiedCoreLifecycleMixin(UnifiedCoreSettingsMixin, UnifiedCoreTimeoutsMixin):
	def _remote_connect_driver_impl(self, command_executor: Union[str, RemoteConnection]) -> None:
		self._driver = legacyWebDriver(
				command_executor=command_executor,
				options=self._webdriver_flags_manager.options,
		)
		
		self._set_driver_timeouts_impl(
				page_load_timeout=self._base_page_load_timeout,
				implicit_wait_timeout=self._base_implicitly_wait,
				script_timeout=self._base_script_timeout,
		)
		
		self._is_active = True
	
	def _create_driver_impl(self) -> None:
		raise AbstractImplementationError(method_name="_create_driver_impl", class_name=self.__class__.__name__)
	
	def _start_webdriver_impl(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		if self._driver_impl is None:
			self._update_settings_impl(flags=flags, window_rect=window_rect)
			self._create_driver_impl()
	
	@requires_driver
	def _quit_impl(self) -> None:
		self._driver_impl.quit()
	
	def _close_webdriver_impl(self) -> None:
		if self._driver_impl is not None:
			self._quit_impl()
		
		self._driver = None
		self._is_active = False
	
	def _restart_webdriver_impl(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		self._close_webdriver_impl()
		self._start_webdriver_impl(flags=flags, window_rect=window_rect)
	
	@requires_driver
	def _start_client_impl(self) -> None:
		self._driver_impl.start_client()
	
	@requires_driver
	def _start_session_impl(self, capabilities: Dict[str, Any]) -> None:
		self._driver_impl.start_session(capabilities=capabilities)
	
	@requires_driver
	def _stop_client_impl(self) -> None:
		self._driver_impl.stop_client()
