from abc import ABC, abstractmethod
from typing import Any, Mapping, Optional, Self, Sequence

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement as legacyWebElement

from osn_selenium.abstract.instances.shadow_root import AbstractShadowRoot


class AbstractWebElement(ABC):
    """
    Abstract base class for a web element.

    Defines the interface for interacting with an element on a web page,
    such as clicking, sending keys, and retrieving attributes.
    """

    @abstractmethod
    def legacy(self) -> legacyWebElement:
        """
        Returns the underlying legacy Selenium WebElement instance.

        This provides a way to access the original Selenium object for operations
        not covered by this abstract interface.

        Returns:
            legacyWebElement: The legacy Selenium WebElement object.
        """
        ...

    @abstractmethod
    def __eq__(self, element: Self) -> bool:
        """
        Checks if two elements are equal.

        Args:
            element (Self): The element to compare with.

        Returns:
            bool: True if the elements are the same, False otherwise.
        """
        ...

    @abstractmethod
    def __hash__(self) -> int:
        """
        Returns the hash of the element's ID.

        Returns:
            int: The hash value.
        """
        ...

    @abstractmethod
    def __ne__(self, element: Self) -> bool:
        """
        Checks if two elements are not equal.

        Args:
            element (Self): The element to compare with.

        Returns:
            bool: True if the elements are not the same, False otherwise.
        """
        ...

    @abstractmethod
    def __repr__(self) -> str:
        """
        Returns a string representation of the WebElement.

        Returns:
            str: The string representation.
        """
        ...

    @abstractmethod
    def text(self) -> str:
        """
        The text of the element.
        """
        ...

    @abstractmethod
    def tag_name(self) -> str:
        """
        The tag name of this element.
        """
        ...

    @abstractmethod
    def size(self) -> Mapping[str, int]:
        """
        The size of the element.
        """
        ...

    @abstractmethod
    def shadow_root(self) -> AbstractShadowRoot:
        """
        The shadow root of this element.
        """
        ...

    @abstractmethod
    def session_id(self) -> str:
        """
        The session ID of the WebDriver controlling this element.
        """
        ...

    @abstractmethod
    def screenshot_as_png(self) -> bytes:
        """
        A PNG image of the element, as binary data.
        """
        ...

    @abstractmethod
    def screenshot_as_base64(self) -> str:
        """
        A base64-encoded PNG image of the element.
        """
        ...

    @abstractmethod
    def rect(self) -> Mapping[str, int]:
        """
        A dictionary with the size and location of the element.
        """
        ...

    @abstractmethod
    def parent(self) -> Self:
        """
        The parent of this element (the WebDriver instance).
        """
        ...

    @abstractmethod
    def location_once_scrolled_into_view(self) -> Mapping[str, int]:
        """
        The location of the element after scrolling it into view.
        """
        ...

    @abstractmethod
    def location(self) -> Mapping[str, int]:
        """
        The location of the element in the renderable canvas.
        """
        ...

    @abstractmethod
    def id(self) -> str:
        """
        The internal ID used by the WebDriver.
        """
        ...

    @abstractmethod
    def aria_role(self) -> str:
        """
        The ARIA role of the element.
        """
        ...

    @abstractmethod
    def accessible_name(self) -> str:
        """
        The accessible name of the element.
        """
        ...

    @abstractmethod
    def value_of_css_property(self, property_name: str) -> str:
        """
        The value of a CSS property.

        Args:
            property_name (str): The name of the CSS property.

        Returns:
            str: The value of the property.
        """
        ...

    @abstractmethod
    def submit(self) -> None:
        """
        Submits a form.
        """
        ...

    @abstractmethod
    def send_keys(self, *value: str) -> None:
        """
        Simulates typing into the element.

        Args:
            *value (str): A sequence of strings to send.
        """
        ...

    @abstractmethod
    def screenshot(self, filename: str) -> bool:
        """
        Saves a screenshot of the element to a file.

        Args:
            filename (str): The full path of the file.

        Returns:
            bool: True if successful, False otherwise.
        """
        ...

    @abstractmethod
    def is_selected(self) -> bool:
        """
        Whether the element is selected.

        Returns:
            bool: True if the element is selected, False otherwise.
        """
        ...

    @abstractmethod
    def is_enabled(self) -> bool:
        """
        Whether the element is enabled.

        Returns:
            bool: True if the element is enabled, False otherwise.
        """
        ...

    @abstractmethod
    def is_displayed(self) -> bool:
        """
        Whether the element is visible to a user.

        Returns:
            bool: True if the element is displayed, False otherwise.
        """
        ...

    @abstractmethod
    def get_property(self, name: str) -> Any:
        """
        Gets the given property of the element.

        Args:
            name (str): The name of the property.

        Returns:
            Any: The value of the property.
        """
        ...

    @abstractmethod
    def get_dom_attribute(self, name: str) -> Optional[str]:
        """
        Gets the given attribute of the element from the DOM.

        Args:
            name (str): The name of the attribute.

        Returns:
            Optional[str]: The value of the attribute, or None if it does not exist.
        """
        ...

    @abstractmethod
    def get_attribute(self, name: str) -> Optional[str]:
        """
        Gets the given attribute or property of the element.

        Args:
            name (str): The name of the attribute/property.

        Returns:
            Optional[str]: The value of the attribute/property, or None if it does not exist.
        """
        ...

    @abstractmethod
    def find_elements(
        self,
        by: str = By.ID,
        value: Optional[str] = None,
    ) -> Sequence[Self]:
        """
        Finds all child elements within this element's context.

        Args:
            by (str): The strategy to use for finding elements.
            value (Optional[str]): The value of the locator.

        Returns:
            Sequence[Self]: A sequence of found WebElements.
        """
        ...

    @abstractmethod
    def find_element(
        self,
        by: str = By.ID,
        value: Optional[str] = None,
    ) -> Self:
        """
        Finds a child element within this element's context.

        Args:
            by (str): The strategy to use for finding the element.
            value (Optional[str]): The value of the locator.

        Returns:
            AbstractWebElement: The found WebElement.
        """
        ...

    @abstractmethod
    def click(self) -> None:
        """
        Clicks the element.
        """
        ...

    @abstractmethod
    def clear(self) -> None:
        """
        Clears the text if it's a text entry element.
        """
        ...
