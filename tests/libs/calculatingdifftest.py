import datetime
import pathlib
import sys

sys.path.append("..")

current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_dir) + "/../..")
from unittest import TestCase

from libs.calculatingdiff import CalculatingDifference


class TestCalculatingDifference(TestCase):

    mode = "test"
    calcdiff = CalculatingDifference(mode)

    """ 待ち時間取得 """

    def test_get_intervaltime(self):
        # 件数に100件を指定
        print("\n100items-->>")
        reccount = 100
        result = self.calcdiff.get_intervaltime(reccount)
        print(result)
        self.assertIsInstance(result, int)
        # 件数に300件を指定
        print("1000items-->>")
        reccount = 1000
        result = self.calcdiff.get_intervaltime(reccount)
        print(result)
        self.assertIsInstance(result, int)
        # 件数に50件を指定
        print("50items-->>")
        reccount = 50
        result = self.calcdiff.get_intervaltime(reccount)
        print(result)
        self.assertIsInstance(result, int)
        # 59分の処理
        print("59minutes-->>")
        reccount = 100
        fiftynine = datetime.datetime.now().strftime("%Y-%m-%d %H:59:%S")
        time = datetime.datetime.strptime(fiftynine, "%Y-%m-%d %H:%M:%S")
        result = self.calcdiff.get_intervaltime(reccount, time)
        print(result)
        self.assertIsInstance(result, int)

    """ ID数の比較 """

    def test_get_diffids(self):
        # ids1に差分がある場合(ids1に親アカウントを入れる前提)
        print("\ndifference ids1-->>")
        ids1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        ids2 = [1, 2, 3, 4, 5, 6]
        testresult = [7, 8, 9]
        result = self.calcdiff.get_diffids(ids1, ids2)
        self.assertEqual(result, testresult)
        # ids2に差分がある場合
        print("difference ids2-->>")
        ids1 = [1, 2, 3, 4, 5, 6]
        ids2 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        testresult = []
        result = self.calcdiff.get_diffids(ids1, ids2)
        self.assertEqual(result, testresult)
        # 差分がない場合
        print("No difference-->>")
        ids1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        ids2 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        testresult = []
        result = self.calcdiff.get_diffids(ids1, ids2)
        self.assertEqual(result, testresult)
        # 0件同士
        print("0 items-->>")
        ids1 = []
        ids2 = []
        testresult = []
        result = self.calcdiff.get_diffids(ids1, ids2)
        self.assertEqual(result, testresult)
