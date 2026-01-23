from typing import Optional
from abc import ABC, abstractmethod
from osn_selenium.models import WindowRect
from osn_selenium.flags.models.base import BrowserFlags


__all__ = ["AbstractCoreSettingsMixin"]


class AbstractCoreSettingsMixin(ABC):
	"""Mixin responsible for browser flags and settings."""
	
	@abstractmethod
	def reset_settings(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		"""
		Resets the WebDriver settings to a default or specified state.

		Args:
			flags (Optional[BrowserFlags]): Browser flags to reset to.
			window_rect (Optional[WindowRect]): Window dimensions to reset to.
		"""
		
		...
	
	@abstractmethod
	def update_settings(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		"""
		Updates the WebDriver settings with new flags or window dimensions.

		Args:
			flags (Optional[BrowserFlags]): Browser flags to add or update.
			window_rect (Optional[WindowRect]): New window dimensions and position.
		"""
		
		...
