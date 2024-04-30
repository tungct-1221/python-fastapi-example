from typing import Any


LOGGING_CONFIG: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "correlation_id": {
            "()": "asgi_correlation_id.CorrelationIdFilter",
            "uuid_length": 32,
            "default_value": "-",
        },
    },
    "formatters": {
        "web": {
            "class": "logging.Formatter",
            "datefmt": "%H:%M:%S",
            "format": "%(levelname)s ... [%(correlation_id)s] %(name)s %(message)s",
        },
    },
    "handlers": {
        "web": {
            "class": "logging.StreamHandler",
            "filters": ["correlation_id"],
            "formatter": "web",
        },
    },
    "loggers": {
        "my_project": {
            "handlers": ["web"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
