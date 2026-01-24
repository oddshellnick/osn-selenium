from selenium import webdriver
from typing import (
	Any,
	Literal,
	Mapping,
	Union
)


__all__ = [
	"ANY_FLAGS_TYPEHINT",
	"ANY_WEBDRIVER_OPTION_TYPEHINT",
	"AUTOPLAY_POLICY_TYPEHINT",
	"BLINK_WEBDRIVER_OPTION_TYPEHINT",
	"LOG_LEVEL_TYPEHINT",
	"USE_GL_TYPEHINT",
	"VALID_AUTOPLAY_POLICIES",
	"VALID_LOG_LEVELS",
	"VALID_USE_GLS"
]

AUTOPLAY_POLICY_TYPEHINT = Literal["user-gesture-required", "no-user-gesture-required"]
VALID_AUTOPLAY_POLICIES = ["user-gesture-required", "no-user-gesture-required"]

LOG_LEVEL_TYPEHINT = Literal[0, 1, 2, 3]
VALID_LOG_LEVELS = [0, 1, 2, 3]

USE_GL_TYPEHINT = Literal["desktop", "egl", "swiftshader"]
VALID_USE_GLS = ["desktop", "egl", "swiftshader"]

ANY_FLAGS_TYPEHINT = Mapping[str, Any]

ANY_WEBDRIVER_OPTION_TYPEHINT = Union[webdriver.ChromeOptions, webdriver.EdgeOptions]
BLINK_WEBDRIVER_OPTION_TYPEHINT = Union[webdriver.ChromeOptions, webdriver.EdgeOptions]
