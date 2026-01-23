from abc import ABC, abstractmethod
from osn_selenium.abstract.instances.dialog import AbstractDialog
from osn_selenium.abstract.instances.mobile import AbstractMobile
from osn_selenium.abstract.instances.browser import AbstractBrowser
from osn_selenium.abstract.instances.permissions import AbstractPermissions
from osn_selenium.abstract.instances.web_extension import AbstractWebExtension
from osn_selenium.abstract.instances.browsing_context import (
	AbstractBrowsingContext
)


__all__ = ["AbstractCoreComponentsMixin"]


class AbstractCoreComponentsMixin(ABC):
	"""Mixin responsible for accessing various sub-components of the browser."""
	
	@abstractmethod
	def browser(self) -> AbstractBrowser:
		"""
		Provides access to browser-level actions.

		Returns:
			AbstractBrowser: An object for controlling browser-level features.
		"""
		
		...
	
	@abstractmethod
	def browsing_context(self) -> AbstractBrowsingContext:
		"""
		Provides access to the browsing context interface (e.g., tabs, windows).

		Returns:
			AbstractBrowsingContext: An object for managing browsing contexts.
		"""
		
		...
	
	@abstractmethod
	def dialog(self) -> AbstractDialog:
		"""
		Provides access to the dialog (alert, prompt, confirm) interface.

		Returns:
			AbstractDialog: An object for interacting with browser dialogs.
		"""
		
		...
	
	@abstractmethod
	def mobile(self) -> AbstractMobile:
		"""
		Provides access to mobile-specific functionality.

		Returns:
			AbstractMobile: An object for mobile-specific interactions.
		"""
		
		...
	
	@abstractmethod
	def permissions(self) -> AbstractPermissions:
		"""
		Provides access to the permissions management interface.

		Returns:
			AbstractPermissions: An object for managing browser permissions.
		"""
		
		...
	
	@abstractmethod
	def webextension(self) -> AbstractWebExtension:
		"""
		Provides access to the web extension management interface.

		Returns:
			AbstractWebExtension: An object to manage browser extensions.
		"""
		
		...
