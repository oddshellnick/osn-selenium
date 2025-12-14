import trio
from osn_selenium.types import Point
from osn_selenium.trio_base_mixin import _TrioThreadMixin
from osn_selenium.instances.types import WEB_ELEMENT_TYPEHINT
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.executors.trio_threads.javascript import JSExecutor
from osn_selenium.instances.trio_threads.web_element import WebElement
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from typing import (
	Any,
	Callable,
	Coroutine,
	Optional,
	Self,
	Tuple,
	Union
)
from selenium.webdriver.common.action_chains import (
	ActionChains as legacyActionChains
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


class ActionChains(_TrioThreadMixin, AbstractActionChains):
	"""
	Wrapper for the legacy Selenium ActionChains instance.

	Provides low-level interactions such as mouse movements, mouse button actions,
	key presses, and context menu interactions.
	"""
	
	def __init__(
			self,
			selenium_action_chains: legacyActionChains,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> None:
		"""
		Initializes the ActionChains wrapper.

		Args:
			selenium_action_chains (legacyActionChains): The legacy Selenium ActionChains instance to wrap.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.
		"""
		
		super().__init__(lock=lock, limiter=limiter)
		
		if not isinstance(selenium_action_chains, legacyActionChains):
			raise ExpectedTypeError(
					expected_class=legacyActionChains,
					received_instance=selenium_action_chains
			)
		
		self._selenium_action_chains = selenium_action_chains
	
	async def click(self, on_element: Optional[WEB_ELEMENT_TYPEHINT] = None) -> Self:
		await self._wrap_to_trio(
				self._selenium_action_chains.click,
				on_element=get_legacy_instance(on_element)
		)
		
		return self
	
	async def click_and_hold(self, on_element: Optional[WEB_ELEMENT_TYPEHINT] = None) -> Self:
		await self._wrap_to_trio(
				self._selenium_action_chains.click_and_hold,
				on_element=get_legacy_instance(on_element)
		)
		
		return self
	
	async def context_click(self, on_element: Optional[WEB_ELEMENT_TYPEHINT] = None) -> Self:
		await self._wrap_to_trio(
				self._selenium_action_chains.context_click,
				on_element=get_legacy_instance(on_element)
		)
		
		return self
	
	async def double_click(self, on_element: Optional[WEB_ELEMENT_TYPEHINT] = None) -> Self:
		await self._wrap_to_trio(
				self._selenium_action_chains.double_click,
				on_element=get_legacy_instance(on_element)
		)
		
		return self
	
	async def drag_and_drop(self, source: WEB_ELEMENT_TYPEHINT, target: WEB_ELEMENT_TYPEHINT) -> Self:
		await self._wrap_to_trio(
				self._selenium_action_chains.drag_and_drop,
				source=get_legacy_instance(source),
				target=get_legacy_instance(target)
		)
		
		return self
	
	async def drag_and_drop_by_offset(self, source: WEB_ELEMENT_TYPEHINT, xoffset: int, yoffset: int) -> Self:
		await self._wrap_to_trio(
				self._selenium_action_chains.drag_and_drop_by_offset,
				source=get_legacy_instance(source),
				xoffset=xoffset,
				yoffset=yoffset
		)
		
		return self
	
	async def key_down(self, value: str, element: Optional[WEB_ELEMENT_TYPEHINT] = None) -> Self:
		await self._wrap_to_trio(
				self._selenium_action_chains.key_down,
				value=value,
				element=get_legacy_instance(element)
		)
		
		return self
	
	async def key_up(self, value: str, element: Optional[WEB_ELEMENT_TYPEHINT] = None) -> Self:
		await self._wrap_to_trio(
				self._selenium_action_chains.key_up,
				value=value,
				element=get_legacy_instance(element)
		)
		
		return self
	
	@property
	def legacy(self) -> legacyActionChains:
		return self._selenium_action_chains
	
	async def move_by_offset(self, xoffset: int, yoffset: int) -> Self:
		await self._wrap_to_trio(
				self._selenium_action_chains.move_by_offset,
				xoffset=xoffset,
				yoffset=yoffset,
		)
		
		return self
	
	async def move_to_element(self, to_element: WEB_ELEMENT_TYPEHINT) -> Self:
		await self._wrap_to_trio(
				self._selenium_action_chains.move_to_element,
				to_element=get_legacy_instance(to_element)
		)
		
		return self
	
	async def move_to_element_with_offset(self, to_element: WEB_ELEMENT_TYPEHINT, xoffset: int, yoffset: int) -> Self:
		await self._wrap_to_trio(
				self._selenium_action_chains.move_to_element_with_offset,
				to_element=get_legacy_instance(to_element),
				xoffset=xoffset,
				yoffset=yoffset
		)
		
		return self
	
	async def pause(self, seconds: Union[float, int]) -> Self:
		await self._wrap_to_trio(self._selenium_action_chains.pause, seconds=seconds)
		
		return self
	
	async def perform(self) -> None:
		await self._wrap_to_trio(self._selenium_action_chains.perform)
	
	async def release(self, on_element: Optional[WEB_ELEMENT_TYPEHINT] = None) -> Self:
		await self._wrap_to_trio(
				self._selenium_action_chains.release,
				on_element=get_legacy_instance(on_element)
		)
		
		return self
	
	async def scroll_by_amount(self, delta_x: int, delta_y: int) -> Self:
		await self._wrap_to_trio(
				self._selenium_action_chains.scroll_by_amount,
				delta_x=delta_x,
				delta_y=delta_y
		)
		
		return self
	
	async def scroll_from_origin(self, scroll_origin: ScrollOrigin, delta_x: int, delta_y: int) -> Self:
		await self._wrap_to_trio(
				self._selenium_action_chains.scroll_from_origin,
				scroll_origin=scroll_origin,
				delta_x=delta_x,
				delta_y=delta_y
		)
		
		return self
	
	async def scroll_to_element(self, element: WEB_ELEMENT_TYPEHINT) -> Self:
		await self._wrap_to_trio(
				self._selenium_action_chains.scroll_to_element,
				element=get_legacy_instance(element)
		)
		
		return self
	
	async def send_keys(self, *keys_to_send: str) -> Self:
		await self._wrap_to_trio(self._selenium_action_chains.send_keys, *keys_to_send)
		
		return self
	
	async def send_keys_to_element(self, element: WEB_ELEMENT_TYPEHINT, *keys_to_send: str) -> Self:
		await self._wrap_to_trio(
				self._selenium_action_chains.send_keys_to_element,
				get_legacy_instance(element),
				*keys_to_send
		)
		
		return self


class HumanLikeActionChains(ActionChains, AbstractHumanLikeActionChains):
	"""
	Extended ActionChains class simulating human-like behavior.

	Implements natural mouse movements (using Bezier curves or deviations),
	human-like typing with variable delays, and smooth scrolling.
	"""
	
	def __init__(
			self,
			execute_script_function: Callable[[str, Any], Coroutine[Any, Any, Any]],
			selenium_action_chains: legacyActionChains,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> None:
		"""
		Initializes the HumanLikeActionChains wrapper.

		Args:
			execute_script_function (Callable[[str, Any], Coroutine[Any, Any, Any]]): Function to execute JavaScript in the browser.
			selenium_action_chains (legacyActionChains): The legacy Selenium ActionChains instance.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.
		"""
		
		super().__init__(
				selenium_action_chains=selenium_action_chains,
				lock=lock,
				limiter=limiter
		)
		
		self._js_executor = JSExecutor(execute_function=execute_script_function)
	
	async def hm_move(self, start_position: Point, end_position: Point) -> Self:
		parts = await self._wrap_to_trio(
				move_to_parts,
				start_position=start_position,
				end_position=end_position
		)
		
		for part in parts:
			await self.pause(seconds=part.duration * 0.001)
			await self.move_by_offset(xoffset=part.offset.x, yoffset=part.offset.y)
		
		return self
	
	async def hm_move_by_offset(self, start_position: Point, xoffset: int, yoffset: int) -> Tuple[Self, Point]:
		end_position = Point(x=start_position.x + xoffset, y=start_position.y + yoffset)
		
		return await self.hm_move(start_position=start_position, end_position=end_position), end_position
	
	async def hm_move_to_element(self, start_position: Point, element: WEB_ELEMENT_TYPEHINT) -> Tuple[Self, Point]:
		element_rect = await WebElement.from_legacy(
				selenium_web_element=get_legacy_instance(element),
				lock=self._lock,
				limiter=self._capacity_limiter
		).rect()
		end_position = Point(
				x=element_rect["x"] +
				element_rect["width"] //
				2,
				y=element_rect["y"] +
				element_rect["height"] //
				2
		)
		
		return await self.hm_move(start_position=start_position, end_position=end_position), end_position
	
	async def hm_move_to_element_with_offset(
			self,
			start_position: Point,
			element: WEB_ELEMENT_TYPEHINT,
			xoffset: int,
			yoffset: int
	) -> Tuple[Self, Point]:
		element_rect = await WebElement.from_legacy(
				selenium_web_element=get_legacy_instance(element),
				lock=self._lock,
				limiter=self._capacity_limiter
		).rect()
		end_position = Point(x=element_rect["x"] + xoffset, y=element_rect["y"] + yoffset)
		
		return await self.hm_move(start_position=start_position, end_position=end_position), end_position
	
	async def hm_move_to_element_with_random_offset(self, start_position: Point, element: WEB_ELEMENT_TYPEHINT) -> Tuple[Self, Point]:
		end_position = await self._js_executor.get_random_element_point(element=get_legacy_instance(element))
		
		return await self.hm_move(start_position=start_position, end_position=end_position), end_position
	
	async def hm_scroll(self, delta_x: int, delta_y: int, origin: Optional[ScrollOrigin] = None) -> Self:
		if origin is None:
			viewport_size = await self._js_executor.get_viewport_size()
		
			origin_x = 0 if delta_x >= 0 else viewport_size.width
			origin_y = 0 if delta_y >= 0 else viewport_size.height
		
			origin = ScrollOrigin.from_viewport(x_offset=origin_x, y_offset=origin_y)
		
		start = Point(x=int(origin.x_offset), y=int(origin.y_offset))
		end = Point(x=int(origin.x_offset) + int(delta_x), y=int(origin.y_offset) + int(delta_y))
		
		parts = await self._wrap_to_trio(scroll_to_parts, start_position=start, end_position=end)
		
		for part in parts:
			await self.pause(seconds=part.duration * 0.001)
			await self.scroll_from_origin(scroll_origin=origin, delta_x=int(part.delta.x), delta_y=int(part.delta.y))
		
		return self
	
	async def hm_scroll_to_element(
			self,
			element: WEB_ELEMENT_TYPEHINT,
			additional_lower_y_offset: int = 0,
			additional_upper_y_offset: int = 0,
			additional_right_x_offset: int = 0,
			additional_left_x_offset: int = 0,
			origin: Optional[ScrollOrigin] = None,
	) -> Self:
		viewport_rect = await self._js_executor.get_viewport_rect()
		element_rect = await self._js_executor.get_element_rect_in_viewport(get_legacy_instance(element))
		
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
		
		return await self.hm_scroll(delta_x=delta_x, delta_y=delta_y, origin=origin)
	
	async def hm_text_input(self, text: str) -> Self:
		parts = await self._wrap_to_trio(text_input_to_parts, text=text)
		
		for part in parts:
			await self.pause(seconds=part.duration * 0.001)
			await self.send_keys(part.text)
		
		return self
