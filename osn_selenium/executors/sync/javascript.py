from osn_selenium.javascript.models import JS_Scripts
from typing import (
	Any,
	Callable,
	Dict,
	Optional
)
from osn_selenium.instances.sync.web_element import WebElement
from osn_selenium.javascript.fingerprint import FingerprintSettings
from osn_selenium.executors.unified.javascript import UnifiedJSExecutor
from osn_selenium.models import (
	Point,
	Position,
	Rectangle,
	Size
)
from osn_selenium.abstract.executors.javascript import AbstractJSExecutor


__all__ = ["JSExecutor"]


class JSExecutor(UnifiedJSExecutor, AbstractJSExecutor):
	"""
	A synchronous JavaScript executor that provides unified access to browser-side script execution.
	"""
	
	def __init__(self, execute_function: Callable[[str, Any], Any]):
		"""
		Initialize the JSExecutor with a synchronous execution function.

		Args:
			execute_function (Callable[[str, Any], Any]): The function used to run JavaScript code.
		"""
		
		UnifiedJSExecutor.__init__(self, execute_function=execute_function)
	
	def check_element_in_viewport(self, element: WebElement) -> bool:
		return self._check_element_in_viewport_impl(element=element)
	
	def execute(self, script: str, *args: Any) -> Any:
		return self._execute_impl(script, *args)
	
	def get_document_scroll_size(self) -> Size:
		return self._get_document_scroll_size_impl()
	
	def get_element_css_style(self, element: WebElement) -> Dict[str, str]:
		return self._get_element_css_style_impl(element=element)
	
	def get_element_rect_in_viewport(self, element: WebElement) -> Rectangle:
		return self._get_element_rect_in_viewport_impl(element=element)
	
	def get_random_element_point(self, element: WebElement) -> Optional[Point]:
		return self._get_random_element_point_impl(element=element)
	
	def get_random_element_point_in_viewport(self, element: WebElement, step: int = 1) -> Optional[Position]:
		return self._get_random_element_point_in_viewport_impl(element=element, step=step)
	
	def get_viewport_position(self) -> Position:
		return self._get_viewport_position_impl()
	
	def get_viewport_rect(self) -> Rectangle:
		return self._get_viewport_rect_impl()
	
	def get_viewport_size(self) -> Size:
		return self._get_viewport_size_impl()
	
	def open_new_tab(self, link: str = "") -> None:
		self._open_new_tab_impl(link=link)
	
	@property
	def scripts(self) -> JS_Scripts:
		return self._scripts_impl
	
	def start_fingerprint_detection(self, fingerprint_settings: FingerprintSettings) -> None:
		self._start_fingerprint_detection_impl(fingerprint_settings=fingerprint_settings)
	
	def stop_window_loading(self) -> None:
		self._stop_window_loading_impl()
