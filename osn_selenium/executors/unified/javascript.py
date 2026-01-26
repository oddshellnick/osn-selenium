from osn_selenium.javascript.models import JS_Scripts
from typing import (
	Any,
	Callable,
	Dict,
	Optional
)
from osn_selenium.javascript.functions import get_js_scripts
from osn_selenium.javascript.fingerprint import FingerprintSettings
from osn_selenium.models import (
	Point,
	Position,
	Rectangle,
	Size
)


__all__ = ["UnifiedJSExecutor"]


class UnifiedJSExecutor:
	"""
	A unified executor for JavaScript scripts within the Selenium environment.
	"""
	
	def __init__(self, execute_function: Callable[[str, Any], Any]):
		"""
		Initialize the UnifiedJSExecutor with an execution function.

		Args:
			execute_function (Callable[[str, Any], Any]): The function that performs the actual JS execution.
		"""
		
		self._execute_function = execute_function
		self._scripts = get_js_scripts()
	
	def _execute_impl(self, script: str, *args: Any) -> Any:
		return self._execute_function(script, *args)
	
	def _check_element_in_viewport_impl(self, element: Any) -> bool:
		return self._execute_impl(self._scripts.check_element_in_viewport, element)
	
	def _get_document_scroll_size_impl(self) -> Size:
		size = self._execute_impl(self._scripts.get_document_scroll_size)
		
		return Size.model_validate(size)
	
	def _get_element_css_style_impl(self, element: Any) -> Dict[str, str]:
		return self._execute_impl(self._scripts.get_element_css, element)
	
	def _get_element_rect_in_viewport_impl(self, element: Any) -> Rectangle:
		rectangle = self._execute_impl(self._scripts.get_element_rect_in_viewport, element)
		
		return Rectangle.model_validate(rectangle)
	
	def _get_random_element_point_in_viewport_impl(self, element: Any, step: int = 1) -> Optional[Position]:
		position = self._execute_impl(self._scripts.get_random_element_point_in_viewport, element, step)
		
		if position is not None:
			return Position.model_validate(position)
		
		return None
	
	def _get_random_element_point_impl(self, element: Any) -> Optional[Point]:
		point_in_viewport = self._get_random_element_point_in_viewport_impl(element=element, step=1)
		
		if point_in_viewport is not None:
			element_viewport_pos = self._get_element_rect_in_viewport_impl(element=element)
		
			if element_viewport_pos is not None:
				x = int(element_viewport_pos.x + point_in_viewport.x)
				y = int(element_viewport_pos.y + point_in_viewport.y)
		
				return Point(x=x, y=y)
		
		return None
	
	def _get_viewport_position_impl(self) -> Position:
		position = self._execute_impl(self._scripts.get_viewport_position)
		
		return Position.model_validate(position)
	
	def _get_viewport_rect_impl(self) -> Rectangle:
		rectangle = self._execute_impl(self._scripts.get_viewport_rect)
		
		return Rectangle.model_validate(rectangle)
	
	def _get_viewport_size_impl(self) -> Size:
		size = self._execute_impl(self._scripts.get_viewport_size)
		
		return Size.model_validate(size)
	
	def _open_new_tab_impl(self, link: str = "") -> None:
		self._execute_impl(self._scripts.open_new_tab, link)
	
	@property
	def _scripts_impl(self) -> JS_Scripts:
		return self._scripts
	
	def _start_fingerprint_detection_impl(self, fingerprint_settings: FingerprintSettings) -> None:
		self._execute_impl(fingerprint_settings.generate_js())
	
	def _stop_window_loading_impl(self) -> None:
		self._execute_impl(self._scripts.stop_window_loading)
