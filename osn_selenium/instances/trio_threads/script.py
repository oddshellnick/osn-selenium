import trio
from typing import Any, Callable, Self
from osn_selenium.instances.types import SCRIPT_TYPEHINT
from osn_selenium.trio_base_mixin import _TrioThreadMixin
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.abstract.instances.script import AbstractScript
from selenium.webdriver.common.bidi.script import (
	Script as legacyScript
)


class Script(_TrioThreadMixin, AbstractScript):
	def __init__(
			self,
			selenium_script: legacyScript,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> None:
		super().__init__(lock=lock, limiter=limiter)
		
		if not isinstance(selenium_script, legacyScript):
			raise TypeError(f"Expected {type(legacyScript)}, got {type(selenium_script)}")
		
		self._selenium_script = selenium_script
	
	async def add_console_message_handler(self, handler: Callable[[Any], None]) -> int:
		return await self._wrap_to_trio(self.legacy.add_console_message_handler, handler=handler)
	
	async def add_javascript_error_handler(self, handler: Callable[[Any], None]) -> int:
		return await self._wrap_to_trio(self.legacy.add_javascript_error_handler, handler=handler)
	
	async def execute(self, script: str, *args: Any) -> Any:
		return await self._wrap_to_trio(self.legacy.execute, script, *args)
	
	@classmethod
	def from_legacy(
			cls,
			selenium_script: SCRIPT_TYPEHINT,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> Self:
		"""
		Creates an instance from a legacy Selenium Script object.

		This factory method is used to wrap an existing Selenium Script
		instance into the new interface.

		Args:
			selenium_script (SCRIPT_TYPEHINT): The legacy Selenium Script instance or its wrapper.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.

		Returns:
			Self: A new instance of a class implementing Script.
		"""
		
		legacy_script_obj = get_legacy_instance(selenium_script)
		
		if not isinstance(legacy_script_obj, legacyScript):
			raise TypeError(
					f"Could not convert input to {type(legacyScript)}: {type(selenium_script)}"
			)
		
		return cls(selenium_script=legacy_script_obj, lock=lock, limiter=limiter)
	
	@property
	def legacy(self) -> legacyScript:
		return self._selenium_script
	
	async def pin(self, script: str) -> str:
		return await self._wrap_to_trio(self.legacy.pin, script=script)
	
	async def remove_console_message_handler(self, id: int) -> None:
		await self._wrap_to_trio(self.legacy.remove_console_message_handler, id=id)
	
	async def unpin(self, script_id: str) -> None:
		await self._wrap_to_trio(self.legacy.unpin, script_id=script_id)
