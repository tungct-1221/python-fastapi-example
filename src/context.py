from contextvars import ContextVar
from typing import Optional


# add some context variables here
# Middleware
correlation_id_ctx: ContextVar[Optional[str]] = ContextVar("correlation_id_ctx", default=None)
process_time_ctx: ContextVar[Optional[str]] = ContextVar("process_time_ctx", default=None)
