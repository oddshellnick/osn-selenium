from typing_extensions import deprecated
from osn_selenium.trio_bidi.mixin import TrioBiDiMixin
from typing import (
	List,
	Literal,
	Optional,
	Union
)
from osn_selenium.instances.trio_bidi.switch_to import SwitchTo
from osn_selenium.models import (
	Position,
	Rectangle,
	Size
)
from osn_selenium.instances.convert import (
	get_trio_bidi_instance_wrapper
)
from osn_selenium.webdrivers.unified.core.window import (
	UnifiedCoreWindowMixin
)
from osn_selenium.abstract.webdriver.core.window import (
	AbstractCoreWindowMixin
)
from osn_selenium.exceptions.experimental import (
	NotImplementedExperimentalFeatureError
)


__all__ = ["CoreWindowMixin"]


class CoreWindowMixin(UnifiedCoreWindowMixin, TrioBiDiMixin, AbstractCoreWindowMixin):
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
	
	@deprecated(
			"This method is currently not supported. It will raise 'NotImplementedExperimentalFeatureError' on call."
	)
	async def fullscreen_window(self) -> None:
		raise NotImplementedExperimentalFeatureError(name="CoreWindowMixin.fullscreen_window")
	
	async def get_orientation(self) -> Literal["LANDSCAPE", "PORTRAIT"]:
		return await self.sync_to_trio(sync_function=self._orientation_get_impl)()
	
	async def get_window_handle(self, window: Optional[Union[str, int]] = None) -> str:
		return await self.sync_to_trio(sync_function=self._get_window_handle_impl)(window=window)
	
	@deprecated(
			"This method is currently not supported. It will raise 'NotImplementedExperimentalFeatureError' on call."
	)
	async def get_window_position(self, windowHandle: str = "current") -> Position:
		raise NotImplementedExperimentalFeatureError(name="CoreWindowMixin.get_window_position")
	
	@deprecated(
			"This method is currently not supported. It will raise 'NotImplementedExperimentalFeatureError' on call."
	)
	async def get_window_rect(self) -> Rectangle:
		raise NotImplementedExperimentalFeatureError(name="CoreWindowMixin.get_window_rect")
	
	@deprecated(
			"This method is currently not supported. It will raise 'NotImplementedExperimentalFeatureError' on call."
	)
	async def get_window_size(self, windowHandle: str = "current") -> Size:
		raise NotImplementedExperimentalFeatureError(name="CoreWindowMixin.get_window_size")
	
	@deprecated(
			"This method is currently not supported. It will raise 'NotImplementedExperimentalFeatureError' on call."
	)
	async def maximize_window(self) -> None:
		raise NotImplementedExperimentalFeatureError(name="CoreWindowMixin.maximize_window")
	
	@deprecated(
			"This method is currently not supported. It will raise 'NotImplementedExperimentalFeatureError' on call."
	)
	async def minimize_window(self) -> None:
		raise NotImplementedExperimentalFeatureError(name="CoreWindowMixin.minimize_window")
	
	async def set_orientation(self, value: Literal["LANDSCAPE", "PORTRAIT"]) -> None:
		await self.sync_to_trio(sync_function=self._orientation_set_impl)(value=value)
	
	@deprecated(
			"This method is currently not supported. It will raise 'NotImplementedExperimentalFeatureError' on call."
	)
	async def set_window_position(self, x: int, y: int, windowHandle: str = "current") -> Position:
		raise NotImplementedExperimentalFeatureError(name="CoreWindowMixin.set_window_position")
	
	@deprecated(
			"This method is currently not supported. It will raise 'NotImplementedExperimentalFeatureError' on call."
	)
	async def set_window_rect(
			self,
			x: Optional[int] = None,
			y: Optional[int] = None,
			width: Optional[int] = None,
			height: Optional[int] = None,
	) -> Rectangle:
		raise NotImplementedExperimentalFeatureError(name="CoreWindowMixin.set_window_rect")
	
	@deprecated(
			"This method is currently not supported. It will raise 'NotImplementedExperimentalFeatureError' on call."
	)
	async def set_window_size(self, width: int, height: int, windowHandle: str = "current") -> None:
		raise NotImplementedExperimentalFeatureError(name="CoreWindowMixin.set_window_size")
	
	def switch_to(self) -> SwitchTo:
		legacy = self._switch_to_impl()
		
		return get_trio_bidi_instance_wrapper(
				wrapper_class=SwitchTo,
				legacy_object=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter,
				trio_token=self._trio_token,
				bidi_buffer_size=self._trio_bidi_buffer_size,
		)
	
	async def window_handles(self) -> List[str]:
		return await self.sync_to_trio(sync_function=self._window_handles_impl)()
