from _contextvars import ContextVar
from osn_selenium.trio_bidi._typehints import (
	CURRENT_BROWSING_CONTEXT_TYPEHINT
)


__all__ = ["CURRENT_BROWSING_CONTEXT"]

CURRENT_BROWSING_CONTEXT: ContextVar[CURRENT_BROWSING_CONTEXT_TYPEHINT] = ContextVar("current_browsing_context",


 default=None)
