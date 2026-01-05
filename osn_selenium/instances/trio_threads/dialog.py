import trio
from typing import List, Optional, Self

from osn_selenium.instances.errors import TypesConvertError, ExpectedTypeError
from osn_selenium.instances.types import DIALOG_TYPEHINT
from osn_selenium.trio_base_mixin import _TrioThreadMixin
from selenium.webdriver.common.fedcm.account import Account
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.abstract.instances.dialog import AbstractDialog
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
		
		if not isinstance(selenium_dialog, legacyDialog):
			raise ExpectedTypeError(expected_class=legacyDialog, received_instance=selenium_dialog)
		
		self._selenium_dialog = selenium_dialog
	
	async def accept(self) -> None:
		await self._wrap_to_trio(self.legacy.accept)
	
	async def dismiss(self) -> None:
		await self._wrap_to_trio(self.legacy.dismiss)
	
	@classmethod
	def from_legacy(
			cls,
			selenium_dialog: DIALOG_TYPEHINT,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> Self:
		"""
		Creates an instance from a legacy Selenium Dialog object.

		This factory method is used to wrap an existing Selenium Dialog
		instance into the new interface.

		Args:
			selenium_dialog (DIALOG_TYPEHINT): The legacy Selenium Dialog instance or its wrapper.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.

		Returns:
			Self: A new instance of a class implementing Dialog.
		"""
		
		legacy_dialog_obj = get_legacy_instance(selenium_dialog)
		
		if not isinstance(legacy_dialog_obj, legacyDialog):
			raise TypesConvertError(from_=legacyDialog, to_=selenium_dialog)
		
		return cls(selenium_dialog=legacy_dialog_obj, lock=lock, limiter=limiter)
	
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
