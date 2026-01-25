from typing import Sequence, Union
from osn_selenium.dev_tools.manager.base import BaseMixin
from osn_selenium.dev_tools._decorators import warn_if_active
from osn_selenium.exceptions.configuration import NotExpectedTypeError
from osn_selenium.dev_tools.domains import (
	DomainsSettings,
	domains_classes_type,
	domains_type
)


__all__ = ["SettingsMixin"]


class SettingsMixin(BaseMixin):
	"""
	Mixin for managing DevTools domain settings (handlers and configurations).
	"""
	
	@warn_if_active
	def _remove_handler_settings(self, domain: domains_type):
		"""
		Removes the settings for a specific domain.

		This is an internal method intended to be used only when the DevTools context is not active.
		It uses the `@warn_if_active` decorator to log a warning if called incorrectly.

		Args:
			domain (domains_type): The name of the domain to remove settings for.
		"""
		
		if self._domains_settings is not None:
			self._domains_settings.pop(domain, None)
	
	def remove_domains_handlers(self, domains: Union[domains_type, Sequence[domains_type]]):
		"""
		Removes handler settings for one or more DevTools domains.

		This method can be called with a single domain name or a sequence of domain names.
		It should only be called when the DevTools context is not active.

		Args:
			domains (Union[domains_type, Sequence[domains_type]]): A single domain name as a string,
				or a sequence of domain names to be removed.

		Raises:
			TypeError: If the `domains` argument is not a string or a sequence of strings.
		"""
		
		if isinstance(domains, str):
			self._remove_handler_settings(domains)
		elif isinstance(domains, Sequence) and all(isinstance(domain, str) for domain in domains):
			for domain in domains:
				self._remove_handler_settings(domain)
		else:
			raise NotExpectedTypeError(
					value_name="domains",
					value=domains,
					valid_types=("str", "Sequence[str]")
			)
	
	@warn_if_active
	def _set_handler_settings(self, domain: domains_type, settings: domains_classes_type):
		"""
		Sets the handler settings for a specific domain.

		This is an internal method intended to be used only when the DevTools context is not active.
		It uses the `@warn_if_active` decorator to log a warning if called incorrectly.

		Args:
			domain (domains_type): The name of the domain to configure.
			settings (domains_classes_type): The configuration settings for the domain.
		"""
		
		setattr(self._domains_settings, domain, settings)
	
	def set_domains_handlers(self, settings: DomainsSettings):
		"""
		Sets handler settings for multiple domains from a DomainsSettings object.

		This method iterates through the provided settings and applies them to the corresponding domains.
		It should only be called when the DevTools context is not active.

		Args:
			settings (DomainsSettings): An object containing the configuration for one or more domains.
		"""
		
		for domain_name, domain_settings in settings.model_dump(exclude_none=True).items():
			self._set_handler_settings(domain_name, domain_settings)
