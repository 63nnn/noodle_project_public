import logging


class FileLog:
    def __init__(self, logName, who, encoding="utf-8") -> None:
        self.logger = logging.getLogger(who)
        self.logger.setLevel(logging.DEBUG)  # DEBUG, INFO, WARNING, ERROR, CRITICAL
        self.filehandler = logging.FileHandler(logName, encoding=encoding)
        self.filehandlerformatter = logging.Formatter(
            "%(asctime)s, %(name)s, %(levelname)s, %(message)s",
            datefmt="%Y/%m/%d - %H:%M:%S",
        )
        self.filehandler.setFormatter(self.filehandlerformatter)

        if not any(
            isinstance(handler, logging.FileHandler) for handler in self.logger.handlers
        ):
            self.logger.addHandler(self.filehandler)

    def setLoggerLevel(self, level):
        """
        DEBUG, INFO, WARNING, ERROR, CRITICAL
        """
        level = str(level).upper()
        levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        try:
            self.logger.setLevel(levels[level])
        except:
            self.logger.error("setLoggerLevel value error")

    def getLoggerLevel(self):
        """get logger level"""
        return logging.root.level

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)
