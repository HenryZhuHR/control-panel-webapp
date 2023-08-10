import logging
import socket


class CustomLogger(object):
    def __init__(self, **kwargs):
        pass

    def info(self,  msg, *args, **kwargs):
        print(msg)

    def debug(self, msg, *args, **kwargs):
        print(msg)

    def warning(self, msg, *args, **kwargs):
        print(msg)

    def warn(self, msg, *args, **kwargs):
        print(msg)

    def error(self, msg, *args, **kwargs):
        print(msg)

    def exception(self, msg, *args, **kwargs):
        print(msg)

    def critical(self, msg, *args, **kwargs):
        pass

    def log(self, level, msg, *args, **kwargs):
        print(msg)


def host_log_adapter(logger):
    hostname = {"hostname": socket.gethostname()}
    return logging.LoggerAdapter(logger, hostname)


def get_logger(log_name, level=logging.DEBUG):
    logger = logging.getLogger(log_name)
    logger.setLevel(level=level)
    return host_log_adapter(logger)
