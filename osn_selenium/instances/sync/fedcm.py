from typing import (
	Dict,
	List,
	Optional,
	Self
)
from osn_selenium.instances._typehints import FEDCM_TYPEHINT
from osn_selenium.instances.unified.fedcm import UnifiedFedCM
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.abstract.instances.fedcm import AbstractFedCM
from selenium.webdriver.remote.fedcm import FedCM as legacyFedCM
from osn_selenium.exceptions.instance import (
	CannotConvertTypeError
)


__all__ = ["FedCM"]


class FedCM(UnifiedFedCM, AbstractFedCM):
	"""
	Wrapper for the legacy Selenium FedCM instance.

	Provides an interface for controlling the Federated Credential Management API,
	including dialog delays and cooldown resets.
	"""
	
	def __init__(self, selenium_fedcm: legacyFedCM) -> None:
		"""
		Initializes the FedCM wrapper.

		Args:
			selenium_fedcm (legacyFedCM): The legacy Selenium FedCM instance to wrap.
		"""
		
		UnifiedFedCM.__init__(self, selenium_fedcm=selenium_fedcm)
	
	def accept(self) -> None:
		self._accept_impl()
	
	def account_list(self) -> List[Dict]:
		return self._account_list_impl()
	
	def dialog_type(self) -> str:
		return self._dialog_type_impl()
	
	def disable_delay(self) -> None:
		self._disable_delay_impl()
	
	def dismiss(self) -> None:
		self._dismiss_impl()
	
	def enable_delay(self) -> None:
		self._enable_delay_impl()
	
	@classmethod
	def from_legacy(cls, legacy_object: FEDCM_TYPEHINT) -> Self:
		"""
		Creates an instance from a legacy Selenium FedCM object.

		This factory method is used to wrap an existing Selenium FedCM
		instance into the new interface.

		Args:
			legacy_object (FEDCM_TYPEHINT): The legacy Selenium FedCM instance or its wrapper.

		Returns:
			Self: A new instance of a class implementing FedCM.
		"""
		
		legacy_fedcm_obj = get_legacy_instance(instance=legacy_object)
		
		if not isinstance(legacy_fedcm_obj, legacyFedCM):
			raise CannotConvertTypeError(from_=legacyFedCM, to_=legacy_object)
		
		return cls(selenium_fedcm=legacy_fedcm_obj)
	
	@property
	def legacy(self) -> legacyFedCM:
		return self._legacy_impl
	
	def reset_cooldown(self) -> None:
		self._reset_cooldown_impl()
	
	def select_account(self, index: int) -> None:
		self._select_account_impl(index=index)
	
	def subtitle(self) -> Optional[str]:
		return self._subtitle_impl()
	
	def title(self) -> str:
		return self._title_impl()
