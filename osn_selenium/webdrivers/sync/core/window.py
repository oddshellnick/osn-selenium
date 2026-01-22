from typing import (
	List,
	Literal,
	Optional,
	Union
)
from selenium.common import (
	InvalidSessionIdException
)
from osn_selenium.instances.sync.switch_to import SwitchTo
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.types import (
	Position,
	Rectangle,
	Size
)
from osn_selenium.webdrivers.sync.core.base import CoreBaseMixin
from osn_selenium.instances.convert import (
	get_sync_instance_wrapper
)
from osn_selenium.abstract.webdriver.core.window import (
	AbstractCoreWindowMixin
)


class CoreWindowMixin(CoreBaseMixin, AbstractCoreWindowMixin):
	"""
	Mixin for window and tab management in Core WebDrivers.

	Controls window dimensions, position, state (minimized/maximized), and
	switching between active window handles or frames.
	"""
	
	def close_all_windows(self) -> None:
		for window_handle in reversed(self.window_handles()):
			self.close_window(window_handle)
	
	@requires_driver
	def fullscreen_window(self) -> None:
		self.driver.fullscreen_window()
	
	@requires_driver
	def get_window_position(self, windowHandle: str = "current") -> Position:
		position = self.driver.get_window_position(windowHandle=windowHandle)
		
		return Position.model_validate(position)
	
	@requires_driver
	def get_window_rect(self) -> Rectangle:
		rectangle = self.driver.get_window_rect()
		
		return Rectangle.model_validate(rectangle)
	
	@requires_driver
	def get_window_size(self, windowHandle: str = "current") -> Size:
		size = self.driver.get_window_size(windowHandle=windowHandle)
		
		return Size.model_validate(size)
	
	@requires_driver
	def maximize_window(self) -> None:
		self.driver.maximize_window()
	
	@requires_driver
	def minimize_window(self) -> None:
		self.driver.minimize_window()
	
	@requires_driver
	def orientation(self) -> Literal["LANDSCAPE", "PORTRAIT"]:
		return self.driver.orientation["orientation"]
	
	@requires_driver
	def set_orientation(self, value: Literal["LANDSCAPE", "PORTRAIT"]) -> None:
		setattr(self.driver, "orientation", value)
	
	@requires_driver
	def set_window_position(self, x: int, y: int, windowHandle: str = "current") -> Position:
		position = self.driver.set_window_position(x=x, y=y, windowHandle=windowHandle)
		
		return Position.model_validate(position)
	
	@requires_driver
	def set_window_rect(
			self,
			x: Optional[int] = None,
			y: Optional[int] = None,
			width: Optional[int] = None,
			height: Optional[int] = None,
	) -> Rectangle:
		rectangle = self.driver.set_window_rect(x=x, y=y, width=width, height=height)
		
		return Rectangle.model_validate(rectangle)
	
	@requires_driver
	def set_window_size(self, width: int, height: int, windowHandle: str = "current") -> None:
		self.driver.set_window_size(width=width, height=height, windowHandle=windowHandle)
	
	@requires_driver
	def window_handles(self) -> List[str]:
		return self.driver.window_handles
	
	@requires_driver
	def close(self) -> None:
		self.driver.close()
	
	@requires_driver
	def switch_to(self) -> SwitchTo:
		legacy = self.driver.switch_to
		
		return get_sync_instance_wrapper(wrapper_class=SwitchTo, legacy_object=legacy)
	
	@requires_driver
	def current_window_handle(self) -> str:
		return self.driver.current_window_handle
	
	def get_window_handle(self, window: Optional[Union[str, int]] = None) -> str:
		if isinstance(window, str):
			return window
		
		if isinstance(window, int):
			handles = self.window_handles()
		
			if not handles:
				raise RuntimeError("No window handles available")
		
			idx = window if window >= 0 else len(handles) + window
		
			if idx < 0 or idx >= len(handles):
				raise IndexError(f"Window index {window} out of range [0, {len(handles) - 1}]")
		
			return handles[idx]
		
		return self.current_window_handle()
	
	def close_window(self, window: Optional[Union[str, int]] = None) -> None:
		current = self.current_window_handle()
		target = self.get_window_handle(window)
		switch_to = self.switch_to()
		
		if target == current:
			self.close()
		
			try:
				remaining = self.window_handles()
		
				if remaining:
					switch_to.window(remaining[-1])
			except InvalidSessionIdException:
				pass
		else:
			switch_to.window(target)
			self.close()
			switch_to.window(current)
