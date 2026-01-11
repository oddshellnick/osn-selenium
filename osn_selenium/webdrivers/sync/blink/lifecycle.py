import re
import time
import pathlib
from subprocess import Popen
from typing import Optional, Union
from osn_selenium.types import WindowRect
from osn_selenium.flags.models.blink import BlinkFlags
from osn_system_utils.api.process import kill_process_by_pid
from osn_selenium.webdrivers.sync.core import CoreLifecycleMixin
from osn_selenium.webdrivers.sync.blink.settings import BlinkSettingsMixin
from osn_selenium.abstract.webdriver.blink.lifecycle import (
	AbstractBlinkLifecycleMixin
)
from osn_system_utils.api.network import (
	get_localhost_pids_with_addresses,
	get_localhost_pids_with_ports
)


class BlinkLifecycleMixin(BlinkSettingsMixin, CoreLifecycleMixin, AbstractBlinkLifecycleMixin):
	"""
	Mixin for managing the lifecycle of the Blink WebDriver.

	Handles the creation, startup, shutdown, and restarting processes of the
	underlying browser instance, ensuring clean session management.
	"""
	
	def _create_driver(self):
		raise NotImplementedError("This function must be implemented in child classes.")
	
	def _check_browser_exe_active(self) -> bool:
		for pid, ports in get_localhost_pids_with_addresses().items():
			if len(ports) == 1 and re.search(rf":{self.debugging_port}\Z", ports[0]) is not None:
				address = re.search(rf"\A(.+):{self.debugging_port}\Z", ports[0]).group(1)
		
				if address != self.debugging_ip:
					self._set_debugging_port(
							debugging_port=self.debugging_port,
							debugging_address=re.search(rf"\A(.+):{self.debugging_port}\Z", ports[0]).group(1)
					)
		
				return True
		
		return False
	
	def start_webdriver(
			self,
			flags: Optional[BlinkFlags] = None,
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	):
		if self.driver is None:
			self.update_settings(
					flags=flags,
					browser_exe=browser_exe,
					browser_name_in_system=browser_name_in_system,
					use_browser_exe=use_browser_exe,
					start_page_url=start_page_url,
					window_rect=window_rect,
			)
		
			if self.browser_exe is not None:
				is_active = self._check_browser_exe_active()
		
				if not is_active:
					Popen(args=self._webdriver_flags_manager.start_command, shell=True)
		
					while not is_active:
						is_active = self._check_browser_exe_active()
		
			self._create_driver()
		
			self._is_active = True
	
	def close_webdriver(self):
		if self.browser_exe is not None:
			pids_with_ports = get_localhost_pids_with_ports()
		
			for pid, ports in pids_with_ports.items():
				if self.debugging_port in ports and 1 <= len(ports) <= 2:
					kill_process_by_pid(pid=pid, force=True)
		
					is_active = self._check_browser_exe_active()
		
					while is_active:
						is_active = self._check_browser_exe_active()
		
						if is_active:
							time.sleep(0.05)
		
		if self.driver is not None:
			self.driver.quit()
			self._driver = None
		
		self._is_active = False
	
	def restart_webdriver(
			self,
			flags: Optional[BlinkFlags] = None,
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	):
		self.close_webdriver()
		self.start_webdriver(
				flags=flags,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				start_page_url=start_page_url,
		)
