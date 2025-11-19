from typing import Any, Callable, Dict, Optional

from selenium.webdriver.remote.webelement import WebElement

from osn_selenium.abstract.executors.javascript import AbstractJSExecutor
from osn_selenium.types import Position, Rectangle, Size
from osn_selenium.webdrivers.types import Point


class JSExecutor(AbstractJSExecutor):
    def __init__(self, execute_function: Callable[..., Any]):
        super().__init__(
                execute_function=execute_function,
        )

    def execute(self, script: str, *args: Any) -> Any:
        return self._execute_function(script, *args)

    def check_element_in_viewport(self, element: WebElement) -> bool:
        return self.execute(self._scripts.check_element_in_viewport, element)

    def get_document_scroll_size(self) -> Size:
        size = self.execute(self._scripts.get_document_scroll_size)

        return Size(width=int(size["width"]), height=int(size["height"]))

    def get_element_css_style(self, element: WebElement) -> Dict[str, str]:
        return self.execute(self._scripts.get_element_css, element)

    def get_element_rect_in_viewport(self, element: WebElement) -> Rectangle:
        rect = self.execute(self._scripts.get_element_rect_in_viewport, element)

        return Rectangle(
            x=int(rect["x"]),
            y=int(rect["y"]),
            width=int(rect["width"]),
            height=int(rect["height"]),
        )

    def get_random_element_point_in_viewport(
        self,
        element: WebElement,
        step: int = 1
    ) -> Optional[Position]:
        position = self.execute(
            self._scripts.get_random_element_point_in_viewport,
            element,
            step
        )

        if position is not None:
            return Position(x=int(position["x"]), y=int(position["y"]))

        return None

    def get_random_element_point(self, element: WebElement) -> Point:
        point_in_viewport = self.get_random_element_point_in_viewport(
            element=element,
            step=1
        )

        element_viewport_pos = self.get_element_rect_in_viewport(
            element=element
        )

        x = int(element_viewport_pos.x + point_in_viewport.x)
        y = int(element_viewport_pos.y + point_in_viewport.y)

        return Point(x=x, y=y)

    def get_viewport_position(self) -> Position:
        position = self.execute(self._scripts.get_viewport_position)

        return Position(x=int(position["x"]), y=int(position["y"]))

    def get_viewport_rect(self) -> Rectangle:
        rect = self.execute(self._scripts.get_viewport_rect)

        return Rectangle(
            x=int(rect["x"]),
            y=int(rect["y"]),
            width=int(rect["width"]),
            height=int(rect["height"]),
        )

    def get_viewport_size(self) -> Size:
        size = self.execute(self._scripts.get_viewport_size)

        return Size(width=int(size["width"]), height=int(size["height"]))

    def open_new_tab(self, link: str = "") -> None:
        self.execute(self._scripts.open_new_tab, link)

    def stop_window_loading(self) -> None:
        self.execute(self._scripts["stop_window_loading"])
