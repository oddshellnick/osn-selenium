from typing import (
	List,
	Literal,
	Optional,
	Union
)
from osn_selenium.instances.sync.switch_to import SwitchTo
from osn_selenium.models import (
	Position,
	Rectangle,
	Size
)
from osn_selenium.instances.convert import (
	get_sync_instance_wrapper
)
from osn_selenium.webdrivers.unified.core.window import (
	UnifiedCoreWindowMixin
)
from osn_selenium.abstract.webdriver.core.window import (
	AbstractCoreWindowMixin
)


__all__ = ["CoreWindowMixin"]


class CoreWindowMixin(UnifiedCoreWindowMixin, AbstractCoreWindowMixin):
	"""
	Mixin for window and tab management in Core WebDrivers.

	Controls window dimensions, position, state (minimized/maximized), and
	switching between active window handles or frames.
	"""
	
	def close(self) -> None:
		self._close_impl()
	
	def close_all_windows(self) -> None:
		self._close_all_windows_impl()
	
	def close_window(self, window: Optional[Union[str, int]] = None) -> None:
		self._close_window_impl(window=window)
	
	def current_window_handle(self) -> str:
		return self._current_window_handle_impl()
	
	def fullscreen_window(self) -> None:
		self._fullscreen_window_impl()
	
	def get_window_handle(self, window: Optional[Union[str, int]] = None) -> str:
		return self._get_window_handle_impl(window=window)
	
	def get_window_position(self, windowHandle: str = "current") -> Position:
		position = self._get_window_position_impl(windowHandle=windowHandle)
		return Position.model_validate(position)
	
	def get_window_rect(self) -> Rectangle:
		rectangle = self._get_window_rect_impl()
		return Rectangle.model_validate(rectangle)
	
	def get_window_size(self, windowHandle: str = "current") -> Size:
		size = self._get_window_size_impl(windowHandle=windowHandle)
		return Size.model_validate(size)
	
	def maximize_window(self) -> None:
		self._maximize_window_impl()
	
	def minimize_window(self) -> None:
		self._minimize_window_impl()
	
	def orientation(self) -> Literal["LANDSCAPE", "PORTRAIT"]:
		return self._orientation_get_impl()
	
	def set_orientation(self, value: Literal["LANDSCAPE", "PORTRAIT"]) -> None:
		self._orientation_set_impl(value=value)
	
	def set_window_position(self, x: int, y: int, windowHandle: str = "current") -> Position:
		position = self._set_window_position_impl(x=x, y=y, windowHandle=windowHandle)
		return Position.model_validate(position)
	
	def set_window_rect(
			self,
			x: Optional[int] = None,
			y: Optional[int] = None,
			width: Optional[int] = None,
			height: Optional[int] = None,
	) -> Rectangle:
		rectangle = self._set_window_rect_impl(x=x, y=y, width=width, height=height)
		return Rectangle.model_validate(rectangle)
	
	def set_window_size(self, width: int, height: int, windowHandle: str = "current") -> None:
		self._set_window_size_impl(width=width, height=height, windowHandle=windowHandle)
	
	def switch_to(self) -> SwitchTo:
		legacy = self._switch_to_impl()
		return get_sync_instance_wrapper(wrapper_class=SwitchTo, legacy_object=legacy)
	
	def window_handles(self) -> List[str]:
		return self._window_handles_impl()
