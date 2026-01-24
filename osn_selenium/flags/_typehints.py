from selenium import webdriver
from typing import (
	Any,
	Literal,
	Mapping,
	Union
)


__all__ = [
	"AutoplayPolicyType",
	"LogLevelType",
	"UseGLType",
	"ValidAutoplayPolicies",
	"ValidLogLevels",
	"ValidUseGLs",
	"any_flags_mapping",
	"any_webdriver_option_type",
	"blink_webdriver_option_type"
]

AutoplayPolicyType = Literal["user-gesture-required", "no-user-gesture-required"]
ValidAutoplayPolicies = ["user-gesture-required", "no-user-gesture-required"]

LogLevelType = Literal[0, 1, 2, 3]
ValidLogLevels = [0, 1, 2, 3]

UseGLType = Literal["desktop", "egl", "swiftshader"]
ValidUseGLs = ["desktop", "egl", "swiftshader"]

any_flags_mapping = Mapping[str, Any]

any_webdriver_option_type = Union[webdriver.ChromeOptions, webdriver.EdgeOptions]
blink_webdriver_option_type = Union[webdriver.ChromeOptions, webdriver.EdgeOptions]
