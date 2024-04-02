async def __init__(hub):
    hub.log.LOGGER = {}
    hub.log.FILE_HANDLER = None
    hub.log.STREAM_HANDLER = None
    hub.log.LEVEL = {
        "notset": hub.lib.logging.NOTSET,
        "trace": 5,
        "debug": hub.lib.logging.DEBUG,
        "info": hub.lib.logging.INFO,
        "warn": hub.lib.logging.WARN,
        "warning": hub.lib.logging.WARNING,
        "error": hub.lib.logging.ERROR,
        "fatal": hub.lib.logging.FATAL,
        "critical": hub.lib.logging.CRITICAL,
    }
