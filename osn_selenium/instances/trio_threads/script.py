import trio
from typing import Any, Callable, Self
from osn_selenium.abstract.instances.script import AbstractScript
from osn_selenium.instances.trio_threads.base_mixin import _TrioThreadMixin
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
		
		self._selenium_script = selenium_script
	
	async def add_console_message_handler(self, handler: Callable[[Any], None],) -> int:
		return await self._wrap_to_trio(self.legacy.add_console_message_handler, handler=handler)
	
	async def add_javascript_error_handler(self, handler: Callable[[Any], None],) -> int:
		return await self._wrap_to_trio(self.legacy.add_javascript_error_handler, handler=handler)
	
	async def execute(self, script: str, *args: Any) -> Any:
		return await self._wrap_to_trio(self.legacy.execute, script, *args)
	
	@classmethod
	def from_legacy(
			cls,
			selenium_script: legacyScript,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> Self:
		"""
		Creates an instance from a legacy Selenium Script object.

		This factory method is used to wrap an existing Selenium Script
		instance into the new interface.

		Args:
			selenium_script (legacyScript): The legacy Selenium Script instance.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.

		Returns:
			Self: A new instance of a class implementing Script.
		"""
		
		return cls(selenium_script=selenium_script, lock=lock, limiter=limiter)
	
	@property
	def legacy(self) -> legacyScript:
		return self._selenium_script
	
	async def pin(self, script: str) -> str:
		return await self._wrap_to_trio(self.legacy.pin, script=script)
	
	async def remove_console_message_handler(self, id: int) -> None:
		await self._wrap_to_trio(self.legacy.remove_console_message_handler, id=id)
	
	async def unpin(self, script_id: str) -> None:
		await self._wrap_to_trio(self.legacy.unpin, script_id=script_id)
