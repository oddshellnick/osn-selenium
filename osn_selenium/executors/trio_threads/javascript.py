from typing import Any, Awaitable, Callable, Dict, Optional

from selenium.webdriver.remote.webelement import WebElement

from osn_selenium.abstract.executors.javascript import AbstractJSExecutor
from osn_selenium.types import Position, Rectangle, Size
from osn_selenium.webdrivers.types import Point


class JSExecutor(AbstractJSExecutor):
    def __init__(self, execute_function: Callable[..., Awaitable[Any]]):
        super().__init__(
                execute_function=execute_function,
        )

    async def execute(self, script: str, *args: Any) -> Any:
        return await self._execute_function(script, *args)

    async def check_element_in_viewport(self, element: WebElement) -> bool:
        return await self.execute(
            self._scripts.check_element_in_viewport,
            element
        )

    async def get_document_scroll_size(self) -> Size:
        size = await self.execute(self._scripts.get_document_scroll_size)

        return Size(width=int(size["width"]), height=int(size["height"]))

    async def get_element_css_style(
        self,
        element: WebElement
    ) -> Dict[str, str]:
        return await self.execute(self._scripts.get_element_css, element)

    async def get_element_rect_in_viewport(
        self,
        element: WebElement
    ) -> Optional[Rectangle]:
        rect = await self.execute(
            self._scripts.get_element_rect_in_viewport,
            element
        )

        if rect is not None:
            return Rectangle(
                x=int(rect["x"]),
                y=int(rect["y"]),
                width=int(rect["width"]),
                height=int(rect["height"]),
            )

        return rect

    async def get_random_element_point_in_viewport(
        self,
        element: WebElement,
        step: int = 1
    ) -> Optional[Position]:
        position = await self.execute(
            self._scripts.get_random_element_point_in_viewport,
            element,
            step
        )

        if position is not None:
            return Position(x=int(position["x"]), y=int(position["y"]))

        return None

    async def get_random_element_point(
        self,
        element: WebElement
    ) -> Optional[Point]:
        point_in_viewport = await self.get_random_element_point_in_viewport(
            element=element,
            step=1
        )

        if point_in_viewport is not None:
            element_viewport_pos = await self.get_element_rect_in_viewport(
                element=element
            )

            if element_viewport_pos is not None:
                x = int(element_viewport_pos.x + point_in_viewport.x)
                y = int(element_viewport_pos.y + point_in_viewport.y)

                return Point(x=x, y=y)

        return None

    async def get_viewport_position(self) -> Position:
        position = await self.execute(self._scripts.get_viewport_position)

        return Position(x=int(position["x"]), y=int(position["y"]))

    async def get_viewport_rect(self) -> Rectangle:
        rect = await self.execute(self._scripts.get_viewport_rect)

        return Rectangle(
            x=int(rect["x"]),
            y=int(rect["y"]),
            width=int(rect["width"]),
            height=int(rect["height"]),
        )

    async def get_viewport_size(self) -> Size:
        size = await self.execute(self._scripts.get_viewport_size)

        return Size(width=int(size["width"]), height=int(size["height"]))

    async def open_new_tab(self, link: str = "") -> None:
        await self.execute(self._scripts.open_new_tab, link)

    async def stop_window_loading(self) -> None:
        await self.execute(self._scripts.stop_window_loading)
