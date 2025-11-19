import trio
from typing import List, Optional, Self
from selenium.webdriver.common.fedcm.account import Account
from osn_selenium.abstract.instances.dialog import AbstractDialog
from osn_selenium.instances.trio_threads.base_mixin import _TrioThreadMixin
from selenium.webdriver.common.fedcm.dialog import (
	Dialog as legacyDialog
)


class Dialog(_TrioThreadMixin, AbstractDialog):
	def __init__(
			self,
			selenium_dialog: legacyDialog,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> None:
		super().__init__(lock=lock, limiter=limiter)
		
		self._selenium_dialog = selenium_dialog
	
	async def accept(self) -> None:
		await self._wrap_to_trio(self.legacy.accept)
	
	async def dismiss(self) -> None:
		await self._wrap_to_trio(self.legacy.dismiss)
	
	@classmethod
	def from_legacy(
			cls,
			selenium_dialog: legacyDialog,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> Self:
		"""
		Creates an instance from a legacy Selenium Dialog object.

		This factory method is used to wrap an existing Selenium Dialog
		instance into the new interface.

		Args:
			selenium_dialog (legacyDialog): The legacy Selenium Dialog instance.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.

		Returns:
			Self: A new instance of a class implementing Dialog.
		"""
		
		return cls(selenium_dialog=selenium_dialog, lock=lock, limiter=limiter)
	
	async def get_accounts(self) -> List[Account]:
		return await self._wrap_to_trio(self.legacy.get_accounts)
	
	@property
	def legacy(self) -> legacyDialog:
		return self._selenium_dialog
	
	async def select_account(self, index: int) -> None:
		await self._wrap_to_trio(self.legacy.select_account, index=index)
	
	async def subtitle(self) -> Optional[str]:
		return await self._wrap_to_trio(lambda: self.legacy.subtitle)
	
	async def title(self) -> str:
		return await self._wrap_to_trio(lambda: self.legacy.title)
	
	async def type(self) -> Optional[str]:
		return await self._wrap_to_trio(lambda: self.legacy.type)
