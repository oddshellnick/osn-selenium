import trio
from typing import Any, Callable, Self
from osn_selenium.instances.types import SCRIPT_TYPEHINT
from osn_selenium.base_mixin import TrioThreadMixin
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.abstract.instances.script import AbstractScript
from selenium.webdriver.common.bidi.script import (
	Script as legacyScript
)
from osn_selenium.instances.errors import (
	ExpectedTypeError,
	TypesConvertError
)


class Script(TrioThreadMixin, AbstractScript):
	"""
	Wrapper for the legacy Selenium BiDi Script instance.

	Facilitates execution of JavaScript within specific contexts, adding preload scripts,
	and handling console messages or JS errors.
	"""
	
	def __init__(
			self,
			selenium_script: legacyScript,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> None:
		"""
		Initializes the Script wrapper.

		Args:
			selenium_script (legacyScript): The legacy Selenium Script instance to wrap.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.
		"""
		
		super().__init__(lock=lock, limiter=limiter)
		
		if not isinstance(selenium_script, legacyScript):
			raise ExpectedTypeError(expected_class=legacyScript, received_instance=selenium_script)
		
		self._selenium_script = selenium_script
	
	async def add_console_message_handler(self, handler: Callable[[Any], None]) -> int:
		return await self._sync_to_trio(self.legacy.add_console_message_handler, handler=handler)
	
	async def add_javascript_error_handler(self, handler: Callable[[Any], None]) -> int:
		return await self._sync_to_trio(self.legacy.add_javascript_error_handler, handler=handler)
	
	async def execute(self, script: str, *args: Any) -> Any:
		return await self._sync_to_trio(self.legacy.execute, script, *args)
	
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
			raise TypesConvertError(from_=legacyScript, to_=selenium_script)
		
		return cls(selenium_script=legacy_script_obj, lock=lock, limiter=limiter)
	
	@property
	def legacy(self) -> legacyScript:
		return self._selenium_script
	
	async def pin(self, script: str) -> str:
		return await self._sync_to_trio(self.legacy.pin, script=script)
	
	async def remove_console_message_handler(self, id: int) -> None:
		await self._sync_to_trio(self.legacy.remove_console_message_handler, id=id)
	
	async def unpin(self, script_id: str) -> None:
		await self._sync_to_trio(self.legacy.unpin, script_id=script_id)
