from osn_selenium.types import Point
from osn_selenium.instances.types import WEB_ELEMENT_TYPEHINT
from osn_selenium.executors.sync.javascript import JSExecutor
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.instances.sync.web_element import WebElement
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver import (
	ActionChains as legacyActionChains
)
from typing import (
	Any,
	Callable,
	Optional,
	Self,
	Tuple,
	Union
)
from osn_selenium.instances._functions import (
	move_to_parts,
	scroll_to_parts,
	text_input_to_parts
)
from osn_selenium.abstract.instances.action_chains import (
	AbstractActionChains,
	AbstractHumanLikeActionChains
)


class ActionChains(AbstractActionChains):
	def __init__(self, selenium_action_chains: legacyActionChains) -> None:
		if not isinstance(selenium_action_chains, legacyActionChains):
			raise ExpectedTypeError(
					expected_class=legacyActionChains,
					received_instance=selenium_action_chains
			)
		
		self._selenium_action_chains = selenium_action_chains
	
	def click(self, on_element: Optional[WEB_ELEMENT_TYPEHINT] = None) -> Self:
		self._selenium_action_chains.click(on_element=get_legacy_instance(on_element))
		
		return self
	
	def click_and_hold(self, on_element: Optional[WEB_ELEMENT_TYPEHINT] = None) -> Self:
		self._selenium_action_chains.click_and_hold(on_element=get_legacy_instance(on_element))
		
		return self
	
	def context_click(self, on_element: Optional[WEB_ELEMENT_TYPEHINT] = None) -> Self:
		self._selenium_action_chains.context_click(on_element=get_legacy_instance(on_element))
		
		return self
	
	def double_click(self, on_element: Optional[WEB_ELEMENT_TYPEHINT] = None) -> Self:
		self._selenium_action_chains.double_click(on_element=get_legacy_instance(on_element))
		
		return self
	
	def drag_and_drop(
			self,
			source_element: WEB_ELEMENT_TYPEHINT,
			target_element: WEB_ELEMENT_TYPEHINT
	) -> Self:
		self._selenium_action_chains.drag_and_drop(
				source=get_legacy_instance(source_element),
				target=get_legacy_instance(target_element)
		)
		
		return self
	
	def drag_and_drop_by_offset(self, source_element: WEB_ELEMENT_TYPEHINT, xoffset: int, yoffset: int) -> Self:
		self._selenium_action_chains.drag_and_drop_by_offset(
				source=get_legacy_instance(source_element),
				xoffset=xoffset,
				yoffset=yoffset
		)
		
		return self
	
	def key_down(self, value: str, element: Optional[WEB_ELEMENT_TYPEHINT] = None) -> Self:
		self._selenium_action_chains.key_down(value=value, element=get_legacy_instance(element))
		
		return self
	
	def key_up(self, value: str, element: Optional[WEB_ELEMENT_TYPEHINT] = None) -> Self:
		self._selenium_action_chains.key_up(value=value, element=get_legacy_instance(element))
		
		return self
	
	@property
	def legacy(self) -> legacyActionChains:
		return self._selenium_action_chains
	
	def move_by_offset(self, xoffset: int, yoffset: int) -> Self:
		self._selenium_action_chains.move_by_offset(xoffset=xoffset, yoffset=yoffset)
		
		return self
	
	def move_to_element(self, to_element: WEB_ELEMENT_TYPEHINT) -> Self:
		self._selenium_action_chains.move_to_element(to_element=get_legacy_instance(to_element))
		
		return self
	
	def move_to_element_with_offset(self, to_element: WEB_ELEMENT_TYPEHINT, xoffset: int, yoffset: int) -> Self:
		self._selenium_action_chains.move_to_element_with_offset(
				to_element=get_legacy_instance(to_element),
				xoffset=xoffset,
				yoffset=yoffset
		)
		
		return self
	
	def pause(self, seconds: Union[float, int]) -> Self:
		self._selenium_action_chains.pause(seconds=seconds)
		
		return self
	
	def perform(self) -> Self:
		self._selenium_action_chains.perform()
		
		return self
	
	def release(self, on_element: Optional[WEB_ELEMENT_TYPEHINT] = None) -> Self:
		self._selenium_action_chains.release(on_element=get_legacy_instance(on_element))
		
		return self
	
	def scroll_by_amount(self, delta_x: int, delta_y: int) -> Self:
		self._selenium_action_chains.scroll_by_amount(delta_x=delta_x, delta_y=delta_y)
		
		return self
	
	def scroll_from_origin(self, scroll_origin: ScrollOrigin, delta_x: int, delta_y: int) -> Self:
		self._selenium_action_chains.scroll_from_origin(scroll_origin=scroll_origin, delta_x=delta_x, delta_y=delta_y)
		
		return self
	
	def scroll_to_element(self, element: WEB_ELEMENT_TYPEHINT) -> Self:
		self._selenium_action_chains.scroll_to_element(element=get_legacy_instance(element))
		
		return self
	
	def send_keys(self, *keys_to_send: str) -> Self:
		self._selenium_action_chains.send_keys(*keys_to_send)
		
		return self
	
	def send_keys_to_element(self, element: WEB_ELEMENT_TYPEHINT, *keys_to_send: str) -> Self:
		self._selenium_action_chains.send_keys_to_element(get_legacy_instance(element), *keys_to_send)
		
		return self


class HumanLikeActionChains(ActionChains, AbstractHumanLikeActionChains):
	def __init__(
			self,
			execute_script_function: Callable[[str, Any], Any],
			selenium_action_chains: legacyActionChains
	) -> None:
		super().__init__(selenium_action_chains=selenium_action_chains)
		
		self._js_executor = JSExecutor(execute_function=execute_script_function)
	
	def hm_move(self, start_position: Point, end_position: Point) -> Self:
		parts = move_to_parts(start_position=start_position, end_position=end_position)
		
		for part in parts:
			self.pause(seconds=part.duration * 0.001)
			self.move_by_offset(xoffset=part.offset.x, yoffset=part.offset.y)
		
		return self
	
	def hm_move_by_offset(self, start_position: Point, xoffset: int, yoffset: int) -> Tuple[Self, Point]:
		end_position = Point(x=start_position.x + xoffset, y=start_position.y + yoffset)
		
		return self.hm_move(start_position=start_position, end_position=end_position), end_position
	
	def hm_move_to_element(self, start_position: Point, element: WEB_ELEMENT_TYPEHINT) -> Tuple[Self, Point]:
		element_rect = WebElement.from_legacy(selenium_web_element=get_legacy_instance(element)).rect()
		end_position = Point(
				x=element_rect["x"] +
				element_rect["width"] //
				2,
				y=element_rect["y"] +
				element_rect["height"] //
				2
		)
		
		return self.hm_move(start_position=start_position, end_position=end_position), end_position
	
	def hm_move_to_element_with_offset(
			self,
			start_position: Point,
			element: WEB_ELEMENT_TYPEHINT,
			xoffset: int,
			yoffset: int
	) -> Tuple[Self, Point]:
		element_rect = WebElement.from_legacy(selenium_web_element=get_legacy_instance(element)).rect()
		end_position = Point(x=element_rect["x"] + xoffset, y=element_rect["y"] + yoffset)
		
		return self.hm_move(start_position=start_position, end_position=end_position), end_position
	
	def hm_move_to_element_with_random_offset(self, start_position: Point, element: WEB_ELEMENT_TYPEHINT) -> Tuple[Self, Point]:
		end_position = self._js_executor.get_random_element_point(element=get_legacy_instance(element))
		
		return self.hm_move(start_position=start_position, end_position=end_position), end_position
	
	def hm_scroll(self, delta_x: int, delta_y: int, origin: Optional[ScrollOrigin] = None) -> Self:
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
			element: WEB_ELEMENT_TYPEHINT,
			additional_lower_y_offset: int = 0,
			additional_upper_y_offset: int = 0,
			additional_right_x_offset: int = 0,
			additional_left_x_offset: int = 0,
			origin: Optional[ScrollOrigin] = None,
	) -> Self:
		viewport_rect = self._js_executor.get_viewport_rect()
		element_rect = self._js_executor.get_element_rect_in_viewport(element=get_legacy_instance(element))
		
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
	
	def hm_text_input(self, text: str) -> Self:
		parts = text_input_to_parts(text=text)
		
		for part in parts:
			self.pause(seconds=part.duration * 0.001)
			self.send_keys(part.text)
		
		return self
