import io
import os
import pathlib
import subprocess
import sys
from unittest import TestCase

sys.path.append("..")
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_dir) + "/../..")
from libs.applicationlogs import ApplicationLogs


class TestApplicationLogs(TestCase):
    logpath = "/home/matarain/pythonapp/uhiimanbot/tests/testmaterials/logs/app.log"
    """ common """

    def get_console_log(self, name, mode, loglevel, logbody):
        with io.StringIO() as c:
            sys.stdout = c
            applications = ApplicationLogs(name, mode, self.logpath)
            applications.output_log(loglevel, logbody)
            result = c.getvalue()
            sys.stdout = sys.__stdout__
            return result

    """ モード変更確認 """

    def test_output_log_mode(self):
        name = "test_output_log_mode"
        mode = "test"
        loglevel = "INFO"
        logbody = "information log"
        result = self.get_console_log(name, mode, loglevel, logbody)
        self.assertIn(result, loglevel)

    """ ログ出力確認 """

    def test_output_log_file(self):
        name = "test_output_log_file"
        mode = "dev"
        valuedictarray = [
            {"logbody": "debug log", "loglevel": "DEBUG"},
            {"logbody": "info log", "loglevel": "INFO"},
            {"logbody": "warning log", "loglevel": "WARNING"},
            {"logbody": "error log", "loglevel": "ERROR"},
            {"logbody": "critical log", "loglevel": "CRITICAL"},
        ]
        with open(self.logpath, "a", newline="") as f:
            f.truncate(0)
        applications = ApplicationLogs(name, mode, self.logpath)
        for vd in valuedictarray:
            applications.output_log(vd["loglevel"], vd["logbody"])
        is_file = os.path.isfile(self.logpath)
        self.assertTrue(is_file)
        line_count = int(
            subprocess.check_output(["wc", "-l", self.logpath]).decode().split(" ")[0]
        )
        self.assertEqual(5, line_count)

    """ ログレベルDEBUG """

    def test_output_log_debug(self):
        name = "test_output_log_deebug"
        mode = "test"
        loglevel = "DEBUG"
        logbody = "debug log"
        result = self.get_console_log(name, mode, loglevel, logbody)
        self.assertIn(result, loglevel)

    """ ログレベルINFO """

    def test_output_log_info(self):
        name = "test_output_log_info"
        mode = "test"
        loglevel = "INFO"
        logbody = "info log"
        result = self.get_console_log(name, mode, loglevel, logbody)
        self.assertIn(result, loglevel)

    """ ログレベルWARNING """

    def test_output_log_warning(self):
        name = "test_output_log_warning"
        mode = "test"
        loglevel = "WARNING"
        logbody = "warning log"
        result = self.get_console_log(name, mode, loglevel, logbody)
        self.assertIn(result, loglevel)

    """ ログレベルERROR """

    def test_output_log_error(self):
        name = "test_output_log_error"
        mode = "test"
        loglevel = "ERROR"
        logbody = "error log"
        result = self.get_console_log(name, mode, loglevel, logbody)
        self.assertIn(result, loglevel)

    """ ログレベルCRITICAL """

    def test_output_log_critical(self):
        name = "test_output_log_critical"
        mode = "test"
        loglevel = "CRITICAL"
        logbody = "critical log"
        result = self.get_console_log(name, mode, loglevel, logbody)
        self.assertIn(result, loglevel)

    """ Exception """

    def test_output_log_exception(self):
        name = "test_output_log_exception"
        logbody = "exception log"
        loglevel = "EXCEPTION"
        mode = "dev"
        applications = ApplicationLogs(name, mode, self.logpath)
        with self.assertRaises(Exception, msg="Generate log exception!!"):
            applications.output_log(loglevel, logbody)
