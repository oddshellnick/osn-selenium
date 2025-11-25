from typing import (
	Dict,
	List,
	Optional,
	Self
)
from osn_selenium.instances.types import FEDCM_TYPEHINT
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.abstract.instances.fedcm import AbstractFedCM
from selenium.webdriver.remote.fedcm import FedCM as legacyFedCM


class FedCM(AbstractFedCM):
	def __init__(self, selenium_fedcm: legacyFedCM) -> None:
		if not isinstance(selenium_fedcm, legacyFedCM):
			raise TypeError(f"Expected {type(legacyFedCM)}, got {type(selenium_fedcm)}")
		
		self._selenium_fedcm = selenium_fedcm
	
	def accept(self) -> None:
		self.legacy.accept()
	
	def account_list(self) -> List[Dict]:
		return self.legacy.account_list
	
	def dialog_type(self) -> str:
		return self.legacy.dialog_type
	
	def disable_delay(self) -> None:
		self.legacy.disable_delay()
	
	def dismiss(self) -> None:
		self.legacy.dismiss()
	
	def enable_delay(self) -> None:
		self.legacy.enable_delay()
	
	@classmethod
	def from_legacy(cls, selenium_fedcm: FEDCM_TYPEHINT) -> Self:
		legacy_fedcm_obj = get_legacy_instance(selenium_fedcm)
		
		if not isinstance(legacy_fedcm_obj, legacyFedCM):
			raise TypeError(
					f"Could not convert input to {type(legacyFedCM)}: {type(selenium_fedcm)}"
			)
		
		return cls(selenium_fedcm=legacy_fedcm_obj)
	
	@property
	def legacy(self) -> legacyFedCM:
		return self._selenium_fedcm
	
	def reset_cooldown(self) -> None:
		self.legacy.reset_cooldown()
	
	def select_account(self, index: int) -> None:
		self.legacy.select_account(index=index)
	
	def subtitle(self) -> Optional[str]:
		return self.legacy.subtitle
	
	def title(self) -> str:
		return self.legacy.title
