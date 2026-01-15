from osn_selenium._functions import read_js_scripts
from typing import (
	Any,
	Callable,
	Dict,
	Optional
)
from osn_selenium.instances.sync.web_element import WebElement
from osn_selenium.abstract.executors.javascript import AbstractJSExecutor
from osn_selenium.types import (
	JS_Scripts,
	Point,
	Position,
	Rectangle,
	Size
)


class JSExecutor(AbstractJSExecutor):
	def __init__(self, execute_function: Callable[[str, Any], Any]):
		self._execute_function = execute_function
		self._scripts = read_js_scripts()
	
	def execute(self, script: str, *args: Any) -> Any:
		return self._execute_function(script, *args)
	
	def check_element_in_viewport(self, element: WebElement) -> bool:
		return self.execute(self._scripts.check_element_in_viewport, element)
	
	def get_document_scroll_size(self) -> Size:
		size = self.execute(self._scripts.get_document_scroll_size)
		
		return Size.model_validate(size)
	
	def get_element_css_style(self, element: WebElement) -> Dict[str, str]:
		return self.execute(self._scripts.get_element_css, element)
	
	def get_element_rect_in_viewport(self, element: WebElement) -> Rectangle:
		rectangle = self.execute(self._scripts.get_element_rect_in_viewport, element)
		
		return Rectangle.model_validate(rectangle)
	
	def get_random_element_point_in_viewport(self, element: WebElement, step: int = 1) -> Optional[Position]:
		position = self.execute(self._scripts.get_random_element_point_in_viewport, element, step)
		
		if position is not None:
			return Position.model_validate(position)
		
		return None
	
	def get_random_element_point(self, element: WebElement) -> Point:
		point_in_viewport = self.get_random_element_point_in_viewport(element=element, step=1)
		
		element_viewport_pos = self.get_element_rect_in_viewport(element=element)
		
		x = int(element_viewport_pos.x + point_in_viewport.x)
		y = int(element_viewport_pos.y + point_in_viewport.y)
		
		return Point(x=x, y=y)
	
	def get_viewport_position(self) -> Position:
		position = self.execute(self._scripts.get_viewport_position)
		
		return Position.model_validate(position)
	
	def get_viewport_rect(self) -> Rectangle:
		rectangle = self.execute(self._scripts.get_viewport_rect)
		
		return Rectangle.model_validate(rectangle)
	
	def get_viewport_size(self) -> Size:
		size = self.execute(self._scripts.get_viewport_size)
		
		return Size.model_validate(size)
	
	def open_new_tab(self, link: str = "") -> None:
		self.execute(self._scripts.open_new_tab, link)
	
	@property
	def scripts(self) -> JS_Scripts:
		return self._scripts
	
	def stop_window_loading(self) -> None:
		self.execute(self._scripts.stop_window_loading)
