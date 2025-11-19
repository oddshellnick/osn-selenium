from typing import Any, Optional

from pydantic import Field

from osn_selenium.types import DictModel, ExtraDictModel


class ArgumentValue(DictModel):
    """
    Command-line argument structure.

    Attributes:
        command_line (str): The command-line string.
        value (Any): Value associated with the argument.
    """

    command_line: str
    value: Any


class ExperimentalOptionValue(DictModel):
    """
    Experimental option structure.

    Attributes:
        option_name (str): Option name.
        value (Any): Option value.
    """

    option_name: str
    value: Any


class AttributeValue(DictModel):
    """
    WebDriver attribute structure.

    Attributes:
        attribute_name (str): Attribute name.
        value (Any): Attribute value.
    """

    attribute_name: str
    value: Any


class FlagTypeNotDefined:
    """
    Sentinel indicating missing flag type definition.
    """

    pass


class BrowserExperimentalOptions(ExtraDictModel):
    """
    WebDriver experimental options for browser.
    """

    pass


class BrowserAttributes(ExtraDictModel):
    """
    WebDriver attributes for browser.

    Attributes:
        enable_bidi (Optional[bool]): Enable/disable BiDi protocol.
    """

    enable_bidi: Optional[bool] = None


class BrowserArguments(ExtraDictModel):
    """
    WebDriver command-line arguments.

    Attributes:
        se_downloads_enabled (Optional[bool]): Enable Selenium downloads.
    """

    se_downloads_enabled: Optional[bool] = None


class BrowserFlags(DictModel):
    """
    Combined structure of all browser flags.

    Attributes:
        argument (BrowserArguments): Command-line arguments.
        experimental_option (BrowserExperimentalOptions): Experimental options.
        attribute (BrowserAttributes): WebDriver attributes.
    """

    argument: BrowserArguments = Field(default_factory=BrowserArguments)
    experimental_option: BrowserExperimentalOptions = Field(default_factory=BrowserExperimentalOptions)
    attribute: BrowserAttributes = Field(default_factory=BrowserAttributes)


def _argument_to_flag(argument: ArgumentValue) -> str:
    """
    Format a command-line argument.

    Args:
        argument (ArgumentValue): Argument to format.

    Returns:
        str: Formatted argument.
    """

    if "{value}" in argument.command_line:
        return argument.command_line.format(value=argument.value)

    return argument.command_line


BrowserArguments.model_rebuild()
BrowserExperimentalOptions.model_rebuild()
BrowserAttributes.model_rebuild()
BrowserFlags.model_rebuild()
