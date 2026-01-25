from typing import (
	Any,
	List,
	Literal,
	Optional,
	Union
)
from osn_selenium.webdrivers._decorators import requires_driver
from selenium.common.exceptions import (
	InvalidSessionIdException
)
from osn_selenium.webdrivers.unified.core.base import UnifiedCoreBaseMixin
from osn_selenium.exceptions.window import (
	InvalidWindowHandleError,
	InvalidWindowIndexError,
	NoWindowHandlesFoundError
)


__all__ = ["UnifiedCoreWindowMixin"]


class UnifiedCoreWindowMixin(UnifiedCoreBaseMixin):
	@requires_driver
	def _window_handles_impl(self) -> List[str]:
		return self._driver_impl.window_handles
	
	@requires_driver
	def _close_impl(self) -> None:
		self._driver_impl.close()
	
	@requires_driver
	def _switch_to_impl(self) -> Any:
		return self._driver_impl.switch_to
	
	@requires_driver
	def _current_window_handle_impl(self) -> str:
		return self._driver_impl.current_window_handle
	
	def _get_window_handle_impl(self, window: Optional[Union[str, int]] = None) -> str:
		handles = self._window_handles_impl()
		
		if not handles:
			raise NoWindowHandlesFoundError()
		
		if isinstance(window, str):
			if window not in handles:
				raise InvalidWindowHandleError(handle=window)
		
			return window
		
		if isinstance(window, int):
			idx = window if window >= 0 else len(handles) + window
			if idx < 0 or idx >= len(handles):
				raise InvalidWindowIndexError(index=window, handles_length=len(handles))
			
			return handles[idx]
		
		return self._current_window_handle_impl()
	
	def _close_window_impl(self, window: Optional[Union[str, int]] = None) -> None:
		current = self._current_window_handle_impl()
		target = self._get_window_handle_impl(window)
		legacy_switch_to = self._switch_to_impl()
		
		if target == current:
			self._close_impl()
		
			try:
				remaining = self._window_handles_impl()
		
				if remaining:
					legacy_switch_to.window(remaining[-1])
			except InvalidSessionIdException:
				pass
		else:
			legacy_switch_to.window(target)
		
			self._close_impl()
		
			legacy_switch_to.window(current)
	
	def _close_all_windows_impl(self) -> None:
		for window_handle in reversed(self._window_handles_impl()):
			self._close_window_impl(window_handle)
	
	@requires_driver
	def _fullscreen_window_impl(self) -> None:
		self._driver_impl.fullscreen_window()
	
	@requires_driver
	def _get_window_position_impl(self, windowHandle: str = "current") -> Any:
		return self._driver_impl.get_window_position(windowHandle=windowHandle)
	
	@requires_driver
	def _get_window_rect_impl(self) -> Any:
		return self._driver_impl.get_window_rect()
	
	@requires_driver
	def _get_window_size_impl(self, windowHandle: str = "current") -> Any:
		return self._driver_impl.get_window_size(windowHandle=windowHandle)
	
	@requires_driver
	def _maximize_window_impl(self) -> None:
		self._driver_impl.maximize_window()
	
	@requires_driver
	def _minimize_window_impl(self) -> None:
		self._driver_impl.minimize_window()
	
	@requires_driver
	def _orientation_get_impl(self) -> Literal["LANDSCAPE", "PORTRAIT"]:
		return self._driver_impl.orientation["orientation"]
	
	@requires_driver
	def _orientation_set_impl(self, value: Literal["LANDSCAPE", "PORTRAIT"]) -> None:
		setattr(self._driver_impl, "orientation", value)
	
	@requires_driver
	def _set_window_position_impl(self, x: int, y: int, windowHandle: str = "current") -> Any:
		return self._driver_impl.set_window_position(x=x, y=y, windowHandle=windowHandle)
	
	@requires_driver
	def _set_window_rect_impl(
			self,
			x: Optional[int] = None,
			y: Optional[int] = None,
			width: Optional[int] = None,
			height: Optional[int] = None,
	) -> Any:
		return self._driver_impl.set_window_rect(x=x, y=y, width=width, height=height)
	
	@requires_driver
	def _set_window_size_impl(self, width: int, height: int, windowHandle: str = "current") -> None:
		self._driver_impl.set_window_size(width=width, height=height, windowHandle=windowHandle)
