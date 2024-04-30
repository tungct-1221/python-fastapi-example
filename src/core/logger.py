# reference the asgi_correlation_id package

from logging import Filter
from typing import TYPE_CHECKING, Optional

from context import correlation_id_ctx

if TYPE_CHECKING:
    from logging import LogRecord


def _trim_string(string: Optional[str], string_length: Optional[int]) -> Optional[str]:
    return string[:string_length] if string_length is not None and string else string


# Middleware
class CorrelationIdFilter(Filter):
    """Logging filter to attached correlation IDs to log records"""

    def __init__(self, name: str = "", uuid_length: Optional[int] = None, default_value: Optional[str] = None):
        super().__init__(name=name)
        self.uuid_length = uuid_length
        self.default_value = default_value

    def filter(self, record: "LogRecord") -> bool:
        """
        Attach a correlation ID to the log record.

        Since the correlation ID is defined in the middleware layer, any
        log generated from a request after this point can easily be searched
        for, if the correlation ID is added to the message, or included as
        metadata.
        """
        cid = correlation_id_ctx.get(self.default_value)
        record.correlation_id = _trim_string(cid, self.uuid_length)
        return True
