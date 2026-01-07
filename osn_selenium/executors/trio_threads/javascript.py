from osn_selenium._functions import read_js_scripts
from selenium.webdriver.remote.webelement import WebElement
from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	Optional
)
from osn_selenium.abstract.executors.javascript import AbstractJSExecutor
from osn_selenium.types import (
	JS_Scripts,
	Point,
	Position,
	Rectangle,
	Size
)


class JSExecutor(AbstractJSExecutor):
	def __init__(self, execute_function: Callable[[str, Any], Coroutine[Any, Any, Any]]):
		self._execute_function = execute_function
		self._scripts = read_js_scripts()
	
	async def execute(self, script: str, *args: Any) -> Any:
		return await self._execute_function(script, *args)
	
	async def check_element_in_viewport(self, element: WebElement) -> bool:
		return await self.execute(self._scripts.check_element_in_viewport, element)
	
	async def get_document_scroll_size(self) -> Size:
		size = await self.execute(self._scripts.get_document_scroll_size)
		
		return Size.model_validate(size)
	
	async def get_element_css_style(self, element: WebElement) -> Dict[str, str]:
		return await self.execute(self._scripts.get_element_css, element)
	
	async def get_element_rect_in_viewport(self, element: WebElement) -> Optional[Rectangle]:
		rectangle = await self.execute(self._scripts.get_element_rect_in_viewport, element)
		
		if rectangle is not None:
			return Rectangle.model_validate(rectangle)
		
		return rectangle
	
	async def get_random_element_point_in_viewport(self, element: WebElement, step: int = 1) -> Optional[Position]:
		position = await self.execute(self._scripts.get_random_element_point_in_viewport, element, step)
		
		if position is not None:
			return Position.model_validate(position)
		
		return None
	
	async def get_random_element_point(self, element: WebElement) -> Optional[Point]:
		point_in_viewport = await self.get_random_element_point_in_viewport(element=element, step=1)
		
		if point_in_viewport is not None:
			element_viewport_pos = await self.get_element_rect_in_viewport(element=element)
		
			if element_viewport_pos is not None:
				x = int(element_viewport_pos.x + point_in_viewport.x)
				y = int(element_viewport_pos.y + point_in_viewport.y)
		
				return Point(x=x, y=y)
		
		return None
	
	async def get_viewport_position(self) -> Position:
		position = await self.execute(self._scripts.get_viewport_position)
		
		return Position.model_validate(position)
	
	async def get_viewport_rect(self) -> Rectangle:
		rectangle = await self.execute(self._scripts.get_viewport_rect)
		
		return Rectangle.model_validate(rectangle)
	
	async def get_viewport_size(self) -> Size:
		size = await self.execute(self._scripts.get_viewport_size)
		
		return Size.model_validate(size)
	
	async def open_new_tab(self, link: str = "") -> None:
		await self.execute(self._scripts.open_new_tab, link)
	
	@property
	def scripts(self) -> JS_Scripts:
		return self._scripts
	
	async def stop_window_loading(self) -> None:
		await self.execute(self._scripts.stop_window_loading)
