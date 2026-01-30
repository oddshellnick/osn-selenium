import trio
from osn_selenium.trio_threads_mixin import TrioThreadMixin
from osn_selenium.javascript.models import JS_Scripts
from typing import (
	Any,
	Callable,
	Dict,
	Optional
)
from osn_selenium.javascript.fingerprint import FingerprintSettings
from osn_selenium.instances.trio_threads.web_element import WebElement
from osn_selenium.executors.unified.javascript import UnifiedJSExecutor
from osn_selenium.models import (
	Point,
	Position,
	Rectangle,
	Size
)
from osn_selenium.abstract.executors.javascript import AbstractJSExecutor


__all__ = ["JSExecutor"]


class JSExecutor(UnifiedJSExecutor, TrioThreadMixin, AbstractJSExecutor):
	"""
	An asynchronous JavaScript executor that integrates Trio's threading mixin for thread-safe operations.
	"""
	
	def __init__(
			self,
			execute_function: Callable[[str, Any], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		"""
		Initialize the JSExecutor with Trio synchronization primitives and execution logic.

		Args:
			execute_function (Callable[[str, Any], Any]): The function used to run JavaScript code.
			lock (trio.Lock): Trio lock for synchronizing access.
			limiter (trio.CapacityLimiter): Trio limiter for controlling concurrency.
		"""
		
		UnifiedJSExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def check_element_in_viewport(self, element: WebElement) -> bool:
		return await self.sync_to_trio(sync_function=self._check_element_in_viewport_impl)(element=element)
	
	async def execute(self, script: str, *args: Any) -> Any:
		return await self.sync_to_trio(sync_function=self._execute_impl)(script, *args)
	
	async def get_document_scroll_size(self) -> Size:
		return await self.sync_to_trio(sync_function=self._get_document_scroll_size_impl)()
	
	async def get_element_css_style(self, element: WebElement) -> Dict[str, str]:
		return await self.sync_to_trio(sync_function=self._get_element_css_style_impl)(element=element)
	
	async def get_element_rect_in_viewport(self, element: WebElement) -> Optional[Rectangle]:
		return await self.sync_to_trio(sync_function=self._get_element_rect_in_viewport_impl)(element=element)
	
	async def get_random_element_point(self, element: WebElement) -> Optional[Point]:
		return await self.sync_to_trio(sync_function=self._get_random_element_point_impl)(element=element)
	
	async def get_random_element_point_in_viewport(self, element: WebElement, step: int = 1) -> Optional[Position]:
		return await self.sync_to_trio(sync_function=self._get_random_element_point_in_viewport_impl)(element=element, step=step)
	
	async def get_viewport_position(self) -> Position:
		return await self.sync_to_trio(sync_function=self._get_viewport_position_impl)()
	
	async def get_viewport_rect(self) -> Rectangle:
		return await self.sync_to_trio(sync_function=self._get_viewport_rect_impl)()
	
	async def get_viewport_size(self) -> Size:
		return await self.sync_to_trio(sync_function=self._get_viewport_size_impl)()
	
	async def open_new_tab(self, link: str = "") -> None:
		await self.sync_to_trio(sync_function=self._open_new_tab_impl)(link=link)
	
	@property
	def scripts(self) -> JS_Scripts:
		return self._scripts_impl
	
	async def start_fingerprint_detection(self, fingerprint_settings: FingerprintSettings) -> None:
		await self.sync_to_trio(sync_function=self._start_fingerprint_detection_impl)(fingerprint_settings=fingerprint_settings)
	
	async def stop_window_loading(self) -> None:
		await self.sync_to_trio(sync_function=self._stop_window_loading_impl)()
