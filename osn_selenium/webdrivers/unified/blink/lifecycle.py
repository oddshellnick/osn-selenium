import re
import time
from typing import Optional
from subprocess import Popen
from osn_selenium.models import WindowRect
from osn_selenium._typehints import PATH_TYPEHINT
from osn_selenium.flags.models.blink import BlinkFlags
from osn_system_utils.api.process import kill_process_by_pid
from osn_selenium.webdrivers.unified.blink.settings import (
	UnifiedBlinkSettingsMixin
)
from osn_selenium.webdrivers.unified.core.lifecycle import (
	UnifiedCoreLifecycleMixin
)
from osn_system_utils.api.network import (
	get_localhost_pids_with_addresses,
	get_localhost_pids_with_ports
)


__all__ = ["UnifiedBlinkLifecycleMixin"]


class UnifiedBlinkLifecycleMixin(UnifiedBlinkSettingsMixin, UnifiedCoreLifecycleMixin):
	def _create_driver_impl(self) -> None:
		raise NotImplementedError("This function must be implemented in child classes.")
	
	def _check_browser_exe_active_impl(self) -> bool:
		debugging_port = self._debugging_port_impl
		debugging_ip = self._debugging_ip_impl
		
		for pid, addresses in get_localhost_pids_with_addresses().items():
			for address_str in addresses:
				if re.search(rf":{debugging_port}\Z", address_str) is not None:
					found_ip = re.search(rf"\A(.+):{debugging_port}\Z", address_str).group(1)
		
					if found_ip != debugging_ip:
						self._set_debugging_port_impl(debugging_port=debugging_port, debugging_address=found_ip)
		
					return True
		return False
	
	def _start_webdriver_impl(
			self,
			flags: Optional[BlinkFlags] = None,
			browser_exe: Optional[PATH_TYPEHINT] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		if self._driver_impl is None:
			self._update_settings_impl(
					flags=flags,
					browser_exe=browser_exe,
					browser_name_in_system=browser_name_in_system,
					use_browser_exe=use_browser_exe,
					start_page_url=start_page_url,
					window_rect=window_rect,
			)
		
			if self._browser_exe_impl is not None:
				is_active = self._check_browser_exe_active_impl()
		
				if not is_active:
					Popen(args=self._webdriver_flags_manager.start_command, shell=True)
		
					while not is_active:
						is_active = self._check_browser_exe_active_impl()
						if not is_active:
							time.sleep(0.1)
		
			self._create_driver_impl()
			self._is_active = True
	
	def _close_webdriver_impl(self) -> None:
		if self._browser_exe_impl is not None:
			debugging_port = self._debugging_port_impl
			pids_with_ports = get_localhost_pids_with_ports()
		
			for pid, ports in pids_with_ports.items():
				if debugging_port in ports and 1 <= len(ports) <= 2:
					kill_process_by_pid(pid=pid, force=True)
		
					is_active = self._check_browser_exe_active_impl()
					while is_active:
						is_active = self._check_browser_exe_active_impl()
						if is_active:
							time.sleep(0.05)
		
		if self._driver_impl is not None:
			self._quit_impl()
			self._driver = None
		
		self._is_active = False
	
	def _restart_webdriver_impl(
			self,
			flags: Optional[BlinkFlags] = None,
			browser_exe: Optional[PATH_TYPEHINT] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		self._close_webdriver_impl()
		self._start_webdriver_impl(
				flags=flags,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				start_page_url=start_page_url,
				window_rect=window_rect
		)
