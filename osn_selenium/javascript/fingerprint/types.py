from typing import Union
from osn_selenium.javascript.fingerprint.spoof.rules import (
	CustomRule,
	RandomArrayNoiseRule,
	RandomArraySetRule,
	RandomItemNoiseRule,
	RandomItemSetRule,
	StaticArrayNoiseRule,
	StaticArraySetRule,
	StaticItemNoiseRule,
	StaticItemSetRule
)


__all__ = ["SPOOF_RULE_TYPEHINT"]

SPOOF_RULE_TYPEHINT = Union[
	StaticItemSetRule,
	RandomItemSetRule,
	StaticArraySetRule,
	RandomArraySetRule,
	StaticItemNoiseRule,
	RandomItemNoiseRule,
	StaticArrayNoiseRule,
	RandomArrayNoiseRule,
	CustomRule
]
