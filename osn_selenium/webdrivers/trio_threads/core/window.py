from osn_selenium.trio_threads_mixin import TrioThreadMixin
from typing import (
	List,
	Literal,
	Optional,
	Union
)
from osn_selenium.models import (
	Position,
	Rectangle,
	Size
)
from osn_selenium.instances.trio_threads.switch_to import SwitchTo
from osn_selenium.instances.convert import (
	get_trio_thread_instance_wrapper
)
from osn_selenium.webdrivers.unified.core.window import (
	UnifiedCoreWindowMixin
)
from osn_selenium.abstract.webdriver.core.window import (
	AbstractCoreWindowMixin
)


__all__ = ["CoreWindowMixin"]


class CoreWindowMixin(UnifiedCoreWindowMixin, TrioThreadMixin, AbstractCoreWindowMixin):
	"""
	Mixin for window and tab management in Core WebDrivers.

	Controls window dimensions, position, state (minimized/maximized), and
	switching between active window handles or frames.
	"""
	
	async def close(self) -> None:
		await self.sync_to_trio(sync_function=self._close_impl)()
	
	async def close_all_windows(self) -> None:
		await self.sync_to_trio(sync_function=self._close_all_windows_impl)()
	
	async def close_window(self, window: Optional[Union[str, int]] = None) -> None:
		await self.sync_to_trio(sync_function=self._close_window_impl)(window=window)
	
	async def current_window_handle(self) -> str:
		return await self.sync_to_trio(sync_function=self._current_window_handle_impl)()
	
	async def fullscreen_window(self) -> None:
		await self.sync_to_trio(sync_function=self._fullscreen_window_impl)()
	
	async def get_window_handle(self, window: Optional[Union[str, int]] = None) -> str:
		return await self.sync_to_trio(sync_function=self._get_window_handle_impl)(window=window)
	
	async def get_window_position(self, windowHandle: str = "current") -> Position:
		position = await self.sync_to_trio(sync_function=self._get_window_position_impl)(windowHandle=windowHandle)
		return Position.model_validate(position)
	
	async def get_window_rect(self) -> Rectangle:
		rectangle = await self.sync_to_trio(sync_function=self._get_window_rect_impl)()
		return Rectangle.model_validate(rectangle)
	
	async def get_window_size(self, windowHandle: str = "current") -> Size:
		size = await self.sync_to_trio(sync_function=self._get_window_size_impl)(windowHandle=windowHandle)
		return Size.model_validate(size)
	
	async def maximize_window(self) -> None:
		await self.sync_to_trio(sync_function=self._maximize_window_impl)()
	
	async def minimize_window(self) -> None:
		await self.sync_to_trio(sync_function=self._minimize_window_impl)()
	
	async def orientation(self) -> Literal["LANDSCAPE", "PORTRAIT"]:
		return await self.sync_to_trio(sync_function=self._orientation_get_impl)()
	
	async def set_orientation(self, value: Literal["LANDSCAPE", "PORTRAIT"]) -> None:
		await self.sync_to_trio(sync_function=self._orientation_set_impl)(value=value)
	
	async def set_window_position(self, x: int, y: int, windowHandle: str = "current") -> Position:
		position = await self.sync_to_trio(sync_function=self._set_window_position_impl)(x=x, y=y, windowHandle=windowHandle)
		return Position.model_validate(position)
	
	async def set_window_rect(
			self,
			x: Optional[int] = None,
			y: Optional[int] = None,
			width: Optional[int] = None,
			height: Optional[int] = None,
	) -> Rectangle:
		rectangle = await self.sync_to_trio(sync_function=self._set_window_rect_impl)(x=x, y=y, width=width, height=height)
		return Rectangle.model_validate(rectangle)
	
	async def set_window_size(self, width: int, height: int, windowHandle: str = "current") -> None:
		await self.sync_to_trio(sync_function=self._set_window_size_impl)(width=width, height=height, windowHandle=windowHandle)
	
	def switch_to(self) -> SwitchTo:
		legacy = self._switch_to_impl()
		return get_trio_thread_instance_wrapper(
				wrapper_class=SwitchTo,
				legacy_object=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	async def window_handles(self) -> List[str]:
		return await self.sync_to_trio(sync_function=self._window_handles_impl)()
