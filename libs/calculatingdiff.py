import datetime
import random
import time
import traceback

from .applicationlogs import ApplicationLogs
from .configreader import Configreader


class CalculatingDifference:
    def __init__(self, mode: str = "prod"):
        self.mode = mode
        name = __name__
        logmode = "prod"
        self.loglevel = "CRITICAL"
        config = Configreader(mode)
        logpath = config.get_filepath("applog")
        self.applog = ApplicationLogs(name, logmode, logpath)

    """ get interval time """

    def get_intervaltime(self, reccount: int = None, settime=datetime.datetime.now()):
        try:
            nowtime = settime
            period = 1
            MAX_TIME = 60
            START_NUM = 5
            maxsec = 10
            # Find the number of seconds remaining from the current time to
            # the next 00 minutes
            timeonhourafter = nowtime + datetime.timedelta(hours=period)
            stronehourafter = timeonhourafter.strftime("%Y-%m-%d %H:00:%S")
            onehourafter = datetime.datetime.strptime(
                stronehourafter, "%Y-%m-%d %H:%M:%S"
            )
            delta = onehourafter - nowtime
            remaintime = delta.seconds
            # Maximum number of seconds to be set if the remaining time is more than
            #  60 seconds and the number of records is in the range of 60 seconds.
            if remaintime > MAX_TIME and 0 < reccount < 60:
                maxsec = remaintime / reccount
            # If it is 59 minutes every hour, the RSS feed acquisition process will run,
            # so the acquisition time will be waited.
            if int(maxsec) < 120 and nowtime.minute < 59:
                exitnum = int(maxsec)
            elif nowtime.minute == 59:
                time.sleep(100)
                exitnum = 60
            else:
                exitnum = 90
            result = random.randint(START_NUM, exitnum)
            return result
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("get intervaltime exception!!")

    """ Produce a difference compared """

    def get_diffids(self, idlists1: list = None, idlists2: list = None) -> list:
        try:
            result = list(set(idlists1 + idlists2) ^ set(idlists2))
            return result
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("get ids exception!!")
