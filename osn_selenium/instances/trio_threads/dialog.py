import trio
from typing import List, Optional, Self
from osn_selenium.trio_threads_mixin import TrioThreadMixin
from selenium.webdriver.common.fedcm.account import Account
from osn_selenium.instances._typehints import DIALOG_TYPEHINT
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.instances.unified.dialog import UnifiedDialog
from osn_selenium.abstract.instances.dialog import AbstractDialog
from osn_selenium.exceptions.instance import (
	CannotConvertTypeError
)
from selenium.webdriver.common.fedcm.dialog import (
	Dialog as legacyDialog
)


__all__ = ["Dialog"]


class Dialog(UnifiedDialog, TrioThreadMixin, AbstractDialog):
	"""
	Wrapper for the legacy Selenium FedCM Dialog instance.

	Handles Federated Credential Management dialogs, including account selection
	and dismissal.
	"""
	
	def __init__(
			self,
			selenium_dialog: legacyDialog,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> None:
		"""
		Initializes the Dialog wrapper.

		Args:
			selenium_dialog (legacyDialog): The legacy Selenium Dialog instance to wrap.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.
		"""
		
		UnifiedDialog.__init__(self, selenium_dialog=selenium_dialog)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def accept(self) -> None:
		await self.sync_to_trio(sync_function=self._accept_impl)()
	
	async def dismiss(self) -> None:
		await self.sync_to_trio(sync_function=self._dismiss_impl)()
	
	@classmethod
	def from_legacy(
			cls,
			legacy_object: DIALOG_TYPEHINT,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> Self:
		"""
		Creates an instance from a legacy Selenium Dialog object.

		This factory method is used to wrap an existing Selenium Dialog
		instance into the new interface.

		Args:
			legacy_object (DIALOG_TYPEHINT): The legacy Selenium Dialog instance or its wrapper.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.

		Returns:
			Self: A new instance of a class implementing Dialog.
		"""
		
		legacy_dialog_obj = get_legacy_instance(instance=legacy_object)
		
		if not isinstance(legacy_dialog_obj, legacyDialog):
			raise CannotConvertTypeError(from_=legacyDialog, to_=legacy_object)
		
		return cls(selenium_dialog=legacy_dialog_obj, lock=lock, limiter=limiter)
	
	async def get_accounts(self) -> List[Account]:
		return await self.sync_to_trio(sync_function=self._get_accounts_impl)()
	
	@property
	def legacy(self) -> legacyDialog:
		return self._legacy_impl
	
	async def select_account(self, index: int) -> None:
		await self.sync_to_trio(sync_function=self._select_account_impl)(index=index)
	
	async def subtitle(self) -> Optional[str]:
		return await self.sync_to_trio(sync_function=self._subtitle_impl)()
	
	async def title(self) -> str:
		return await self.sync_to_trio(sync_function=self._title_impl)()
	
	async def type(self) -> Optional[str]:
		return await self.sync_to_trio(sync_function=self._type_impl)()
