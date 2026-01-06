from typing import (
	List,
	Literal,
	Optional,
	Union
)
from selenium.common import (
	InvalidSessionIdException
)
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.types import (
	Position,
	Rectangle,
	Size
)
from osn_selenium.instances.trio_threads.switch_to import SwitchTo
from osn_selenium.webdrivers.trio_threads.base.base import BaseMixin
from osn_selenium.abstract.webdriver.base.window import AbstractWindowMixin


class WindowMixin(BaseMixin, AbstractWindowMixin):
	async def close_all_windows(self) -> None:
		for window_handle in reversed(await self.window_handles()):
			await self.close_window(window_handle)
	
	@requires_driver
	async def fullscreen_window(self) -> None:
		await self._wrap_to_trio(self.driver.fullscreen_window)
	
	@requires_driver
	async def get_window_position(self, windowHandle: str = "current") -> Position:
		position = await self._wrap_to_trio(self.driver.get_window_position, windowHandle=windowHandle)
		
		return Position.model_validate(position)
	
	@requires_driver
	async def get_window_rect(self) -> Rectangle:
		rectangle = await self._wrap_to_trio(self.driver.get_window_rect)
		
		return Rectangle.model_validate(rectangle)
	
	@requires_driver
	async def get_window_size(self, windowHandle: str = "current") -> Size:
		size = await self._wrap_to_trio(self.driver.get_window_size, windowHandle=windowHandle)
		
		return Size.model_validate(size)
	
	@requires_driver
	async def maximize_window(self) -> None:
		await self._wrap_to_trio(self.driver.maximize_window)
	
	@requires_driver
	async def minimize_window(self) -> None:
		await self._wrap_to_trio(self.driver.minimize_window)
	
	@requires_driver
	async def orientation(self) -> Literal["LANDSCAPE", "PORTRAIT"]:
		return (await self._wrap_to_trio(lambda: self.driver.orientation))["orientation"]
	
	@requires_driver
	async def set_orientation(self, value: Literal["LANDSCAPE", "PORTRAIT"]) -> None:
		await self._wrap_to_trio(lambda: setattr(self.driver, "orientation", value))
	
	@requires_driver
	async def set_window_position(self, x: int, y: int, windowHandle: str = "current") -> Position:
		position = await self._wrap_to_trio(self.driver.set_window_position, x=x, y=y, windowHandle=windowHandle)
		
		return Position.model_validate(position)
	
	@requires_driver
	async def set_window_rect(
			self,
			x: Optional[int] = None,
			y: Optional[int] = None,
			width: Optional[int] = None,
			height: Optional[int] = None,
	) -> Rectangle:
		rectangle = await self._wrap_to_trio(self.driver.set_window_rect, x=x, y=y, width=width, height=height)
		
		return Rectangle.model_validate(rectangle)
	
	@requires_driver
	async def set_window_size(self, width: int, height: int, windowHandle: str = "current") -> None:
		await self._wrap_to_trio(
				self.driver.set_window_size,
				width=width,
				height=height,
				windowHandle=windowHandle,
		)
	
	@requires_driver
	async def window_handles(self) -> List[str]:
		return await self._wrap_to_trio(lambda: self.driver.window_handles)
	
	@requires_driver
	async def close(self) -> None:
		await self._wrap_to_trio(self.driver.close)
	
	@requires_driver
	async def switch_to(self) -> SwitchTo:
		legacy = await self._wrap_to_trio(lambda: self.driver.switch_to)
		
		return SwitchTo(
				selenium_switch_to=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	@requires_driver
	async def current_window_handle(self) -> str:
		return await self._wrap_to_trio(lambda: self.driver.current_window_handle)
	
	async def get_window_handle(self, window: Optional[Union[str, int]] = None) -> str:
		if isinstance(window, str):
			return window
		
		if isinstance(window, int):
			handles = await self.window_handles()
		
			if not handles:
				raise RuntimeError("No window handles available")
		
			idx = window if window >= 0 else len(handles) + window
		
			if idx < 0 or idx >= len(handles):
				raise IndexError(f"Window index {window} out of range [0, {len(handles) - 1}]")
		
			return handles[idx]
		
		return await self.current_window_handle()
	
	async def close_window(self, window: Optional[Union[str, int]] = None) -> None:
		current = await self.current_window_handle()
		target = await self.get_window_handle(window)
		switch_to = await self.switch_to()
		
		if target == current:
			await self.close()
		
			try:
				remaining = await self.window_handles()
		
				if remaining:
					await switch_to.window(remaining[-1])
			except InvalidSessionIdException:
				pass
		else:
			await switch_to.window(target)
			await self.close()
			await switch_to.window(current)
