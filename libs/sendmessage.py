import json
import os
import smtplib
import traceback
from email.mime.text import MIMEText

import requests

from .applicationlogs import ApplicationLogs
from .configreader import Configreader


class SendMessage:
    def __init__(self, mode: str = "prod"):
        self.mode = mode
        name = __name__
        logmode = "prod"
        self.loglevel = "CRITICAL"
        self.config = Configreader(mode)
        logpath = self.config.get_filepath("applog")
        self.applog = ApplicationLogs(name, logmode, logpath)
        self.smtpauth = self.config.get_message_auth("smtp")
        self.sendgridauth = self.config.get_message_auth("sendgrid")
        self.slackauth = self.config.get_message_auth("slack")

    """ Sending E-mails with an SMTP Server """

    def send_mail_smtp(
        self, toaddress: str, subject: str, message: str, mailtype: str = None
    ) -> bool:
        try:
            msg = MIMEText(message, mailtype or "plain")
            msg["From"] = self.smtpauth["from"]
            msg["To"] = toaddress
            msg["Subject"] = subject
            server = smtplib.SMTP(self.smtpauth["server"], self.smtpauth["port"])
            if server.has_extn("STARTTLS"):
                server.starttls()

            server.login(self.smtpauth["user"], self.smtpauth["password"])
            result = server.sendmail(self.smtpauth["from"], toaddress, msg.as_string())
            server.quit()
            return result
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("send mail smtp exception!!")

    """ Sending E-mails with an SendGrid """

    def send_mail_sendgrid(
        self, toaddress: str, subject: str, content: str, mailtype: str = None
    ) -> bool:
        try:
            url = "https://api.sendgrid.com/v3/mail/send"
            if mailtype == "html":
                content_type = "text/html"
            else:
                content_type = "text/plain"
            headers = {
                "Authorization": f"Bearer {self.sendgridauth['apikey']}",
                "Content-Type": "application/json",
            }

            data = {
                "personalizations": [
                    {
                        "to": [{"email": toaddress}],
                        "subject": subject,
                    }
                ],
                "from": {"email": self.sendgridauth["from"]},
                "content": [{"type": content_type, "value": content}],
            }

            response = requests.post(url, headers=headers, data=json.dumps(data))

            if response.status_code == 202:
                return True
            else:
                self.applog.output_log("WARNING", response.json())
                return False
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("send mail sendgrid exception!!")

    """ Sending Message with Slack """

    def send_message_slack(self, message: str, filepaths: list = None):
        try:
            if filepaths:
                self._send_message_slack_with_files(message, filepaths)
            else:
                self._send_message_slack_without_files(message)
            return True
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("send slack exception!!")

    def _send_message_slack_with_files(self, message: str, filepaths: list):
        url = "https://slack.com/api/files.upload"
        initial_comment = {"initial_comment": message}
        headers = {"Authorization": "Bearer " + self.slackauth["token"]}

        for i, filepath in enumerate(filepaths):
            data = {"channels": self.slackauth["channel"]}
            with open(filepath, "rb") as file:
                file_data = file.read()
                files = {
                    "file": (filepath, file_data),
                }
            filename = os.path.basename(filepath)
            title = {"title": f"attachment files {i+1} - {filename}"}
            if i == 0:
                data.update(initial_comment)
                data.update(title)
            else:
                data.update(title)
            response = requests.post(url, headers=headers, data=data, files=files)

            if response.status_code != 200:
                self.applog.output_log("WARNING", response.json())

    def _send_message_slack_without_files(self, message: str):
        url = "https://slack.com/api/chat.postMessage"
        data = {
            "channel": self.slackauth["channel"],
            "as_user": "Uhiimanbot",
            "text": message,
        }

        headers = {"Authorization": "Bearer " + self.slackauth["token"]}
        response = requests.post(url, headers=headers, data=data)

        if response.status_code != 200:
            self.applog.output_log("WARNING", response.json())

    """ For final output during testing """

    def test_result_write(
        self, toaddres: str, subject: str = None, message: str = None
    ):
        try:
            filepath = self.config.get_filepath("mailpost")
            with open(filepath, mode="a") as f:
                f.write(f"to:{toaddres}\n")
                f.write(f"subject:{subject}\n")
                f.write(message)
                f.write("\n")
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("send test output exception!!")
