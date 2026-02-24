from .custom_logger import CustomerLogger as _CustomLogger # backward compatibility
try:
    from .custom_logger import _CustomLogger
except Exception:
    CustomLogger = _CustomLogger

# Expose a global structlog-style logger used across the codebase
GLOBAL_LOGGER = CustomLogger().get_logger(__name__)