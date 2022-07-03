import sys
import logging


class SimpleLogFormatter(logging.Formatter):
    def_keys = [
        "name",
        "msg",
        "args",
        "levelname",
        "levelno",
        "pathname",
        "filename",
        "module",
        "exc_info",
        "exc_text",
        "stack_info",
        "lineno",
        "funcName",
        "created",
        "msecs",
        "relativeCreated",
        "thread",
        "correlation_id" "threadName",
        "processName",
        "process",
        "message",
        "extra_data",
    ]

    def __init__(self, fmt=None, datefmt=None, style="%", validate=True):
        super().__init__(fmt, datefmt, style, validate)

    def format(self, record):
        string = super().format(record)
        return string


class Logger:
    def __init__(self, logLevel: str = "INFO"):
        FORMAT = """created="%(asctime)s" level=%(levelname)s
         message="%(message)s" correlation_id=%(correlation_id)s"""
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            logger.setLevel(logging.DEBUG)
            sh = logging.StreamHandler(sys.stdout)
            formatter = SimpleLogFormatter(FORMAT)
            sh.setFormatter(formatter)
            sh.setLevel(logging.getLevelName(logLevel))
            logger.addHandler(sh)
            logger.propagate = False
        self.log = logger

    def info(self, msg: str, traceId: str = "") -> None:
        extra = {"correlation_id": traceId}
        self.log.info(msg=msg, extra=extra)

    def error(self, msg: str, traceId: str = "") -> None:
        extra = {"correlation_id": traceId}
        self.log.error(msg=msg, extra=extra)

    def exception(self, msg: str, traceId: str = "", exc_info=None) -> None:
        extra = {"correlation_id": traceId}
        self.log.exception(msg=msg, extra=extra)

    def debug(self, msg: str, traceId: str = "") -> None:
        extra = {"correlation_id": traceId}
        self.log.debug(msg=msg, extra=extra)
