from abc import ABC, abstractmethod
from typing import Optional, Sequence, TYPE_CHECKING

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.shadowroot import ShadowRoot as legacyShadowRoot


if TYPE_CHECKING:
    from osn_selenium.abstract.instances.web_element import AbstractWebElement


class AbstractShadowRoot(ABC):
    """
    Abstract base class for a shadow root.

    Defines the interface for finding elements within a shadow DOM.
    """

    @abstractmethod
    def legacy(self) -> legacyShadowRoot:
        """
        Returns the underlying legacy Selenium ShadowRoot instance.

        This provides a way to access the original Selenium object for operations
        not covered by this abstract interface.

        Returns:
            legacyShadowRoot: The legacy Selenium ShadowRoot object.
        """
        ...

    @property
    @abstractmethod
    def id(self) -> str:
        """
        The ID of the shadow root.

        Returns:
            str: The unique identifier for the shadow root.
        """
        ...

    @abstractmethod
    def find_elements(
        self,
        by: By = By.ID,
        value: Optional[str] = None,
    ) -> Sequence["AbstractWebElement"]:
        """
        Find all elements within the shadow root's context.

        Args:
            by (By): The strategy to use for finding elements.
            value (Optional[str]): The value of the locator.

        Returns:
            Sequence["AbstractWebElement"]: A sequence of found WebElements.
        """
        ...

    @abstractmethod
    def find_element(
        self,
        by: By = By.ID,
        value: Optional[str] = None,
    ) -> "AbstractWebElement":
        """
        Find an element within the shadow root's context.

        Args:
            by (By): The strategy to use for finding the element.
            value (Optional[str]): The value of the locator.

        Returns:
            "AbstractWebElement": The found WebElement.
        """
        ...
