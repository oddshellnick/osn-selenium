from osn_selenium.types import DEVICES_TYPEHINT
from osn_selenium.webdrivers.types import Point
from typing import (
	List,
	Optional,
	Self, Tuple,
	Union
)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from osn_selenium.executors.sync.javascript import JSExecutor
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver import (
	ActionChains as selenium_ActionChains
)
from osn_selenium.webdrivers._functions import (
	move_to_parts,
	scroll_to_parts,
	text_input_to_parts
)
from osn_selenium.abstract.instances.action_chains import (
	AbstractActionChains,
	AbstractHumanLikeActionChains
)


class ActionChains(AbstractActionChains):
	def __init__(
			self,
			driver: WebDriver,
			duration: int = 250,
			devices: Optional[List[DEVICES_TYPEHINT]] = None
	):
		self._driver = driver
		
		self._action = selenium_ActionChains(driver=driver, duration=duration, devices=devices,)
	
	def click(self, on_element: Optional[WebElement] = None,) -> Self:
		self._action.click(on_element=on_element)
		
		return self
	
	def click_and_hold(self, on_element: Optional[WebElement] = None,) -> Self:
		self._action.click_and_hold(on_element=on_element)
		
		return self
	
	def context_click(self, on_element: Optional[WebElement] = None,) -> Self:
		self._action.context_click(on_element=on_element)
		
		return self
	
	def double_click(self, on_element: Optional[WebElement] = None,) -> Self:
		self._action.double_click(on_element=on_element)
		
		return self
	
	def drag_and_drop(self, source_element: WebElement, target_element: WebElement,) -> Self:
		self._action.drag_and_drop(source=source_element, target=target_element)
		
		return self
	
	def drag_and_drop_by_offset(self, source_element: WebElement, xoffset: int, yoffset: int,) -> Self:
		self._action.drag_and_drop_by_offset(source=source_element, xoffset=xoffset, yoffset=yoffset)
		
		return self
	
	def key_down(self, value: str, element: Optional[WebElement] = None,) -> Self:
		self._action.key_down(value=value, element=element)
		
		return self
	
	def key_up(self, value: str, element: Optional[WebElement] = None,) -> Self:
		self._action.key_up(value=value, element=element)
		
		return self
	
	def move_by_offset(self, xoffset: int, yoffset: int,) -> Self:
		self._action.move_by_offset(xoffset=xoffset, yoffset=yoffset,)
		
		return self
	
	def move_to_element(self, to_element: WebElement,) -> Self:
		self._action.move_to_element(to_element=to_element)
		
		return self
	
	def move_to_element_with_offset(self, to_element: WebElement, xoffset: int, yoffset: int,) -> Self:
		self._action.move_to_element_with_offset(to_element=to_element, xoffset=xoffset, yoffset=yoffset)
		
		return self
	
	def pause(self, seconds: Union[float, int],) -> Self:
		self._action.pause(seconds=seconds)
		
		return self
	
	def perform(self) -> Self:
		self._action.perform()
		
		return self
	
	def release(self, on_element: Optional[WebElement] = None,) -> Self:
		self._action.release(on_element=on_element)
		
		return self
	
	def scroll_by_amount(self, delta_x: int, delta_y: int,) -> Self:
		self._action.scroll_by_amount(delta_x=delta_x, delta_y=delta_y)
		
		return self
	
	def scroll_from_origin(self, scroll_origin: ScrollOrigin, delta_x: int, delta_y: int,) -> Self:
		self._action.scroll_from_origin(scroll_origin=scroll_origin, delta_x=delta_x, delta_y=delta_y)
		
		return self
	
	def scroll_to_element(self, element: WebElement,) -> Self:
		self._action.scroll_to_element(element=element)
		
		return self
	
	def send_keys(self, keys_to_send: str,) -> Self:
		self._action.send_keys(keys_to_send)
		
		return self
	
	def send_keys_to_element(self, element: WebElement, keys_to_send: str,) -> Self:
		self._action.send_keys_to_element(element, keys_to_send)
		
		return self


class HumanLikeActionChains(ActionChains, AbstractHumanLikeActionChains):
	def __init__(
			self,
			driver: WebDriver,
			duration: int = 250,
			devices: Optional[List[DEVICES_TYPEHINT]] = None
	) -> None:
		super().__init__(driver=driver, duration=duration, devices=devices)
		
		self._js_executor = JSExecutor(execute_function=self._driver.execute_script)
	
	def hm_move(self, start_position: Point, end_position: Point,) -> Self:
		parts = move_to_parts(start_position=start_position, end_position=end_position)
		
		for part in parts:
			self.pause(seconds=part.duration * 0.001)
			self.move_by_offset(xoffset=part.offset.x, yoffset=part.offset.y)
		
		return self
	
	def hm_move_to_element(self, start_position: Point, element: WebElement,) -> Tuple[Self, Point]:
		end_position = self._js_executor.get_random_element_point(element=element)
		
		return self.hm_move(start_position=start_position, end_position=end_position), end_position
	
	def hm_scroll(self, delta_x: int, delta_y: int, origin: Optional[ScrollOrigin] = None,) -> Self:
		if origin is None:
			viewport_size = self._js_executor.get_viewport_size()
		
			origin_x = 0 if delta_x >= 0 else viewport_size.width
			origin_y = 0 if delta_y >= 0 else viewport_size.height
		
			origin = ScrollOrigin.from_viewport(x_offset=origin_x, y_offset=origin_y)
		
		start = Point(x=int(origin.x_offset), y=int(origin.y_offset))
		end = Point(x=int(origin.x_offset) + int(delta_x), y=int(origin.y_offset) + int(delta_y))
		
		parts = scroll_to_parts(start_position=start, end_position=end)
		
		for part in parts:
			self.pause(seconds=part.duration * 0.001)
			self.scroll_from_origin(scroll_origin=origin, delta_x=int(part.delta.x), delta_y=int(part.delta.y))
		
		return self
	
	def hm_scroll_to_element(
			self,
			element: WebElement,
			additional_lower_y_offset: int = 0,
			additional_upper_y_offset: int = 0,
			additional_right_x_offset: int = 0,
			additional_left_x_offset: int = 0,
			origin: Optional[ScrollOrigin] = None,
	) -> Self:
		viewport_rect = self._js_executor.get_viewport_rect()
		element_rect = self._js_executor.get_element_rect_in_viewport(element=element)
		
		if element_rect.x < additional_left_x_offset:
			delta_x = int(element_rect.x - additional_left_x_offset)
		elif element_rect.x + element_rect.width > viewport_rect.width - additional_right_x_offset:
			delta_x = int(
					element_rect.x + element_rect.width - (viewport_rect.width - additional_right_x_offset)
			)
		else:
			delta_x = 0
		
		if element_rect.y < additional_upper_y_offset:
			delta_y = int(element_rect.y - additional_upper_y_offset)
		elif element_rect.y + element_rect.height > viewport_rect.height - additional_lower_y_offset:
			delta_y = int(
					element_rect.y + element_rect.height - (viewport_rect.height - additional_lower_y_offset)
			)
		else:
			delta_y = 0
		
		return self.hm_scroll(delta_x=delta_x, delta_y=delta_y, origin=origin)
	
	def hm_text_input(self, text: str,) -> Self:
		parts = text_input_to_parts(text=text)
		
		for part in parts:
			self.pause(seconds=part.duration * 0.001)
			self.send_keys(part.text)
		
		return self
