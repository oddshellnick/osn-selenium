import re
import trio
import pathlib
from subprocess import Popen
from typing import Optional, Union
from osn_selenium.types import WindowRect
from osn_selenium.flags.models.blink import BlinkFlags
from osn_windows_cmd.taskkill.parameters import TaskKillTypes
from osn_selenium.webdrivers.trio_threads.base import LifecycleMixin
from osn_windows_cmd.taskkill import (
	ProcessID,
	taskkill_windows
)
from osn_selenium.webdrivers.trio_threads.blink.settings import BlinkSettingsMixin
from osn_selenium.abstract.webdriver.blink.lifecycle import (
	AbstractBlinkLifecycleMixin
)
from osn_windows_cmd.netstat import (
	get_localhost_pids_with_addresses,
	get_localhost_pids_with_ports
)


class BlinkLifecycleMixin(BlinkSettingsMixin, LifecycleMixin, AbstractBlinkLifecycleMixin):
	async def _create_driver(self):
		raise NotImplementedError("This function must be implemented in child classes.")
	
	async def _check_browser_exe_active(self) -> bool:
		pids_with_addrs = await self._wrap_to_trio(
				get_localhost_pids_with_addresses,
				self._console_encoding,
				self._ip_pattern,
		)
		
		for pid, ports in pids_with_addrs.items():
			if len(ports) == 1 and re.search(rf":{self.debugging_port}\Z", ports[0]) is not None:
				address = re.search(rf"\A(.+):{self.debugging_port}\Z", ports[0]).group(1)
		
				if address != self.debugging_ip:
					await self._set_debugging_port(debugging_port=self.debugging_port, debugging_address=address,)
		
				return True
		
		return False
	
	async def start_webdriver(
			self,
			flags: Optional[BlinkFlags] = None,
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		if self.driver is None:
			await self.update_settings(
					flags=flags,
					browser_exe=browser_exe,
					browser_name_in_system=browser_name_in_system,
					use_browser_exe=use_browser_exe,
					start_page_url=start_page_url,
					window_rect=window_rect,
			)
		
			if self.browser_exe is not None:
				is_active = await self._check_browser_exe_active()
		
				if not is_active:
					await self._wrap_to_trio(Popen, args=self._webdriver_flags_manager.start_command, shell=True)
		
					while not is_active:
						is_active = await self._check_browser_exe_active()
		
						if not is_active:
							await trio.sleep(0.05)
		
			await self._create_driver()
		
			self._is_active = True
	
	async def close_webdriver(self) -> None:
		if self.browser_exe is not None:
			pids_to_ports = await self._wrap_to_trio(
					get_localhost_pids_with_ports,
					self._console_encoding,
					self._ip_pattern,
			)
		
			for pid, ports in pids_to_ports.items():
				if ports == [self.debugging_port]:
					await self._wrap_to_trio(
							taskkill_windows,
							taskkill_type=TaskKillTypes.forcefully_terminate,
							selectors=ProcessID(pid),
					)
		
					is_active = await self._check_browser_exe_active()
		
					while is_active:
						is_active = await self._check_browser_exe_active()
		
						if is_active:
							await trio.sleep(0.05)
		
		if self.driver is not None:
			await self.quit()
			self._driver = None
		
		self._is_active = False
	
	async def restart_webdriver(
			self,
			flags: Optional[BlinkFlags] = None,
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		await self.close_webdriver()
		await self.start_webdriver(
				flags=flags,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				start_page_url=start_page_url,
				window_rect=window_rect,
		)
