import traceback

from libs.applicationlogs import ApplicationLogs
from libs.configreader import Configreader
from libs.datacrud import Datacrud
from libs.sendmessage import SendMessage


class AfterOperationProcessing:
    def __init__(self, mode: str = "prod", destinationtype: str = "mongo"):
        self.mode = mode
        name = __name__
        logmode = "prod"
        self.loglevel = "CRITICAL"
        self.config = Configreader(mode)
        self.logpath = self.config.get_filepath("applog")
        self.applog = ApplicationLogs(name, logmode, self.logpath)
        self.datacrud = Datacrud(mode, destinationtype)
        self.sendmessage = SendMessage(mode)
        self.destinationtype = destinationtype

    """ Delete submitted data """

    def submitted_post_delete(self) -> bool:
        try:
            delete_condition = {"wordcloud": "completed"}
            self.datacrud.delete_data(delete_condition)
            return True
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("submitted post exception!!")

    """ Find the word ERROR in the log file """

    def checked_log_normalization(self) -> bool:
        try:
            with open(self.logpath, mode="r") as log_file:
                log_contents = log_file.read()
                if "ERROR" in log_contents or "CRITICAL" in log_contents:
                    return False
            return True
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("checked log normalization!!")

    """ notification of error contents """

    def notification_error_sending(self):
        try:
            with open(self.logpath, mode="r") as f:
                log_contents = f.read()
            subject = "【Alert】uhiiman_bot processing error"
            comment = "An error has occurred. Please investigate and respond."
            targetaddress = "ujimasa@hotmail.com"
            mail_body = comment + "\n-----------------------\n" + log_contents
            if self.mode == "prod":
                self.sendmessage.send_mail_smtp(targetaddress, subject, mail_body)
            else:
                self.sendmessage.test_result_write(targetaddress, subject, mail_body)
            return True
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("notification error sending!!")

    def main(self):
        try:
            result = self.checked_log_normalization()
            if result is False:
                self.notification_error_sending()
            with open(self.logpath, mode="r+") as log_file:
                log_file.truncate(0)
            self.submitted_post_delete()
            return True
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("AfterOperationProcessing exception!!")
