import logging
import traceback


class ApplicationLogs:
    def __init__(self, name: str = None, mode: str = "prod", filepath: str = None):
        self.name = name
        self.mode = mode
        self.path = filepath

    def output_log(self, loglevel: str = None, logbody: str = None):
        try:
            logger = logging.getLogger(self.name)
            logger.setLevel(loglevel)
            handler_format = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "%Y-%m-%dT%H:%M:%S",
            )
            if self.mode == "test":
                stream_handler = logging.StreamHandler()
                stream_handler.setFormatter(handler_format)
                logger.addHandler(stream_handler)
            else:
                file_handler = logging.FileHandler(self.path)
                file_handler.setFormatter(handler_format)
                logger.addHandler(file_handler)
            logfuncdict = {
                "DEBUG": "logger.debug",
                "INFO": "logger.info",
                "WARNING": "logger.warning",
                "ERROR": "logger.error",
                "CRITICAL": "logger.critical",
            }
            funcstr = logfuncdict[loglevel]
            eval(funcstr)(logbody)
            name = logger.name
            if self.mode == "test":
                stream_handler.close()
            else:
                file_handler.close()
            del logging.Logger.manager.loggerDict[name]
        except Exception:
            print(traceback.format_exc())
            raise Exception("Generate log exception!!")
