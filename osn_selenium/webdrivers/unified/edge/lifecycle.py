from typing import Optional
from selenium import webdriver
from osn_selenium.models import WindowRect
from osn_selenium._typehints import PATH_TYPEHINT
from selenium.webdriver.edge.service import Service
from osn_selenium.flags.models.edge import EdgeFlags
from osn_selenium.webdrivers.unified.core.window import (
	UnifiedCoreWindowMixin
)
from osn_selenium.webdrivers.unified.core.timeouts import (
	UnifiedCoreTimeoutsMixin
)
from osn_selenium.webdrivers.unified.blink.lifecycle import (
	UnifiedBlinkLifecycleMixin
)


__all__ = ["UnifiedEdgeLifecycleMixin"]


class UnifiedEdgeLifecycleMixin(
		UnifiedBlinkLifecycleMixin,
		UnifiedCoreTimeoutsMixin,
		UnifiedCoreWindowMixin
):
	def _create_driver_impl(self) -> None:
		webdriver_options = self._webdriver_flags_manager.options
		webdriver_service = Service(
				executable_path=self._webdriver_path,
				port=self._debugging_port_impl
				if self._browser_exe_impl is None
				else 0,
				service_args=self._webdriver_flags_manager.start_args
				if self._browser_exe_impl is None
				else None
		)
		
		self._driver = webdriver.Edge(options=webdriver_options, service=webdriver_service)
		
		if self._window_rect is not None:
			self._set_window_rect_impl(
					x=self._window_rect.x,
					y=self._window_rect.y,
					width=self._window_rect.width,
					height=self._window_rect.height,
			)
		
		self._set_driver_timeouts_impl(
				page_load_timeout=self._base_page_load_timeout,
				implicit_wait_timeout=self._base_implicitly_wait,
				script_timeout=self._base_implicitly_wait,
		)
	
	def _restart_webdriver_impl(
			self,
			flags: Optional[EdgeFlags] = None,
			browser_exe: Optional[PATH_TYPEHINT] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		super()._restart_webdriver_impl(
				flags=flags,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				start_page_url=start_page_url,
				window_rect=window_rect,
		)
	
	def _start_webdriver_impl(
			self,
			flags: Optional[EdgeFlags] = None,
			browser_exe: Optional[PATH_TYPEHINT] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		super()._start_webdriver_impl(
				flags=flags,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				start_page_url=start_page_url,
				window_rect=window_rect,
		)
