import os
import pathlib
import sys

sys.path.append("..")

current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_dir) + "/../..")
from unittest import TestCase

from libs.sendmessage import SendMessage


class TestSendMessage(TestCase):
    toaddress = "ujimasa@hotmail.com"
    toaddress2 = "nishimuramasaki@gmail.com"
    subject = "TESTメール"
    txtmessage = """
    テストメールの改行付き
    送信者名
    http://google.co.jp
    """
    htmlmessage = "<h1>テストメールの改行付き</h1></br><p>送信者名</p>"
    mailtype = "html"

    """通常のプロバイダメールなど使用"""

    def test_sendmail_smtp(self):
        okmark = {}

        print("\nSend mail smtp text -->>")
        result = SendMessage().send_mail_smtp(
            self.toaddress, self.subject, self.txtmessage
        )
        self.assertEqual(result, okmark)
        print("Send mail smtp html -->>")
        result = SendMessage().send_mail_smtp(
            self.toaddress, self.subject, self.htmlmessage, self.mailtype
        )
        self.assertEqual(result, okmark)
        print("Send mail smtp exception -->>")
        with self.assertRaises(Exception, msg="send mail smtp exception!!"):
            SendMessage("test").send_mail_smtp(self.subject)

    """SendGridを使用したメール"""

    def test_sendmail_sendgrid(self):
        print("\nSend mail sendgrid text-->>")
        result = SendMessage().send_mail_sendgrid(
            self.toaddress2, self.subject, self.txtmessage
        )
        self.assertTrue(result)
        print("Send mail sendgrid html-->>")
        result = SendMessage().send_mail_sendgrid(
            self.toaddress2, self.subject, self.htmlmessage, self.mailtype
        )
        self.assertTrue(result)
        print("Send mail smtp exception -->>")
        with self.assertRaises(Exception, msg="send mail smtp exception!!"):
            SendMessage("test").send_mail_sendgrid(self.subject)

    """ Slack """

    def test_send_slack(self):
        print("\nSend Slack text only-->>")
        result = SendMessage().send_message_slack(self.txtmessage)
        self.assertTrue(result)
        print("Send Slack with one file -->>")
        filepath = [
            "/home/matarain/pythonapp/uhiimanbot/tests/testmaterials/images/image3.png"
        ]
        result = SendMessage().send_message_slack("テスト添付ファイル", filepath)
        self.assertTrue(result)
        print("Send Slack with multiple file -->>")
        path = "/home/matarain/pythonapp/uhiimanbot/tests/testmaterials/images"
        files = []
        for file in os.listdir(path):
            files.append(os.path.join(path, file))
        result = SendMessage().send_message_slack("テスト添付ファイル(複数)", files)
        self.assertTrue(result)
        print("Send slack exception -->>")
        with self.assertRaises(Exception, msg="send slack exception!!"):
            SendMessage("test").send_message_slack()

    """ テストメッセージ送信(ファイル) """

    def test_send_localfile(self):
        print("\nTest Message-->>")
        localfilepath = (
            "/home/matarain/pythonapp/uhiimanbot/tests/testmaterials/data/mail.txt"
        )
        mode = "test"
        toaddr = "sample@example.com"
        subject = "title"
        message = """
        Hello My name is Uhiimanbot
        http://google.com
        """
        SendMessage(mode).test_result_write(toaddr, subject, message)
        with open(localfilepath, "r") as f:
            result = f.read()
        self.assertRegex(result, toaddr)
        self.assertRegex(result, subject)
        self.assertRegex(result, message)
        with open(localfilepath, "r+") as f:
            f.truncate(0)
