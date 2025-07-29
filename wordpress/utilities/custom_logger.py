# utilities/custom_logger.py
import atexit
import logging
from logging.handlers import RotatingFileHandler
from typing import Dict

_LOGGERS: Dict[str, logging.Logger] = {}
_ROOT_CLOSED = False

def _close_logger_handlers(logger: logging.Logger):
    """Close all handlers (important on Windows to release file locks)."""
    for h in list(logger.handlers):
        try:
            h.flush()
            h.close()
        except Exception:
            pass
    logger.handlers.clear()

def customLogger(
    name: str = "framework",
    log_file: str = "automation.log",
    level: int = logging.DEBUG
) -> logging.Logger:
    """
    Create/fetch a  logger by name with a RotatingFileHandler.
    - Uses delay=True to avoid pre-opening the file (helps on Windows).
    - Ensures only one file handler per named logger.
    - Closes handlers on exit to avoid file locks during rotation.
    Back-compat: if called like customLogger(logging.INFO) treat first arg as level.
    """
    # Back-compat: first positional arg was level int
    if isinstance(name, int):
        level = name
        name = "framework"

    # Return existing logger if already created
    if name in _LOGGERS:
        return _LOGGERS[name]

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False  # avoid duplicate output via root logger

    # Avoid multiple file handlers
    has_file_handler = any(isinstance(h, RotatingFileHandler) for h in logger.handlers)
    if not has_file_handler:
        fh = RotatingFileHandler(
            log_file,
            mode="a",
            maxBytes=2_000_000,
            backupCount=3,
            encoding="utf-8",
            delay=True,            # CRITICAL for Windows: open file lazily
        )
        fh.setLevel(level)
        fmt = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s: %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S %p",
        )
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    # Console handler (info+)
    has_console = any(isinstance(h, logging.StreamHandler) and not isinstance(h, RotatingFileHandler)
                      for h in logger.handlers)
    if not has_console:
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        fmt = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s: %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S %p",
        )
        ch.setFormatter(fmt)
        logger.addHandler(ch)

    # Register atexit closer once per logger
    @atexit.register
    def _close_on_exit():
        global _ROOT_CLOSED
        if not _ROOT_CLOSED:
            for lg in list(_LOGGERS.values()):
                _close_logger_handlers(lg)
            _ROOT_CLOSED = True

    _LOGGERS[name] = logger
    return logger
